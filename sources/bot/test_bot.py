"""."""
from telethon import TelegramClient, events
import asyncio


API_ID = 7212719
API_HASH = '3778859a51ffe2951f3abe886d03d0f1'
BOT_TOKEN = '5238448407:AAFC6Y2qesRNmXgbzTQ3KbvRpLaHR24jgmE'
BOT_SESSION_NAME = 'bot-session'

class Test():

    def __init__(self):
        self.client = TelegramClient(BOT_SESSION_NAME, API_ID, API_HASH)

    async def _run(self):
        await self.client.start(bot_token=BOT_TOKEN)
        print('bot started')
        await self.client.run_until_disconnected()

    def run(self):
        asyncio.run(self._run())


if __name__ == '__main__':
    t = Test()
    t.run()
