from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING, Union

from dataclassy import dataclass
from slack.web.classes import extract_json
from slack.web.classes.blocks import Block

from slack_channeler.util.parse import parse_timestamp

if TYPE_CHECKING:
    from slack_channeler import SlackChannelerConsumer

__all__ = [
    'Message',
]

NOTSET = object()


class FieldNotLoaded(AttributeError):
    """The accessed field has not been loaded, yet.

    To rectify this, call `await parent.load_info()` and perform attribute
    access again.
    """


class loadable_property:
    """Descriptor raising FieldNotLoaded on access until value is set
    """
    def __init__(self, default=NOTSET):
        self.default = default

    def get_loaded_info(self, instance) -> Dict['loadable_property', Any]:
        if loaded_info := getattr(instance, '_loaded_info', None):
            return loaded_info

        instance._loaded_info = {}
        return instance._loaded_info

    def __get__(self, instance, owner):
        if instance is None:
            return self

        loaded_info = self.get_loaded_info(instance)
        value = loaded_info.get(self, self.default)

        if value is NOTSET:
            raise FieldNotLoaded(
                'Field is not loaded, yet. Call `await parent.load_info()` and '
                'repeat attribute access.')

        return value

    def __set__(self, instance, value):
        loaded_info = self.get_loaded_info(instance)
        loaded_info[self] = value

    def __delete__(self, instance):
        loaded_info = self.get_loaded_info(instance)
        loaded_info[self] = NOTSET


class LoadableInfoMixin:
    """Allow manual async loading of properties

    This mixin allows Objects referenced only by their ID to become later
    enriched when more info about them is desired.

    Class attributes declared with `attr = loadable_property()` will raise
    FieldNotLoaded on access (`instance.attr`), until `await instance.load_info()`
    is called.

    Alternatively, one may use `(await instance).attr` to perform loading. Note
    that calling `await instance` twice will only call `await instance.load_info()`
    once. If the instance's data is stale, `await instance.load_info()` may be
    called manually to force a refresh.
    """

    def __await__(self):
        if not getattr(self, '_info_loaded', False):
            yield from self.load_info().__await__()
            self._info_loaded = True
        return self

    async def load_info(self):
        """Load additional info about this object

        When implementing this method, loadable_property() attributes may be
        set directly. For example:

            class MyObject(LoadableInfoMixin, BaseObject):
                id: str
                description: str = loadable_property()

                async def load_info(self):
                    info = await get_info(self.id)
                    self.description = info['description']
        """
        raise NotImplementedError


@dataclass
class BaseObject:
    consumer: 'SlackChannelerConsumer'


class Bot(LoadableInfoMixin, BaseObject):
    id: str
    name: str = loadable_property()

    deleted: bool = loadable_property()
    updated: datetime = loadable_property()

    user: 'User' = loadable_property()
    user_id: str = loadable_property()
    app_id: str = loadable_property()

    icons: Dict[str, str] = loadable_property()

    async def info(self, **fields) -> Dict[str, Any]:
        return await self.consumer.api_call(
            'bots.info',
            bot=self.id,
            **fields,
        )

    async def load_info(self):
        info = await self.info()

        self.name = info['name']

        self.deleted = info['deleted']
        self.updated = parse_timestamp(info['updated'])

        self.user = User(id=info['user_id'])
        self.user_id = info['user_id']
        self.app_id = info['app_id']

        self.icons = info['icons']


class ChannelTopic(BaseObject):
    channel: 'Channel'

    value: str
    creator: 'User'
    last_set: datetime

    def __init__(self):
        if isinstance(self.last_set, (int, float)):
            self.last_set = parse_timestamp(self.last_set)

        if isinstance(self.creator, str):
            self.creator = User(consumer=self.consumer, id=self.creator)


class ChannelPurpose(ChannelTopic):
    pass


class Channel(LoadableInfoMixin, BaseObject):
    id: str

    name: str = loadable_property()
    name_normalized: str = loadable_property()
    previous_names: List[str] = loadable_property()

    is_channel: bool = loadable_property(True)
    is_group: bool = loadable_property(False)
    is_im: bool = loadable_property(False)

    is_archived: bool = loadable_property()
    is_general: bool = loadable_property()
    is_read_only: bool = loadable_property()
    is_shared: bool = loadable_property()
    is_ext_shared: bool = loadable_property()
    is_org_shared: bool = loadable_property()
    is_pending_ext_shared: bool = loadable_property()
    is_member: bool = loadable_property()
    is_private: bool = loadable_property()
    is_mpim: bool = loadable_property()

    created: datetime = loadable_property()
    creator: 'User' = loadable_property()

    # TODO: make this a Message?
    last_read: str = loadable_property()

    topic: ChannelTopic = loadable_property()
    purpose: ChannelPurpose = loadable_property()

    num_members: int = loadable_property()
    locale: str = loadable_property()

    unlinked: int = loadable_property()

    def __str__(self):
        return self.id

    async def load_info(self):
        info = await self.info(include_locale=True, include_num_members=True)

        self.name = info['name']
        self.name_normalized = info['name_normalized']
        self.previous_names = info['previous_names']

        self.is_channel = info['is_channel']
        self.is_group = info['is_group']
        self.is_im = info['is_im']

        self.is_archived = info['is_archived']
        self.is_general = info['is_general']
        self.is_read_only = info['is_read_only']
        self.is_shared = info['is_shared']
        self.is_ext_shared = info['is_ext_shared']
        self.is_org_shared = info['is_org_shared']
        self.is_pending_ext_shared = info['is_pending_ext_shared']
        self.is_member = info['is_member']
        self.is_private = info['is_private']
        self.is_mpim = info['is_mpim']

        self.created = parse_timestamp(info['created'])
        self.creator = User(consumer=self.consumer, id=info['creator'])

        self.last_read = info['last_read']

        self.topic = ChannelTopic(consumer=self.consumer, **info['topic'])
        self.purpose = ChannelPurpose(consumer=self.consumer, **info['purpose'])

        self.num_members = info['num_members']
        self.locale = info['locale']

        self.unlinked = info['unlinked']

    async def info(self, *,
                   include_locale: bool = False,
                   include_num_members: bool = True,
                   **fields,
                   ) -> Dict[str, Any]:
        """Retrieve info about the channel
        """
        return await self.consumer.api_call(
            'conversations.info',
            channel=self.id,
            include_locale=include_locale,
            include_num_members=include_num_members,
            **fields,
        )

    async def send_me_message(self, text: str, **fields):
        """Send a /me message to the channel
        """
        return await self.consumer.api_call(
            'chat_meMessage',
            channel=self.id,
            text=text,
            **fields,
        )

    async def send_message(self, text: str, **fields):
        """Send regular chat message to the channel
        """
        return await self.consumer.send_message(
            channel=self.id,
            text=text,
            **fields,
        )

    async def send_in_thread(self, ts: str, text: str, **fields):
        """Reply to or create a thread off a message
        """
        return await self.send_message(
            thread_ts=ts,
            text=text,
            **fields,
        )

    async def delete_message(self, ts: str, **fields):
        """Delete a message
        """
        return await self.consumer.api_call(
            'chat.delete',
            channel=self.id,
            ts=ts,
            **fields,
        )

    async def leave(self, **fields):
        """Leave the channel

        NOTE: bot users may not be able to perform this action
        """
        return await self.consumer.api_call(
            'conversations.leave',
            channel=self.id,
            **fields,
        )

    async def add_reaction(self, ts: str, name: str, **fields):
        """Add a reaction to a message in the channel

        :param ts:
            Timestamp of the message to add the reaction to

        :param name:
            Name of the reaction (emoji)

        """
        return await self.consumer.api_call(
            'reactions.add',
            channel=self.id,
            timestamp=ts,
            name=name,
            **fields,
        )


class User(LoadableInfoMixin, BaseObject):
    id: str

    updated: datetime = loadable_property()
    deleted: bool = loadable_property()

    team_id: str = loadable_property()

    name: str = loadable_property()
    real_name: str = loadable_property()
    profile: 'UserProfile' = loadable_property()

    color: str = loadable_property()

    tz: str = loadable_property()
    tz_label: str = loadable_property()
    tz_offset: int = loadable_property()

    is_admin: bool = loadable_property()
    is_owner: bool = loadable_property()
    is_primary_owner: bool = loadable_property()
    is_restricted: bool = loadable_property()
    is_ultra_restricted: bool = loadable_property()
    is_bot: bool = loadable_property()
    is_app_user: bool = loadable_property()
    has_2fa: bool = loadable_property()

    def __str__(self):
        return self.id

    async def info(self, **fields) -> Dict[str, Any]:
        return await self.consumer.api_call('users.info', user=self.id, **fields)

    async def load_info(self):
        info = await self.info()

        self.deleted = info['deleted']
        self.updated = parse_timestamp(info['updated'])

        self.team_id = info['team_id']

        self.name = info['name']
        self.real_name = info['real_name']
        self.profile = UserProfile(consumer=self.consumer, user=self, **info['profile'])

        self.color = info['color']

        self.tz = info['tz']
        self.tz_label = info['tz_label']
        self.tz_offset = info['tz_offset']

        self.is_admin = info['is_admin']
        self.is_owner = info['is_owner']
        self.is_primary_owner = info['is_primary_owner']
        self.is_restricted = info['is_restricted']
        self.is_ultra_restricted = info['is_ultra_restricted']
        self.is_bot = info['is_bot']
        self.is_app_user = info['is_app_user']
        self.has_2fa = info['has_2fa']


class UserProfile(BaseObject):
    user: User

    avatar_hash: str = None
    status_text: str = None
    status_emoji: str = None
    real_name: str = None
    display_name: str = None
    real_name_normalized: str = None
    display_name_normalized: str = None
    email: str = None
    image_original: str = None
    image_24: str = None
    image_32: str = None
    image_48: str = None
    image_72: str = None
    image_192: str = None
    image_512: str = None
    team: str = None


class Message(LoadableInfoMixin, BaseObject):
    type: str = 'message'
    subtype: str = None

    ts: str
    channel: Channel

    user: User = None
    text: str = None
    thread_ts: str = None

    # TODO: create objects for these
    blocks: List[Dict] = None
    edited: Dict[str, Any] = None

    def __init__(self):
        if isinstance(self.channel, str):
            self.channel = Channel(consumer=self.consumer, id=self.channel)
        if isinstance(self.user, str):
            self.user = User(consumer=self.consumer, id=self.user)

    async def info(self, **fields) -> Dict[str, Any]:
        res = await self.consumer.api_call(
            'conversations.history',
            channel=self.channel.id,
            latest=self.ts,
            inclusive=True,
            limit=1,
            **fields,
        )
        if history := res['messages']:
            return history[0]

    async def load_info(self):
        info = await self.info()

        if 'user' in info:
            info['user'] = User(consumer=self.consumer, id=info['user'])
        if 'channel' in info:
            info['channel'] = Channel(consumer=self.consumer, id=info['channel'])

        for field, value in info.items():
            setattr(self, field, value)

    @property
    def is_in_thread(self):
        return bool(self.thread_ts)

    async def reply_channel(self, text: str, **fields):
        """Send a message in the channel this message is in
        """
        return await self.channel.send_message(text=text, **fields)

    async def reply_thread(self, text: str, **fields):
        """Send a message in the thread this message is in, or start a thread
        """
        thread_ts = self.thread_ts or self.ts
        return await self.channel.send_in_thread(ts=thread_ts, text=text, **fields)

    async def reply(self, text: str, **fields):
        """Send a message in this message's thread, or channel if not in a thread
        """
        reply = self.reply_thread if self.is_in_thread else self.reply_channel
        return await reply(text, **fields)

    async def add_reaction(self, name: str, **fields):
        """Add a reaction (emoji) to this message
        """
        return await self.channel.add_reaction(ts=self.ts, name=name, **fields)

    async def delete(self, **fields):
        """Delete the message
        """
        return await self.channel.delete_message(ts=self.ts, **fields)


class DoNotDisturb(BaseObject):
    dnd_enabled: bool = None

    next_dnd_end_ts: datetime = None
    next_dnd_start_ts: datetime = None
    snooze_enabled: bool = None
    snooze_endtime: datetime = None

    def __init__(self):
        self.next_dnd_end_ts = parse_timestamp(self.next_dnd_end_ts)
        self.next_dnd_start_ts = parse_timestamp(self.next_dnd_start_ts)
        self.snooze_endtime = parse_timestamp(self.snooze_endtime)


class Team(LoadableInfoMixin, BaseObject):
    id: str

    name: str = loadable_property()

    domain: str = loadable_property()
    email_domain: str = loadable_property()

    icons: Dict[str, Union[str, bool]] = loadable_property()

    enterprise_id: str = loadable_property()
    enterprise_name: str = loadable_property()

    async def info(self, **fields) -> Dict[str, Any]:
        return await self.consumer.api_call(
            'team.info',
            team=self.id,
            **fields,
        )

    async def load_info(self):
        info = await self.info()

        for field, value in info.items():
            setattr(self, field, value)
