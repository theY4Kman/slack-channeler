import logging
import os

import click

from .server import ChannelsSlackClient

logger = logging.getLogger(__name__)


@click.command()
def main():
    """Relay Slack real-time messages to and from Django Channels v2
    """
    slack_token = os.environ['SLACK_CHANNELER_TOKEN']
    rtm_client = ChannelsSlackClient(token=slack_token)

    rtm_client.start()


if __name__ == '__main__':
    main()
