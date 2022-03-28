"""."""
from telethon import TelegramClient, events
import asyncio

async def main():
    """."""
    API_ID = 7212719
    API_HASH = '3778859a51ffe2951f3abe886d03d0f1'
    BOT_TOKEN = '5238448407:AAFC6Y2qesRNmXgbzTQ3KbvRpLaHR24jgmE'
    BOT_SESSION_NAME = 'bot-session'

    bot = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)
    await bot.start(bot_token=BOT_TOKEN)

    @bot.on(events.NewMessage)
    async def handle(event):
        await event.reply('Hello')

    await bot.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
