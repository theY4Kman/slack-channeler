from slack_channeler import events
from slack_channeler.schema.base import BaseEventSchema

__all__ = ['AccountsChangedSchema']


class AccountsChangedSchema(BaseEventSchema):
    class Meta:
        model = events.AccountsChanged
        event_type = 'accounts_changed'
