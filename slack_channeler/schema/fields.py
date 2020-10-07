from datetime import datetime
from typing import Type, TYPE_CHECKING, Optional, Union

#: Expose all fields from this module, so it may be used as a drop-in replacement
from marshmallow.fields import *
from marshmallow import fields

from slack_channeler import objects
from slack_channeler.schema.base import BaseEventSchema

if TYPE_CHECKING:
    from slack_channeler import SlackChannelerConsumer


class ParentConsumerMixin:
    parent: BaseEventSchema

    @property
    def consumer(self) -> 'SlackChannelerConsumer':
        return self.parent.consumer


class ObjectId(ParentConsumerMixin, fields.String):
    """An object represented by its ID"""

    model: Type[objects.BaseObject]
    id_field: str

    def __init__(self, model: Type[objects.BaseObject], *, id_field: str = 'id', **kwargs):
        self.model = model
        self.id_field = id_field
        super().__init__(**kwargs)

    def _serialize(self, value, attr, obj, **kwargs) -> Optional[str]:
        if value:
            return getattr(value, self.id_field, None)

    def _deserialize(self, value, attr, data, **kwargs) -> objects.Channel:
        object_id = super()._deserialize(value, attr, data, **kwargs)
        fields = {
            'consumer': self.consumer,
            self.id_field: object_id
        }
        return self.model(**fields)


class Object(ParentConsumerMixin, fields.Dict):
    """An object represented by a dict of its fields"""

    model: Type[objects.BaseObject]

    def __init__(self, model: Type[objects.BaseObject], **kwargs):
        self.model = model
        super().__init__(**kwargs)

    def _deserialize(self, value, attr, data, **kwargs) -> objects.Channel:
        fields = {
            **super()._deserialize(value, attr, data, **kwargs),
            'consumer': self.consumer,
        }
        return self.model(**fields)


class TimestampStr(fields.String):
    """A datetime represented by a string of its UTC timestamp w/ microsecond precision

    This type is used by event_ts fields.
    """

    def _serialize(self, value: Union[datetime, str], attr, obj, **kwargs) -> Optional[str]:
        if value:
            if isinstance(value, datetime):
                value = value.timestamp()
            return str(value)

    def _deserialize(self, value, attr, data, **kwargs) -> Optional[datetime]:
        if value:
            return datetime.utcfromtimestamp(float(value))
