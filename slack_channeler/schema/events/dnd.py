from slack_channeler import events, objects
from slack_channeler.schema import fields
from slack_channeler.schema.base import BaseEventSchema

__all__ = [
    'DndUpdatedSchema',
    'DndUpdatedUserSchema',
]


class DndUpdatedSchema(BaseEventSchema):
    class Meta:
        model = events.DndUpdated
        event_type = 'dnd_updated'

    user = fields.ObjectId(objects.User)
    dnd_status = fields.Object(objects.DoNotDisturb)


class DndUpdatedUserSchema(BaseEventSchema):
    class Meta:
        model = events.DndUpdatedUser
        event_type = 'dnd_updated_user'

    user = fields.ObjectId(objects.User)
    dnd_status = fields.Object(objects.DoNotDisturb)
