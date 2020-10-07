import sys

from django.conf import settings
from django.core.management import BaseCommand, CommandParser, CommandError

from slack_channeler.server import ChannelsSlackClient


class SlackChanneler(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--token', '-t',
            help='Slack API token to use '
                 '(if not specified, settings.SLACK_CHANNELER_TOKEN is used)',
        )

        parser.add_argument(
            '--print-events',
            action='store_true',
            default=False,
            help='Print all received Slack events to the console',
        )

        parser.add_argument(
            '--relay-self',
            action='store_true',
            default=False,
            help='Whether to forward events originating from the bot user',
        )

    def handle(self, *, token: str, print_events: bool, relay_self: bool, **options):
        if token is None:
            token = settings.SLACK_CHANNELER_TOKEN

        if not token:
            raise CommandError(
                'No token passed (with --token or -t), '
                'and settings.SLACK_CHANNELER_TOKEN not set')

        rtm_client = ChannelsSlackClient(
            token=token,
            print_events=print_events,
            relay_self=relay_self,
        )
        rtm_client.start()


Command = SlackChanneler


def main(argv=None):
    if argv is None:
        argv = sys.argv

    import django
    django.setup()

    return SlackChanneler().run_from_argv([
        argv[0],
        'slack_channeler',
        *argv[1:],
    ])


if __name__ == '__main__':
    main()
