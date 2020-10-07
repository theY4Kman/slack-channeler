from typing import Dict, Type, TYPE_CHECKING, Any

from .base import BaseEventSchema
from .events import *

if TYPE_CHECKING:
    from slack_channeler import SlackChannelerConsumer
    from slack_channeler.events import BaseEvent


SCHEMAS_BY_EVENT_TYPE: Dict[str, Type[BaseEventSchema]] = {
    schema_cls(consumer='dummy').get_event_type(): schema_cls
    for schema_cls in BaseEventSchema.__subclasses__()
}


def hydrate(
    event_type: str, /,
    consumer: 'SlackChannelerConsumer',
    data: Dict[str, Any],
    **fields,
) -> 'BaseEvent':
    schema_cls = SCHEMAS_BY_EVENT_TYPE.get(event_type)
    if schema_cls is None:
        raise ValueError(f'Unhandled event type {event_type}')

    schema = schema_cls(consumer=consumer)
    data = {**data, **fields}
    event = schema.load(data)
    return event
