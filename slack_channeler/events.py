from datetime import datetime
from typing import TYPE_CHECKING

from dataclassy import dataclass

from slack_channeler import objects

if TYPE_CHECKING:
    from slack_channeler import SlackChannelerConsumer


@dataclass
class BaseEvent:
    type: str
    consumer: 'SlackChannelerConsumer' = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class AccountsChanged(BaseEvent):
    type = 'accounts_changed'


class BotAdded(BaseEvent):
    type = 'bot_added'
    bot: objects.Bot = None


class BotChanged(BaseEvent):
    type = 'bot_changed'
    bot = None


class ChannelArchive(BaseEvent):
    type = 'channel_archive'
    channel = None
    user = None


class ChannelCreated(BaseEvent):
    type = 'channel_created'
    channel = None


class ChannelDeleted(BaseEvent):
    type = 'channel_deleted'
    channel = None


class ChannelHistoryChanged(BaseEvent):
    type = 'channel_history_changed'
    latest = None
    ts = None
    event_ts = None


class ChannelJoined(BaseEvent):
    type = 'channel_joined'
    channel = None


class ChannelLeft(BaseEvent):
    type = 'channel_left'
    channel = None


class ChannelMarked(BaseEvent):
    type = 'channel_marked'
    channel = None
    ts = None


class ChannelRename(BaseEvent):
    type = 'channel_rename'
    channel = None


class ChannelUnarchive(BaseEvent):
    type = 'channel_unarchive'
    channel = None
    user = None


class CommandsChanged(BaseEvent):
    type = 'commands_changed'
    event_ts = None


class DndUpdated(BaseEvent):
    type = 'dnd_updated'
    user = None
    dnd_status = None


class DndUpdatedUser(BaseEvent):
    type = 'dnd_updated_user'
    user = None
    dnd_status = None


class EmailDomainChanged(BaseEvent):
    type = 'email_domain_changed'
    email_domain = None
    event_ts = None


class EmojiChanged(BaseEvent):
    type = 'emoji_changed'
    subtype = None
    names = None
    event_ts = None


class ExternalOrgMigrationFinished(BaseEvent):
    type = 'external_org_migration_finished'
    team = None
    date_started = None
    date_finished = None


class ExternalOrgMigrationStarted(BaseEvent):
    type = 'external_org_migration_started'
    team = None
    date_started = None


class FileChange(BaseEvent):
    type = 'file_change'
    file_id = None
    file = None


class FileCommentAdded(BaseEvent):
    type = 'file_comment_added'
    comment = None
    file_id = None
    file = None


class FileCommentDeleted(BaseEvent):
    type = 'file_comment_deleted'
    comment = None
    file_id = None
    file = None


class FileCommentEdited(BaseEvent):
    type = 'file_comment_edited'


class FileCreated(BaseEvent):
    type = 'file_created'
    file_id = None
    file = None


class FileDeleted(BaseEvent):
    type = 'file_deleted'
    file_id = None
    event_ts = None


class FilePublic(BaseEvent):
    type = 'file_public'
    file_id = None
    file = None


class FileShared(BaseEvent):
    type = 'file_shared'
    file_id = None
    file = None


class FileUnshared(BaseEvent):
    type = 'file_unshared'
    file_id = None
    file = None


class Goodbye(BaseEvent):
    type = 'goodbye'


class GroupArchive(BaseEvent):
    type = 'group_archive'
    channel = None


class GroupClose(BaseEvent):
    type = 'group_close'
    user = None
    channel = None


class GroupDeleted(BaseEvent):
    type = 'group_deleted'
    channel = None


class GroupHistoryChanged(BaseEvent):
    type = 'group_history_changed'
    latest = None
    ts = None
    event_ts = None


class GroupJoined(BaseEvent):
    type = 'group_joined'
    channel = None


class GroupLeft(BaseEvent):
    type = 'group_left'
    channel = None


class GroupMarked(BaseEvent):
    type = 'group_marked'
    channel = None
    ts = None


class GroupOpen(BaseEvent):
    type = 'group_open'
    user = None
    channel = None


class GroupRename(BaseEvent):
    type = 'group_rename'
    channel = None


class GroupUnarchive(BaseEvent):
    type = 'group_unarchive'
    channel = None


class Hello(BaseEvent):
    type = 'hello'


class ImClose(BaseEvent):
    type = 'im_close'
    user = None
    channel = None


class ImCreated(BaseEvent):
    type = 'im_created'
    user = None
    channel = None


class ImHistoryChanged(BaseEvent):
    type = 'im_history_changed'
    latest = None
    ts = None
    event_ts = None


class ImMarked(BaseEvent):
    type = 'im_marked'
    channel = None
    ts = None


class ImOpen(BaseEvent):
    type = 'im_open'
    user = None
    channel = None


class ManualPresenceChange(BaseEvent):
    type = 'manual_presence_change'
    presence = None


class MemberJoinedChannel(BaseEvent):
    type = 'member_joined_channel'
    user: objects.User = None
    channel: objects.Channel = None
    channel_type: str = None
    team: objects.Team = None
    inviter: objects.User = None


class MemberLeftChannel(BaseEvent):
    type = 'member_left_channel'
    user: objects.User = None
    channel: objects.Channel = None
    channel_type: str = None
    team: objects.Team = None


class Message(objects.Message, BaseEvent):
    type = 'message'

    event_ts: str = None

    client_msg_id: str = None
    suppress_notification: bool = None
    team: str = None
    source_team: str = None
    username: str = None
    user_team: str = None


class PinAdded(BaseEvent):
    type = 'pin_added'
    user: objects.User = None
    channel: objects.Channel = None
    item: objects.Message = None
    event_ts: datetime = None

    @property
    def channel_id(self):
        # For compatibility with Slack event's transmitted fields
        return self.channel.id


class PinRemoved(BaseEvent):
    type = 'pin_removed'
    user: objects.User = None
    channel: objects.Channel = None
    item: objects.Message = None
    has_pins: bool = None
    event_ts: datetime = None

    @property
    def channel_id(self):
        # For compatibility with Slack event's transmitted fields
        return self.channel.id


class PrefChange(BaseEvent):
    type = 'pref_change'
    name = None
    value = None


class PresenceChange(BaseEvent):
    type = 'presence_change'
    user: objects.User = None
    presence: str = None


class ReactionAdded(BaseEvent):
    type = 'reaction_added'
    ts: str
    user: objects.User = None
    reaction: str = None
    item_user: objects.User = None
    item: objects.Message = None
    event_ts: datetime = None


class ReactionRemoved(BaseEvent):
    type = 'reaction_removed'
    user: objects.User = None
    reaction = None
    item_user: objects.User = None
    item: objects.Message = None
    event_ts: datetime = None


class ReconnectUrl(BaseEvent):
    type = 'reconnect_url'


class StarAdded(BaseEvent):
    type = 'star_added'
    user: objects.User = None
    item: objects.Message = None
    event_ts: datetime = None


class StarRemoved(BaseEvent):
    type = 'star_removed'
    user: objects.User = None
    item: objects.Message = None
    event_ts: datetime = None


class SubteamCreated(BaseEvent):
    type = 'subteam_created'
    subteam = None


class SubteamMembersChanged(BaseEvent):
    type = 'subteam_members_changed'


class SubteamSelfAdded(BaseEvent):
    type = 'subteam_self_added'
    subteam_id = None


class SubteamSelfRemoved(BaseEvent):
    type = 'subteam_self_removed'
    subteam_id = None


class SubteamUpdated(BaseEvent):
    type = 'subteam_updated'


class TeamDomainChange(BaseEvent):
    type = 'team_domain_change'
    url = None
    domain = None


class TeamJoin(BaseEvent):
    type = 'team_join'
    user = None


class TeamMigrationStarted(BaseEvent):
    type = 'team_migration_started'


class TeamPlanChange(BaseEvent):
    type = 'team_plan_change'
    plan = None
    can_add_ura = None
    paid_features = None


class TeamPrefChange(BaseEvent):
    type = 'team_pref_change'
    name = None
    value = None


class TeamProfileChange(BaseEvent):
    type = 'team_profile_change'


class TeamProfileDelete(BaseEvent):
    type = 'team_profile_delete'


class TeamProfileReorder(BaseEvent):
    type = 'team_profile_reorder'


class TeamRename(BaseEvent):
    type = 'team_rename'
    name = None


class UserChange(BaseEvent):
    type = 'user_change'
    user = None


class UserTyping(BaseEvent):
    type = 'user_typing'
    channel = None
    user = None


EVENT_CLASSES_BY_TYPE = {
    event_cls.type: event_cls
    for event_cls in BaseEvent.__subclasses__()
}

###
# These events, descriptions, and example event bodies were scraped from
# https://api.slack.com/events
#
RTM_EVENT_DOCS = {
    'accounts_changed': {
        'description': 'The list of accounts a user is signed into has changed',
        'doc_url': 'https://api.slack.com/events/accounts_changed',
        'example_body': {'type': 'accounts_changed'},
    },
    'bot_added': {
        'description': 'A bot user was added',
        'doc_url': 'https://api.slack.com/events/bot_added',
        'example_body': {
            'bot': {
                'app_id': 'A4H1JB4AZ',
                'icons': {
                    'image_48': 'https://slack.com/path/to/hugbot_48.png',
                },
                'id': 'B024BE7LH',
                'name': 'hugbot',
            },
            'type': 'bot_added',
        },
    },
    'bot_changed': {
        'description': 'A bot user was changed',
        'doc_url': 'https://api.slack.com/events/bot_changed',
        'example_body': {
            'bot': {
                'app_id': 'A4H1JB4AZ',
                'icons': {
                    'image_48': 'https://slack.com/path/to/hugbot_48.png',
                },
                'id': 'B024BE7LH',
                'name': 'hugbot',
            },
            'type': 'bot_changed',
        },
    },
    'channel_archive': {
        'description': 'A channel was archived',
        'doc_url': 'https://api.slack.com/events/channel_archive',
        'example_body': {
            'channel': 'C024BE91L',
            'type': 'channel_archive',
            'user': 'U024BE7LH',
        },
    },
    'channel_created': {
        'description': 'A channel was created',
        'doc_url': 'https://api.slack.com/events/channel_created',
        'example_body': {
            'channel': {
                'created': 1360782804,
                'creator': 'U024BE7LH',
                'id': 'C024BE91L',
                'name': 'fun',
            },
            'type': 'channel_created',
        },
    },
    'channel_deleted': {
        'description': 'A channel was deleted',
        'doc_url': 'https://api.slack.com/events/channel_deleted',
        'example_body': {
            'channel': 'C024BE91L',
            'type': 'channel_deleted',
        },
    },
    'channel_history_changed': {
        'description': "Bulk updates were made to a channel's history",
        'doc_url': 'https://api.slack.com/events/channel_history_changed',
        'example_body': {
            'event_ts': '1361482916.000004',
            'latest': '1358877455.000010',
            'ts': '1361482916.000003',
            'type': 'channel_history_changed',
        },
    },
    'channel_joined': {
        'description': 'You joined a channel',
        'doc_url': 'https://api.slack.com/events/channel_joined',
        'example_body': {
            'channel': {
                'id': 'C024BE91L',
                'name': 'fun',
                'created': 1360782804,
                'creator': 'U024BE7LH'
            },
            'type': 'channel_joined',
        },
    },
    'channel_left': {
        'description': 'You left a channel',
        'doc_url': 'https://api.slack.com/events/channel_left',
        'example_body': {'channel': 'C024BE91L', 'type': 'channel_left'},
    },
    'channel_marked': {
        'description': 'Your channel read marker was updated',
        'doc_url': 'https://api.slack.com/events/channel_marked',
        'example_body': {
            'channel': 'C024BE91L',
            'ts': '1401383885.000061',
            'type': 'channel_marked',
        },
    },
    'channel_rename': {
        'description': 'A channel was renamed',
        'doc_url': 'https://api.slack.com/events/channel_rename',
        'example_body': {
            'channel': {
                'created': 1360782804,
                'id': 'C02ELGNBH',
                'name': 'new_name',
            },
            'type': 'channel_rename',
        },
    },
    'channel_unarchive': {
        'description': 'A channel was unarchived',
        'doc_url': 'https://api.slack.com/events/channel_unarchive',
        'example_body': {
            'channel': 'C024BE91L',
            'type': 'channel_unarchive',
            'user': 'U024BE7LH',
        },
    },
    'commands_changed': {
        'description': 'A slash command has been added or changed',
        'doc_url': 'https://api.slack.com/events/commands_changed',
        'example_body': {
            'event_ts': '1361482916.000004',
            'type': 'commands_changed',
        },
    },
    'dnd_updated': {
        'description': 'Do not Disturb settings changed for the current user',
        'doc_url': 'https://api.slack.com/events/dnd_updated',
        'example_body': {
            'dnd_status': {
                'dnd_enabled': True,
                'next_dnd_end_ts': 1450423800,
                'next_dnd_start_ts': 1450387800,
                'snooze_enabled': True,
                'snooze_endtime': 1450373897,
            },
            'type': 'dnd_updated',
            'user': 'U1234',
        },
    },
    'dnd_updated_user': {
        'description': 'Do not Disturb settings changed for a member',
        'doc_url': 'https://api.slack.com/events/dnd_updated_user',
        'example_body': {
            'dnd_status': {
                'dnd_enabled': True,
                'next_dnd_end_ts': 1450423800,
                'next_dnd_start_ts': 1450387800,
            },
            'type': 'dnd_updated_user',
            'user': 'U1234',
        },
    },
    'email_domain_changed': {
        'description': 'The workspace email domain has changed',
        'doc_url': 'https://api.slack.com/events/email_domain_changed',
        'example_body': {
            'email_domain': 'example.com',
            'event_ts': '1360782804.083113',
            'type': 'email_domain_changed',
        },
    },
    'emoji_changed': {
        'description': 'A custom emoji has been added or changed',
        'doc_url': 'https://api.slack.com/events/emoji_changed',
        'example_body': {
            'event_ts': '1361482916.000004',
            'names': ['picard_facepalm'],
            'subtype': 'remove',
            'type': 'emoji_changed',
        },
    },
    'external_org_migration_finished': {
        'description': 'An enterprise grid migration has finished on an external workspace.',
        'doc_url': 'https://api.slack.com/events/external_org_migration_finished',
        'example_body': {
            'date_finished': 1551409200,
            'date_started': 1551398400,
            'team': {'id': 'TXXXXXXXX', 'is_migrating': False},
            'type': 'external_org_migration_finished',
        },
    },
    'external_org_migration_started': {
        'description': 'An enterprise grid migration has started on an external workspace.',
        'doc_url': 'https://api.slack.com/events/external_org_migration_started',
        'example_body': {
            'date_started': 1551398400,
            'team': {'id': 'TXXXXXXXX', 'is_migrating': True},
            'type': 'external_org_migration_started',
        },
    },
    'file_change': {
        'description': 'A file was changed',
        'doc_url': 'https://api.slack.com/events/file_change',
        'example_body': {
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_change',
        },
    },
    'file_comment_added': {
        'description': 'A file comment was added',
        'doc_url': 'https://api.slack.com/events/file_comment_added',
        'example_body': {
            'comment': {},
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_comment_added',
        },
    },
    'file_comment_deleted': {
        'description': 'A file comment was deleted',
        'doc_url': 'https://api.slack.com/events/file_comment_deleted',
        'example_body': {
            'comment': 'Fc67890',
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_comment_deleted',
        },
    },
    'file_comment_edited': {
        'description': 'A file comment was edited',
        'doc_url': 'https://api.slack.com/events/file_comment_edited',
        'example_body': {
            'comment': {},
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_comment_edited',
        },
    },
    'file_created': {
        'description': 'A file was created',
        'doc_url': 'https://api.slack.com/events/file_created',
        'example_body': {
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_created',
        },
    },
    'file_deleted': {
        'description': 'A file was deleted',
        'doc_url': 'https://api.slack.com/events/file_deleted',
        'example_body': {
            'event_ts': '1361482916.000004',
            'file_id': 'F2147483862',
            'type': 'file_deleted',
        },
    },
    'file_public': {
        'description': 'A file was made public',
        'doc_url': 'https://api.slack.com/events/file_public',
        'example_body': {
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_public',
        },
    },
    'file_shared': {
        'description': 'A file was shared',
        'doc_url': 'https://api.slack.com/events/file_shared',
        'example_body': {
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_shared',
        },
    },
    'file_unshared': {
        'description': 'A file was unshared',
        'doc_url': 'https://api.slack.com/events/file_unshared',
        'example_body': {
            'file': {'id': 'F2147483862'},
            'file_id': 'F2147483862',
            'type': 'file_unshared',
        },
    },
    'goodbye': {
        'description': 'The server intends to close the connection soon.',
        'doc_url': 'https://api.slack.com/events/goodbye',
        'example_body': {'type': 'goodbye'},
    },
    'group_archive': {
        'description': 'A private channel was archived',
        'doc_url': 'https://api.slack.com/events/group_archive',
        'example_body': {'channel': 'G024BE91L', 'type': 'group_archive'},
    },
    'group_close': {
        'description': 'You closed a private channel',
        'doc_url': 'https://api.slack.com/events/group_close',
        'example_body': {
            'channel': 'G024BE91L',
            'type': 'group_close',
            'user': 'U024BE7LH',
        },
    },
    'group_deleted': {
        'description': 'A private channel was deleted',
        'doc_url': 'https://api.slack.com/events/group_deleted',
        'example_body': {'channel': 'G0QN9RGTT', 'type': 'group_deleted'},
    },
    'group_history_changed': {
        'description': "Bulk updates were made to a private channel's history",
        'doc_url': 'https://api.slack.com/events/group_history_changed',
        'example_body': {
            'event_ts': '1361482916.000004',
            'latest': '1358877455.000010',
            'ts': '1361482916.000003',
            'type': 'group_history_changed',
        },
    },
    'group_joined': {
        'description': 'You joined a private channel',
        'doc_url': 'https://api.slack.com/events/group_joined',
        'example_body': {'channel': {}, 'type': 'group_joined'},
    },
    'group_left': {
        'description': 'You left a private channel',
        'doc_url': 'https://api.slack.com/events/group_left',
        'example_body': {'channel': 'G02ELGNBH', 'type': 'group_left'},
    },
    'group_marked': {
        'description': 'A private channel read marker was updated',
        'doc_url': 'https://api.slack.com/events/group_marked',
        'example_body': {
            'channel': 'G024BE91L',
            'ts': '1401383885.000061',
            'type': 'group_marked',
        },
    },
    'group_open': {
        'description': 'You created a group DM',
        'doc_url': 'https://api.slack.com/events/group_open',
        'example_body': {
            'channel': 'G024BE91L',
            'type': 'group_open',
            'user': 'U024BE7LH',
        },
    },
    'group_rename': {
        'description': 'A private channel was renamed',
        'doc_url': 'https://api.slack.com/events/group_rename',
        'example_body': {
            'channel': {
                'created': 1360782804,
                'id': 'G02ELGNBH',
                'name': 'new_name',
            },
            'type': 'group_rename',
        },
    },
    'group_unarchive': {
        'description': 'A private channel was unarchived',
        'doc_url': 'https://api.slack.com/events/group_unarchive',
        'example_body': {
            'channel': 'G024BE91L',
            'type': 'group_unarchive',
        },
    },
    'hello': {
        'description': 'The client has successfully connected to the server',
        'doc_url': 'https://api.slack.com/events/hello',
        'example_body': {'type': 'hello'},
    },
    'im_close': {
        'description': 'You closed a DM',
        'doc_url': 'https://api.slack.com/events/im_close',
        'example_body': {
            'channel': 'D024BE91L',
            'type': 'im_close',
            'user': 'U024BE7LH',
        },
    },
    'im_created': {
        'description': 'A DM was created',
        'doc_url': 'https://api.slack.com/events/im_created',
        'example_body': {
            'channel': {},
            'type': 'im_created',
            'user': 'U024BE7LH',
        },
    },
    'im_history_changed': {
        'description': "Bulk updates were made to a DM's history",
        'doc_url': 'https://api.slack.com/events/im_history_changed',
        'example_body': {
            'event_ts': '1361482916.000004',
            'latest': '1358877455.000010',
            'ts': '1361482916.000003',
            'type': 'im_history_changed',
        },
    },
    'im_marked': {
        'description': 'A direct message read marker was updated',
        'doc_url': 'https://api.slack.com/events/im_marked',
        'example_body': {
            'channel': 'D024BE91L',
            'ts': '1401383885.000061',
            'type': 'im_marked',
        },
    },
    'im_open': {
        'description': 'You opened a DM',
        'doc_url': 'https://api.slack.com/events/im_open',
        'example_body': {
            'channel': 'D024BE91L',
            'type': 'im_open',
            'user': 'U024BE7LH',
        },
    },
    'manual_presence_change': {
        'description': 'You manually updated your presence',
        'doc_url': 'https://api.slack.com/events/manual_presence_change',
        'example_body': {
            'presence': 'away',
            'type': 'manual_presence_change',
        },
    },
    'member_joined_channel': {
        'description': 'A user joined a public or private channel',
        'doc_url': 'https://api.slack.com/events/member_joined_channel',
        'example_body': {
            'channel': 'C0698JE0H',
            'channel_type': 'C',
            'inviter': 'U123456789',
            'team': 'T024BE7LD',
            'type': 'member_joined_channel',
            'user': 'W06GH7XHN',
        },
    },
    'member_left_channel': {
        'description': 'A user left a public or private channel',
        'doc_url': 'https://api.slack.com/events/member_left_channel',
        'example_body': {
            'channel': 'C0698JE0H',
            'channel_type': 'C',
            'team': 'T024BE7LD',
            'type': 'member_left_channel',
            'user': 'W06GH7XHN',
        },
    },
    'message': {
        'description': 'A message was sent to a channel',
        'doc_url': 'https://api.slack.com/events/message',
        'example_body': {
            'channel': 'C2147483705',
            'text': 'Hello world',
            'ts': '1355517523.000005',
            'type': 'message',
            'user': 'U2147483697',
        },
    },
    'pin_added': {
        'description': 'A pin was added to a channel',
        'doc_url': 'https://api.slack.com/events/pin_added',
        'example_body': {
            'channel_id': 'C02ELGNBH',
            'event_ts': '1360782804.083113',
            'item': {},
            'type': 'pin_added',
            'user': 'U024BE7LH',
        },
    },
    'pin_removed': {
        'description': 'A pin was removed from a channel',
        'doc_url': 'https://api.slack.com/events/pin_removed',
        'example_body': {
            'channel_id': 'C02ELGNBH',
            'event_ts': '1360782804.083113',
            'has_pins': False,
            'item': {},
            'type': 'pin_removed',
            'user': 'U024BE7LH',
        },
    },
    'pref_change': {
        'description': 'You have updated your preferences',
        'doc_url': 'https://api.slack.com/events/pref_change',
        'example_body': {
            'name': 'messages_theme',
            'type': 'pref_change',
            'value': 'dense',
        },
    },
    'presence_change': {
        'description': "A member's presence changed",
        'doc_url': 'https://api.slack.com/events/presence_change',
        'example_body': {
            'presence': 'away',
            'type': 'presence_change',
            'user': 'U024BE7LH',
        },
    },
    'reaction_added': {
        'description': 'A member has added an emoji reaction to an item',
        'doc_url': 'https://api.slack.com/events/reaction_added',
        'example_body': {
            'event_ts': '1360782804.083113',
            'item': {
                'channel': 'C0G9QF9GZ',
                'ts': '1360782400.498405',
                'type': 'message',
            },
            'item_user': 'U0G9QF9C6',
            'reaction': 'thumbsup',
            'type': 'reaction_added',
            'user': 'U024BE7LH',
        },
    },
    'reaction_removed': {
        'description': 'A member removed an emoji reaction',
        'doc_url': 'https://api.slack.com/events/reaction_removed',
        'example_body': {
            'event_ts': '1360782804.083113',
            'item': {
                'channel': 'C0G9QF9GZ',
                'ts': '1360782400.498405',
                'type': 'message',
            },
            'item_user': 'U0G9QF9C6',
            'reaction': 'thumbsup',
            'type': 'reaction_removed',
            'user': 'U024BE7LH',
        },
    },
    'reconnect_url': {
        'description': 'Experimental',
        'doc_url': 'https://api.slack.com/events/reconnect_url',
        'example_body': {'type': 'reconnect_url'},
    },
    'star_added': {
        'description': 'A member has starred an item',
        'doc_url': 'https://api.slack.com/events/star_added',
        'example_body': {
            'type': 'star_added',
            'user': 'U024BE7LH',
            'item': {},
            'event_ts': '1360782804.083113'
        },
    },
    'star_removed': {
        'description': 'A member removed a star',
        'doc_url': 'https://api.slack.com/events/star_removed',
        'example_body': {
            'type': 'star_removed',
            'user': 'U024BE7LH',
            'item': {},
            'event_ts': '1360782804.083113'
        },
    },
    'subteam_created': {
        'description': 'A User Group has been added to the workspace',
        'doc_url': 'https://api.slack.com/events/subteam_created',
        'example_body': {
            'subteam': {
                'auto_type': None,
                'created_by': 'U060RNRCZ',
                'date_create': 1446746793,
                'date_delete': 0,
                'date_update': 1446746793,
                'deleted_by': None,
                'description': 'Marketing gurus, PR experts and product advocates.',
                'handle': 'marketing-team',
                'id': 'S0615G0KT',
                'is_external': False,
                'is_usergroup': True,
                'name': 'Marketing Team',
                'prefs': {'channels': [], 'groups': []},
                'team_id': 'T060RNRCH',
                'updated_by': 'U060RNRCZ',
                'user_count': '0',
            },
            'type': 'subteam_created',
        },
    },
    'subteam_members_changed': {
        'description': 'The membership of an existing User Group has changed',
        'doc_url': 'https://api.slack.com/events/subteam_members_changed',
        'example_body': None,
    },
    'subteam_self_added': {
        'description': 'You have been added to a User Group',
        'doc_url': 'https://api.slack.com/events/subteam_self_added',
        'example_body': {
            'subteam_id': 'S0615G0KT',
            'type': 'subteam_self_added',
        },
    },
    'subteam_self_removed': {
        'description': 'You have been removed from a User Group',
        'doc_url': 'https://api.slack.com/events/subteam_self_removed',
        'example_body': {
            'subteam_id': 'S0615G0KT',
            'type': 'subteam_self_removed',
        },
    },
    'subteam_updated': {
        'description': 'An existing User Group has been updated or its members changed',
        'doc_url': 'https://api.slack.com/events/subteam_updated',
        'example_body': None,
    },
    'team_domain_change': {
        'description': 'The workspace domain has changed',
        'doc_url': 'https://api.slack.com/events/team_domain_change',
        'example_body': {
            'domain': 'my',
            'type': 'team_domain_change',
            'url': 'https://my.slack.com',
        },
    },
    'team_join': {
        'description': 'A new member has joined',
        'doc_url': 'https://api.slack.com/events/team_join',
        'example_body': {'type': 'team_join', 'user': {}},
    },
    'team_migration_started': {
        'description': 'The workspace is being migrated between servers',
        'doc_url': 'https://api.slack.com/events/team_migration_started',
        'example_body': None,
    },
    'team_plan_change': {
        'description': 'The account billing plan has changed',
        'doc_url': 'https://api.slack.com/events/team_plan_change',
        'example_body': {
            'can_add_ura': False,
            'paid_features': ['feature1', 'feature2'],
            'plan': 'std',
            'type': 'team_plan_change',
        },
    },
    'team_pref_change': {
        'description': 'A preference has been updated',
        'doc_url': 'https://api.slack.com/events/team_pref_change',
        'example_body': {
            'name': 'slackbot_responses_only_admins',
            'type': 'team_pref_change',
            'value': True,
        },
    },
    'team_profile_change': {
        'description': 'The workspace profile fields have been updated',
        'doc_url': 'https://api.slack.com/events/team_profile_change',
        'example_body': None,
    },
    'team_profile_delete': {
        'description': 'The workspace profile fields have been deleted',
        'doc_url': 'https://api.slack.com/events/team_profile_delete',
        'example_body': None,
    },
    'team_profile_reorder': {
        'description': 'The workspace profile fields have been reordered',
        'doc_url': 'https://api.slack.com/events/team_profile_reorder',
        'example_body': None,
    },
    'team_rename': {
        'description': 'The workspace name has changed',
        'doc_url': 'https://api.slack.com/events/team_rename',
        'example_body': {
            'name': 'New Team Name Inc.',
            'type': 'team_rename',
        },
    },
    'user_change': {
        'description': "A member's data has changed",
        'doc_url': 'https://api.slack.com/events/user_change',
        'example_body': {'type': 'user_change', 'user': {}},
    },
    'user_typing': {
        'description': 'A channel member is typing a message',
        'doc_url': 'https://api.slack.com/events/user_typing',
        'example_body': {
            'channel': 'C02ELGNBH',
            'type': 'user_typing',
            'user': 'U024BE7LH',
        },
    },
}
