from slack_channeler import events, objects
from slack_channeler.schema import BaseEventSchema, fields

__all__ = [
    'ReactionAddedSchema',
    'ReactionRemovedSchema',
]


class ReactionAddedSchema(BaseEventSchema):
    class Meta:
        model = events.ReactionAdded
        event_type = 'reaction_added'

    ts = fields.String()
    user = fields.ObjectId(objects.User)
    reaction = fields.String()
    item_user = fields.ObjectId(objects.User)
    # XXX: can this be other types?
    item = fields.Object(objects.Message)
    event_ts = fields.TimestampStr()


class ReactionRemovedSchema(BaseEventSchema):
    class Meta:
        model = events.ReactionRemoved
        event_type = 'reaction_removed'

    user = fields.ObjectId(objects.User)
    reaction = fields.String()
    item_user = fields.ObjectId(objects.User)
    # XXX: can this be other types?
    item = fields.Object(objects.Message)
    event_ts = fields.TimestampStr()
