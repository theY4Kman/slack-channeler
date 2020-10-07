from slack_channeler import events, objects
from slack_channeler.schema import fields
from slack_channeler.schema.base import BaseEventSchema

__all__ = [
    'ChannelArchiveSchema',
    'ChannelCreatedSchema',
    'ChannelDeletedSchema',
    'ChannelHistoryChangedSchema',
    'ChannelJoinedSchema',
    'ChannelLeftSchema',
    'ChannelMarkedSchema',
    'ChannelRenameSchema',
    'ChannelUnarchiveSchema',
]


class ChannelArchiveSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelArchive
        event_type = 'channel_archive'

    channel = fields.ObjectId(objects.Channel)
    user = fields.ObjectId(objects.User)


class ChannelCreatedSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelCreated
        event_type = 'channel_created'

    channel = fields.Object(objects.Channel)


class ChannelDeletedSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelDeleted
        event_type = 'channel_deleted'

    channel = fields.ObjectId(objects.Channel)


class ChannelHistoryChangedSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelHistoryChanged
        event_type = 'channel_history_changed'

    latest = fields.String()
    ts = fields.String()
    event_ts = fields.TimestampStr()


class ChannelJoinedSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelJoined
        event_type = 'channel_joined'

    channel = fields.Object(objects.Channel)


class ChannelLeftSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelLeft
        event_type = 'channel_left'

    channel = fields.ObjectId(objects.Channel)


class ChannelMarkedSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelMarked
        event_type = 'channel_marked'

    channel = fields.ObjectId(objects.Channel)
    ts = fields.String()


class ChannelRenameSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelRename
        event_type = 'channel_rename'

    channel = fields.Object(objects.Channel)


class ChannelUnarchiveSchema(BaseEventSchema):
    class Meta:
        model = events.ChannelUnarchive
        event_type = 'channel_unarchive'

    channel = fields.ObjectId(objects.Channel)
    user = fields.ObjectId(objects.User)
