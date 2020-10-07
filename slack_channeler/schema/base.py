from typing import Type, Dict, TYPE_CHECKING

import inflection
from marshmallow import Schema, SchemaOpts, post_load, INCLUDE

from slack_channeler import events

if TYPE_CHECKING:
    from slack_channeler import SlackChannelerConsumer


class EventOpts(SchemaOpts):
    def __init__(self, meta, ordered: bool = False):
        super().__init__(meta, ordered)
        self.model = getattr(meta, 'model', None)
        self.event_type = getattr(meta, 'event_type', None)


class BaseEventSchema(Schema):
    OPTIONS_CLASS = EventOpts
    opts: EventOpts

    class Meta:
        unknown = INCLUDE

    def __init__(self, *,
                 consumer: 'SlackChannelerConsumer' = None,
                 context: Dict = None,
                 **kwargs):
        context = {} if context is None else context

        if 'consumer' in context:
            pass
        elif consumer is not None:
            context['consumer'] = consumer
        else:
            raise ValueError('A SlackChannelConsumer must be passed with consumer=consumer, '
                             'or inside the context as context=dict(consumer=consumer)')

        kwargs.setdefault('unknown', INCLUDE)
        super().__init__(context=context, **kwargs)

    @property
    def consumer(self):
        return self.context['consumer']

    @post_load
    def hydrate(self, data, **kwargs):
        model_cls = self.get_model_class()
        instance = model_cls(consumer=self.consumer, **data)
        return instance

    def get_model_class(self) -> Type[events.BaseEvent]:
        if model := self.opts.model:
            return model
        else:
            event_type = self.get_event_type()
            return events.EVENT_CLASSES_BY_TYPE.get(event_type)

    def get_event_type(self) -> str:
        if event_type := self.opts.event_type:
            return event_type
        else:
            return self.guess_event_type()

    @classmethod
    def guess_event_type(cls) -> str:
        """Guess the Slack event type from the Schema class name

        >>> class MessageSchema(BaseEventSchema): pass
        >>> MessageSchema.guess_event_type()
        'message'
        >>> class TeamProfileDeleteSchema(BaseEventSchema): pass
        >>> TeamProfileDeleteSchema.guess_event_type()
        'team_profile_delete'
        """
        name = cls.__name__
        if name.endswith('Schema'):
            name = name[:-len('Schema')]

        guessed_type = inflection.underscore(name.replace('_', '.'))
        return guessed_type
