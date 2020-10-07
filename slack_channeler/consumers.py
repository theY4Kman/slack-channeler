import asyncio
import functools
import logging
import uuid
from typing import Any, Dict, Awaitable, Union, Iterable

from channels.consumer import AsyncConsumer, get_handler_name
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
from channels.utils import await_many_dispatch
from slack.errors import SlackApiError

from slack_channeler import schema, objects
from slack_channeler.util import pprint_event

logger = logging.getLogger(__name__)


class SlackChannelerConsumer(AsyncConsumer):
    #: Whether to pretty-print slack events to console
    print_events: bool = False

    #: Whether to pretty-print API call responses to console
    print_api_responses: bool = False

    def __init__(self, scope):
        super().__init__(scope)

        self.bot_id = None
        self.user_id = None
        self.user_name = None

        #: Mapping of request IDs to Futures, used to notify API requests of responses
        self._api_requests: Dict[str, asyncio.Future] = {}

    async def __call__(self, receive, send):
        """Dispatches incoming messages to type-based handlers asynchronously.
        """
        # Initialize channel layer
        self.channel_layer = get_channel_layer(self.channel_layer_alias)
        if self.channel_layer is not None:
            self.channel_name = await self.channel_layer.new_channel()
            self.channel_receive = functools.partial(
                self.channel_layer.receive, self.channel_name
            )

        # Store send function
        self.base_send = send

        # Perform any startup tasks
        await self.initialize()

        # Pass messages in from channel layer or client to dispatch method
        try:
            await await_many_dispatch(
                [receive, self.channel_receive],
                self.dispatch_nonblocking,
            )
        except StopConsumer:
            # Exit cleanly
            pass

    async def initialize(self):
        asyncio.create_task(self._determine_identity())

    async def _determine_identity(self):
        logger.debug('Calling auth_test to determine our identity ...')
        res = await self.send('api.auth_test')

        self.bot_id = res['bot_id']
        self.user_id = res['user_id']
        self.user_name = res['user']
        logger.info('Learned our identity: bot %s, user %s (%r)', self.bot_id, self.user_id, self.user_name)

    async def dispatch_nonblocking(self, message):
        """Perform dispatch in a task, and return immediately
        """
        # TODO: ensure cleanup
        asyncio.create_task(self.dispatch(message))

    async def dispatch(self, message):
        type_ = message.get('type')
        data = message.get('data')

        if type_ == 'api.response':
            if self.print_api_responses:
                pprint_event(type_, data)

            request_id = message['request_id']
            error = message['error']

            if response_fut := self._api_requests.get(request_id):
                if error:
                    exc = SlackApiError(error, data)
                    response_fut.set_exception(exc)
                else:
                    response_fut.set_result(data)
                del self._api_requests[request_id]

            return

        if self.print_events:
            pprint_event(type_, data)

        handler_name = get_handler_name(message)
        handler = getattr(self, handler_name, None)
        if handler:
            if type_.startswith('slack.'):
                event_type = type_[len('slack.'):]
                event = await self.hydrate(event_type, data)
                arg = event
            else:
                arg = data

            await handler(arg)
        else:
            logger.debug(f'Unhandled slack event {message["type"]} '
                         f'(no {handler_name} method defined)')

    async def hydrate(self, type, data):
        try:
            return schema.hydrate(type, consumer=self, data=data)
        except ValueError:
            return data

    async def send(self, type_: str, message: Dict[str, Any] = None, /, *,
                   request_id: str = None,
                   as_future: bool = False,
                   **fields) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """Send a command to the slack-channeler client

        :param type_:
            Type of message to send to slack-channeler.

        :param message:
            Dict of fields to send as data to slack-channeler

        :param request_id:
            All messages to slack-channeler have a request_id. This value may
            be set manually; otherwise, a UUID4 will be generated.

        :param as_future:
            If False (default), the eventual response from slack-channeler will
            be returned. Otherwise, if True, a Future representing the eventual
            response from slack-channeler will be returned, which must further
            be awaited to retrieve the response.

        :param fields:
            Additional keyword arg fields to pass as data to slack-channeler

        :return:
            The response from slack-channeler. This will be Slack's response
            if the type_ is of the form `api.xyz`

        """
        if request_id is None:
            request_id = str(uuid.uuid4())

        data = {}
        if message:
            data.update(message)
        data.update(fields)

        response_fut = self._api_requests[request_id] = asyncio.Future()
        await self.channel_layer.send('slack_channeler', {
            'type': type_,
            'reply_channel': self.channel_name,
            'request_id': request_id,
            'data': data,
        })

        if as_future:
            return response_fut
        else:
            return await response_fut

    async def send_rtm_event(self, type_: str, **fields) -> None:
        """Send an event upstream over the RTM websocket
        """
        return await self.channel_layer.send('slack_channeler', {
            'type': f'slack.{type_}',
            'data': fields,
        })

    async def send_message(self, *, channel: str, text: str, **fields,
                           ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """Send a Slack message
        """
        return await self.api_call('chat_postMessage', channel=channel, text=text, **fields)

    async def api_call(self, method: str, /, **arguments,
                       ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """Perform an arbitrary API call
        """
        method = method.replace('.', '_')
        return await self.send(f'api.{method}', arguments)

    async def presence_query(self, users: Iterable[str, objects.User]) -> None:
        """Ask the message server to send presence_change events for the specified users

        See: https://api.slack.com/events/presence_query
        """
        ids = [str(user) for user in users]
        return await self.send_rtm_event('presence_query', ids=ids)

    async def presence_sub(self, users: Iterable[str, objects.User]) -> None:
        """Subscribe to all presence_change events for the specified users

        NOTE: the user list here will OVERWRITE any previous subscriptions

        See: https://api.slack.com/events/presence_sub
        """
        ids = [str(user) for user in users]
        return await self.send_rtm_event('presence_query', ids=ids)
