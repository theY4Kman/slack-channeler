from slack_channeler import events, objects
from slack_channeler.schema import fields, BaseEventSchema

__all__ = ['MessageSchema']


class MessageSchema(BaseEventSchema):
    class Meta:
        model = events.Message
        event_type = 'message'

    event_ts = fields.TimestampStr()
    ts = fields.String()

    channel = fields.ObjectId(objects.Channel)
    user = fields.ObjectId(objects.User)

    # TODO: further parsing
    blocks = fields.List(fields.Dict())
