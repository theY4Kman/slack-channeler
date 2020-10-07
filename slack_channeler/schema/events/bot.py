from slack_channeler import events, objects
from slack_channeler.schema import fields
from slack_channeler.schema.base import BaseEventSchema

__all__ = ['BotAddedSchema']


class BotAddedSchema(BaseEventSchema):
    class Meta:
        model = events.BotAdded
        event_type = 'bot_added'

    bot = fields.Object(objects.Bot)
