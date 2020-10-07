from slack_channeler import events
from slack_channeler.schema import fields
from slack_channeler.schema.base import BaseEventSchema

__all__ = ['CommandsChangedSchema']


class CommandsChangedSchema(BaseEventSchema):
    class Meta:
        model = events.CommandsChanged
        event_type = 'commands_changed'

    event_ts = fields.TimestampStr()
