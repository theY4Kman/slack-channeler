from slack_channeler import objects, events
from slack_channeler.schema import BaseEventSchema, fields

__all__ = [
    'PinAddedSchema',
    'PinRemovedSchema',
]


class PinAddedSchema(BaseEventSchema):
    class Meta:
        model = events.PinAdded
        event_type = 'pin_added'

    user = fields.ObjectId(objects.User)
    channel = fields.ObjectId(objects.Channel, data_key='channel_id')
    item = fields.Object(objects.Message)
    event_ts = fields.TimestampStr()


class PinRemovedSchema(BaseEventSchema):
    class Meta:
        model = events.PinRemoved
        event_type = 'pin_removed'

    user = fields.ObjectId(objects.User)
    channel = fields.ObjectId(objects.Channel, data_key='channel_id')
    item = fields.Object(objects.Message)
    has_pins = fields.Boolean()
    event_ts = fields.TimestampStr()
