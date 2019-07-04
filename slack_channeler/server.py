import functools
import inspect
import logging
from collections import defaultdict
from typing import Callable, List, Dict

import slack
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

SLACK_CALLBACK_MARK = '_slack_events'


def run_on(*, event: str):
    """A decorator to store and link a callback to an event."""

    def decorator(callback):
        @functools.wraps(callback)
        def decorator_wrapper():
            events = getattr(callback, SLACK_CALLBACK_MARK, [])
            #
            # We insert the event at the beginning of the list, so the topmost
            # decorator has first priority.
            #
            events.insert(0, event)

            setattr(callback, SLACK_CALLBACK_MARK, events)
            return callback

        return decorator_wrapper()

    return decorator


class BaseRTMClient(slack.RTMClient):
    _declared_callbacks: Dict[str, List[Callable]]

    def __init__(self, *args, **kwargs):
        self._callbacks = defaultdict(list)
        self._register_declared_callbacks()
        super().__init__(*args, **kwargs)

    def on(self, *, event: str, callback: Callable):
        """Stores and links the callback(s) to the event.

        Unlike slack.RTMClient's on(), this method stores the event callback
        against the client *instance*, not against the class. This allows
        multiple clients to have differing callbacks, without interfering with
        each other.

        Args:
            event (str): A string that specifies a Slack or websocket event.
                e.g. 'channel_joined' or 'open'
            callback (Callable): Any object or a list of objects that can be called.
                e.g. <function say_hello at 0x101234567> or
                [<function say_hello at 0x10123>,<function say_bye at 0x10456>]

        Raises:
            SlackClientError: The specified callback is not callable.
            SlackClientError: The callback must accept keyword arguments (**kwargs).
        """
        if isinstance(callback, list):
            for cb in callback:
                self._validate_callback(cb)
            previous_callbacks = self._callbacks[event]
            self._callbacks[event] = list(set(previous_callbacks + callback))
        else:
            self._validate_callback(callback)
            self._callbacks[event].append(callback)

    def _register_declared_callbacks(self):
        """Enumerate any @run_on-decorated event callbacks
        """
        for name, callback in inspect.getmembers(self, inspect.ismethod):
            if not hasattr(callback, SLACK_CALLBACK_MARK):
                continue

            events = getattr(callback, SLACK_CALLBACK_MARK)
            for event in events:
                self.on(event=event, callback=callback)


class ChannelsSlackClient(BaseRTMClient):
    _web_client: slack.WebClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, run_async=True)

        #: Our bot's ID, used to prevent relaying our own messages over the channel
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

    async def _start_channel_worker(self):
        while True:
            message = await self.channel_layer.receive('slack')
            if message.get('type') == 'message':
                del message['type']
                await self.send_message(message)

    def _dispatch_event(self, event, data=None):
        self._execute_callback_async(self.forward_event, {
            'event': event,
            'data': data,
        })

    async def forward_event(self, rtm_client, web_client, data):
        event = data['event']
        data = data['data']

        if event == 'open':
            self.user_id = data['self']['id']
            self.user_name = data['self']['name']
            self._event_loop.create_task(self._start_channel_worker())

        if event == 'message' and data.get('user') == self.user_id:
            logger.debug(f'Skipping relay of our own message: {data!r}')
            return

        await self.channel_layer.send('slack', {
            'type': f'slack.{event}',
            'data': data,
        })

    async def send_message(self, data):
        await self._web_client.chat_postMessage(**data, as_user=True)
