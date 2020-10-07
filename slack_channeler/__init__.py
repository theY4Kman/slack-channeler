from .version import *

from .consumers import SlackChannelerConsumer
from .objects import (
    Message,
)

default_app_config = 'slack_channeler.apps.SlackChannelerAppConfig'
