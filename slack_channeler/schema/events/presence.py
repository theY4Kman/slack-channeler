from slack_channeler import objects, events
from slack_channeler.schema import BaseEventSchema, fields

__all__ = ['PresenceChangeSchema']


class PresenceChangeSchema(BaseEventSchema):
    class Meta:
        model = events.PresenceChange
        event_type = 'presence_change'

    user = fields.ObjectId(objects.User)
    presence = fields.String()
