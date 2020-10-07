import logging

from slack_channeler import SlackChannelerConsumer, events

logger = logging.getLogger(__name__)


class SlackConsumer(SlackChannelerConsumer):
    print_events = True

    async def slack_message(self, message: events.Message):
        text = message.text
        if text.startswith('!'):
            command, *args = text[1:].split(' ')
            if command == 'leave':
                await message.reply('Leaving...')
                await message.channel.leave()
            elif command == 'react':
                emoji = args[0] if args else '+1'
                await message.add_reaction(emoji)
            else:
                await message.reply(f'Unknown command {command}')
        else:
            await message.reply(message.text or 'i did not hear anything')

    async def slack_reaction_added(self, event: events.ReactionAdded):
        await event.item.add_reaction(event.reaction)
