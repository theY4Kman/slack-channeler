from slack_channeler import objects, events
from slack_channeler.schema import BaseEventSchema, fields

__all__ = [
    'StarAddedSchema',
    'StarRemovedSchema',
]


class StarAddedSchema(BaseEventSchema):
    class Meta:
        model = events.StarAdded
        event_type = 'star_added'

    user = fields.ObjectId(objects.User)
    item = fields.Object(objects.Message)
    event_ts = fields.TimestampStr()


class StarRemovedSchema(BaseEventSchema):
    class Meta:
        model = events.StarRemoved
        event_type = 'star_removed'

    user = fields.ObjectId(objects.User)
    item = fields.Object(objects.Message)
    event_ts = fields.TimestampStr()
