import logging
import sys
from typing import Dict, Any

import slack
from channels.layers import get_channel_layer
from django.core.management.base import OutputWrapper
from slack.errors import SlackApiError

from slack_channeler.util import pprint_event

logger = logging.getLogger(__name__)


class ChannelsSlackClient(slack.RTMClient):
    _web_client: slack.WebClient

    def __init__(self, *args, print_events: bool = False, relay_self: bool = False, **kwargs):
        super().__init__(*args, **kwargs, run_async=True)

        self.print_events = print_events
        self._stderr = OutputWrapper(sys.stderr)

        self.relay_self = relay_self

        #: Our bot's identity, used to prevent relaying our own messages over the channel
        self.bot_id = None
        self.user_id = None
        self.user_name = None

        self.channel_layer = get_channel_layer()

    def start(self):
        try:
            logger.info('Starting slack-channeler')
            self._event_loop.run_until_complete(super().start())
        finally:
            logger.info('Cleaning up')
            self._event_loop.stop()

    async def determine_identity(self):
        res = await self._web_client.auth_test()
        self.bot_id = res['bot_id']
        self.user_id = res['user_id']
        self.user_name = res['user']
        logger.info('Learned our identity: bot %s, user %s (%r)', self.bot_id, self.user_id, self.user_name)

    def is_self_action(self, data) -> bool:
        """Determine whether an action originates from ourselves
        """
        if data:
            return data.get('user') == self.user_id or data.get('bot_id') == self.bot_id

    async def _start_channel_worker(self):
        while message := await self.channel_layer.receive('slack_channeler'):
            type_ = message.get('type')
            data = message.get('data')
            reply_channel = message.get('reply_channel')
            request_id = message.get('request_id')

            ###
            # Send an RTM message upstream to Slack
            #
            if type_.startswith('slack.'):
                event_type = type_[len('slack.'):]
                payload = {
                    **data,
                    'type': event_type,
                }
                await self.send_over_websocket(payload=payload)

            ###
            # Make an API call with the Slack web client
            #
            elif type_.startswith('api.'):
                method = type_[len('api.'):]

                try:
                    response = await self.call_api(method, data)
                    error = None
                except SlackApiError as e:
                    logger.exception('Error encountered calling API with params %s', message)
                    response = e.response
                    error = str(e).rsplit('\n', maxsplit=1)[0]

                await self.respond(reply_channel, request_id, response.data, error)

            else:
                logger.warning('Unhandled message type %r received: %r', type_, message)

    async def _dispatch_event(self, event, data=None):
        if self.print_events:
            self._stderr.write('')
            pprint_event(event, data, stream=self._stderr)

        await self.forward_event(event=event, data=data)

    async def forward_event(self, event, data):
        if event == 'open':
            await self.determine_identity()
            self._event_loop.create_task(self._start_channel_worker())

        if not self.relay_self:
            if self.is_self_action(data):
                logger.debug(f'Skipping relay of our own action: {data!r}')
                return

        subtype = data.get('subtype', None) if isinstance(data, dict) else None
        components = ['slack', event, subtype]
        channels_event_type = '.'.join(s for s in components if s)

        logger.debug('Forwarding %s over channel layer: %r', channels_event_type, data)
        await self.channel_layer.send('slack', {
            'type': channels_event_type,
            'data': data,
        })

    async def call_api(self, method: str, data: Dict[str, Any]):
        handler = getattr(self._web_client, method)
        return await handler(**data)

    async def respond(self, reply_channel: str, request_id: str, data, error: str = None):
        logger.debug(f'Responding to api request {request_id} over {reply_channel}: {data!r}')
        await self.channel_layer.send(reply_channel, {
            'type': 'api.response',
            'request_id': request_id,
            'data': data,
            'error': error,
        })


#XXX######################################################################################
#XXX######################################################################################
#XXX######################################################################################
import os
if os.getenv('PDB'):
    def info(type, value, tb):
        if hasattr(sys, 'ps1') or not sys.stderr.isatty():
            # we are in interactive mode or we don't have a tty-like
            # device, so we call the default hook
            sys.__excepthook__(type, value, tb)
        else:
            import traceback, pdb
            # we are NOT in interactive mode, print the exception...
            traceback.print_exception(type, value, tb)
            # ...then start the debugger in post-mortem mode.
            pdb.post_mortem(tb)

    sys.excepthook = info
#XXX######################################################################################
#XXX######################################################################################
#XXX######################################################################################
