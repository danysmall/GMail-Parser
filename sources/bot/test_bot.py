"""."""
from telethon import TelegramClient, events
import asyncio


async def main():
    """."""
    API_ID = 7212719
    API_HASH = '3778859a51ffe2951f3abe886d03d0f1'
    BOT_TOKEN = '5238448407:AAFC6Y2qesRNmXgbzTQ3KbvRpLaHR24jgmE'
    BOT_SESSION_NAME = 'bot-session'

    client = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)
    client.start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage)
    async def handler(event):
        event.reply(event)

    client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
