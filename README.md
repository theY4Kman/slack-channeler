# slack-channeler
Power a Slack bot with Django Channels v2


# Installation
```bash
pip install slack-channeler
```


# Usage
slack-channeler relays slack events on the channel layer. First, ensure `CHANNEL_LAYERS` is configured in your Django settings. [channels-redis](https://github.com/django/channels_redis) is recommended.
```python
# settings.py

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}
```

Now, we add `slack_channeler` to `INSTALLED_APPS`, so we can run slack channeler using `manage.py`; and store our Slack token in the settings.
```python
# settings.py

INSTALLED_APPS = [
    # ...
    'slack_channeler',
]

SLACK_CHANNELER_TOKEN = 'xoxb-12345678900-098765432100-DeadBeefFeed90iIJjYsf3ay'
```

Create a consumer to handle Slack events
```python
# consumers.py

from channels.consumer import AsyncConsumer, get_handler_name

class SlackConsumer(AsyncConsumer):
    async def dispatch(self, message):
        handler = getattr(self, get_handler_name(message), None)
        if handler:
            await handler(**message['data'])

    async def slack_message(self, channel, text, **kwargs):
        # Simply echo back message
        await self.channel_layer.send('slack', {
            'type': 'message',
            'channel': channel,
            'text': text,
        })
```

Route Slack events to the consumer
```python
# routing.py

from channels.routing import ProtocolTypeRouter, ChannelNameRouter

from .consumers import SlackConsumer

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'slack': SlackConsumer,
    }),
})
```

Start a Channels worker to handle Slack events from the channel layer
```bash
python manage.py runworker slack
```

Lastly, run slack-channeler
```bash
python manage.py slack_channeler
```


# Building package
Currently, poetry does not support dynamic generation of version files, nor custom hooks to do so. To keep `pyproject.toml` the source of authority for version numbers, a custom `build.py` script is used to dynamically generate `version.py`.

To build slack-channeler, run `python build.py`. This has the same semantics as `poetry build`.
