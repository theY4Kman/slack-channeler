from channels.routing import ProtocolTypeRouter, ChannelNameRouter

from examplebot import consumers

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        'slack': consumers.SlackConsumer,
    })
})
