from slack_channeler import objects, events
from slack_channeler.schema import fields, BaseEventSchema

__all__ = [
    'MemberJoinedChannelSchema',
    'MemberLeftChannelSchema',
]


class MemberJoinedChannelSchema(BaseEventSchema):
    class Meta:
        model = events.MemberJoinedChannel
        event_type = 'member_joined_channel'

    user = fields.ObjectId(objects.User)
    channel = fields.ObjectId(objects.Channel)
    channel_type = fields.String()
    team = fields.ObjectId(objects.Team)
    inviter: objects.User = fields.ObjectId(objects.User)


class MemberLeftChannelSchema(BaseEventSchema):
    class Meta:
        model = events.MemberLeftChannel
        event_type = 'member_left_channel'

    user = fields.ObjectId(objects.User)
    channel = fields.ObjectId(objects.Channel)
    channel_type = fields.String()
    team = fields.ObjectId(objects.Team)
