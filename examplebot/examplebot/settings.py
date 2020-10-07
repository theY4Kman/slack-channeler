import os

SECRET_KEY = 'absolutely-secret'
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'channels',
    'slack_channeler',
]

ASGI_APPLICATION = 'examplebot.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                (os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', 6379))
            ],
        },
    },
}


SLACK_CHANNELER_TOKEN = os.environ['SLACK_CHANNELER_TOKEN']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
        },
    },
}
