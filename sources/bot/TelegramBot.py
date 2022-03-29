"""Module implements telegram bot behavior."""
from telethon import TelegramClient, events
import inline
import asyncio

import scrapper


API_ID = 7212719
API_HASH = '3778859a51ffe2951f3abe886d03d0f1'
BOT_TOKEN = '5238448407:AAFC6Y2qesRNmXgbzTQ3KbvRpLaHR24jgmE'
BOT_SESSION_NAME = 'bot-session'


class BotFather():
    """Implement telegram bot behavior."""

    def __init__(
        self: 'BotFather',
        api_id: int = API_ID,
        api_hash: str = API_HASH,
        session_name: str = BOT_SESSION_NAME,
        bot_token: str = BOT_TOKEN,
        token_filename: str = None,
        creds_filename: str = None
    ) -> None:
        """Initialize bot object."""
        self._api_id = api_id
        self._api_hash = api_hash
        self._session_name = session_name
        self._bot_token = bot_token

        self._token_filename = token_filename
        self._creds_filename = creds_filename

        self._session = TelegramClient(
            self._session_name,
            self._api_id,
            self._api_hash)

        self._session.session.set_dc(2, '149.154.167.50', 443)

        self._callback_dict = dict()

    async def _async_run(self: 'BotFather'):
        await self._session.start(bot_token=self._bot_token)

        @self._session.on(events.NewMessage(pattern='/start'))
        async def _command_start(event):
            # Send </start> command message
            message = await self._session.send_message(
                event.message.peer_id.user_id,
                inline.INLINE_MESSAGES['start']['message'].format(
                    day_start='01', month_start='01', year_start='1970',
                    day_end='01', month_end='01', year_end='1970'),
                buttons=inline.INLINE_MESSAGES['start']['buttons'],
                parse_mode='html')

            if message.id not in self._callback_dict:
                self._callback_dict[message.id] = {
                    'message': message,
                    'stage': 0,
                    'day_start': None,
                    'month_start': None,
                    'year_start': None,
                    'day_end': None,
                    'month_end': None,
                    'year_end': None
                }

        @self._session.on(events.NewMessage(pattern='/info'))
        async def _get_callback_dict(event):
            print(self._callback_dict)

        # @self._session.on(events.CallbackQuery)
        # async def _callback_query(event):
        #     # print('CALLBACK\n', event)
        #     # await event.edit('Спасибо за клик!')
        #     event_id = event.original_update.msg_id
        #     print(event)
        #
        #     if event.data == b'date_start':
        #         self._callback_dict[event_id]['stage'] = 1
        #         await event.edit(
        #             inline.INLINE_MESSAGES['input_day']['message'],
        #             buttons=inline.INLINE_MESSAGES['input_day']['buttons'])
        #
        #     elif event.data == b'date_end':
        #         self._callback_dict[event_id]['stage'] = 2
        #         await event.edit(
        #             inline.INLINE_MESSAGES['input_day']['message'],
        #             buttons=inline.INLINE_MESSAGES['input_day']['buttons'])
        #
        #     elif event.data == b'start':
        #         self._callback_dict[event_id]['stage'] = 3
        #
        #         if check_dates(
        #             start_date=(
        #                 self._callback_dict[event_id]['day_start'],
        #                 self._callback_dict[event_id]['month_start'],
        #                 self._callback_dict[event_id]['year_start']),
        #             end_date=(
        #                 self._callback_dict[event_id]['day_end'],
        #                 self._callback_dict[event_id]['month_end'],
        #                 self._callback_dict[event_id]['year_end']
        #             )
        #         ):
        #             await event.edit(inline.MESSAGES['base_begin'].format(
        #                 event_id))
        #
        #             f_name = self._get_base(event_id)
        #             if f_name is None:
        #                 await event.edit(inline.MESSAGES['base_failed'])
        #             else:
        #                 f_upd = await self._session.upload_file(f_name)
        #                 await event.edit(inline.MESSAGES['base_end'].format(
        #                     f_name.split('/')[1]))
        #                 await self._session.send_file(
        #                     event.original_update.user_id,
        #                     file=f_upd)
        #         else:
        #             await event.edit('Что-то пошло не так!')
        #
        #     elif not str(event.data).find('day') == -1:
        #         _, number = event.data.decode('utf-8').split(':')
        #
        #         # if user choise was start date
        #         if self._callback_dict[event_id]['stage'] == 1:
        #             self._callback_dict[event_id]['day_start'] = int(number)
        #
        #         # if user choise was end date
        #         elif self._callback_dict[event_id]['stage'] == 2:
        #             self._callback_dict[event_id]['day_end'] = int(number)
        #
        #         await event.edit(
        #             inline.INLINE_MESSAGES['input_month']['message'],
        #             buttons=inline.INLINE_MESSAGES['input_month']['buttons'])
        #
        #     elif not str(event.data).find('month') == -1:
        #         _, number = event.data.decode('utf-8').split(':')
        #
        #         # if user choise was start date
        #         if self._callback_dict[event_id]['stage'] == 1:
        #             self._callback_dict[event_id]['month_start'] = int(number)
        #
        #         # if user choise was end date
        #         elif self._callback_dict[event_id]['stage'] == 2:
        #             self._callback_dict[event_id]['month_end'] = int(number)
        #
        #         await event.edit(
        #             inline.INLINE_MESSAGES['input_year']['message'],
        #             buttons=inline.INLINE_MESSAGES['input_year']['buttons'])
        #
        #     elif not str(event.data).find('year') == -1:
        #         _, number = event.data.decode('utf-8').split(':')
        #
        #         # if user choise was start date
        #         if self._callback_dict[event_id]['stage'] == 1:
        #             self._callback_dict[event_id]['year_start'] = int(number)
        #
        #         # if user choise was end date
        #         elif self._callback_dict[event_id]['stage'] == 2:
        #             self._callback_dict[event_id]['year_end'] = int(number)
        #
        #         await event.edit(
        #             inline.INLINE_MESSAGES['start']['message'].format(
        #                 day_start=self._callback_dict[event_id]['day_start'],
        #                 month_start=self._callback_dict[event_id]['month_start'],
        #                 year_start=self._callback_dict[event_id]['year_start'],
        #                 day_end=self._callback_dict[event_id]['day_end'],
        #                 month_end=self._callback_dict[event_id]['month_end'],
        #                 year_end=self._callback_dict[event_id]['year_end'],
        #             ),
        #             buttons=inline.INLINE_MESSAGES['start']['buttons'],
        #             parse_mode='html')

        @self._session.on(events.NewMessage())
        async def _any_message(event):
            pass

        await self._session.run_until_disconnected()

    def _get_base(self: 'BotFather', event_id):
        mails = scrapper.GMail(
            token_filename=self._token_filename,
            creds_filename=self._creds_filename)

        return mails.get_file(
            from_date=(
                self._callback_dict[event_id]['day_start'],
                self._callback_dict[event_id]['month_start'],
                self._callback_dict[event_id]['year_start']),
            to_date=(
                self._callback_dict[event_id]['day_end'],
                self._callback_dict[event_id]['month_end'],
                self._callback_dict[event_id]['year_end']
            ),
            message_id=str(event_id)
        )

    def run(self: 'BotFather'):
        """Run bot until disconnect."""
        asyncio.run(self._async_run())

    async def _async_stop(self: 'BotFather'):
        await self._session.disconnect()

    def stop(self: 'BotFather'):
        """Close bot connection."""
        asyncio.run(self._async_stop())


def check_dates(
    start_date: tuple[int, int, int] = None,
    end_date: tuple[int, int, int] = None
) -> bool:
    """Check two dates for first is less that second.

    -------------------------------------------------
    • Returns <True> if start_date < end_date
    • Returns <False> if start_date > end_date
    """
    try:
        temp = [snd - fst for fst, snd in zip(start_date, end_date)]
        if (temp[0] + temp[1] * 30 + temp[2] * 365) >= 0:
            return True
        return False
    except TypeError:
        return False


if __name__ == '__main__':
    try:
        bot = BotFather(
            token_filename='assets/token.json',
            creds_filename='assets/credentials.json')
        bot.run()

    except KeyboardInterrupt:
        print('Program exit by pressed ^C')

    finally:
        bot.stop()
