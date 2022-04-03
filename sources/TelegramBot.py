"""Module implements telegram bot behavior."""
from telethon import TelegramClient, events
import inline
import asyncio
from threading import Thread

import scrapper


class ThreadWithReturn(Thread):
    """."""
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

    def get_result(self):
        return self._return


API_ID = 7212719
API_HASH = '3778859a51ffe2951f3abe886d03d0f1'
BOT_TOKEN = '5175209485:AAEmzJi_H9UXFh-LYatrXGURXcswjy9Wg0I'
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

        self._callback_dict = dict()
        self._threads = list()
        self._get_whitelist_file()

    async def _async_run(self: 'BotFather'):
        print('Started')
        self._session = TelegramClient(
            self._session_name, self._api_id, self._api_hash)
        self._session.session.set_dc(2, '149.154.167.50', 443)
        await self._session.start(bot_token=self._bot_token)
        print('Session completed')

        @self._session.on(events.NewMessage(pattern='/start'))
        async def _command_start(event):
            uid = event.original_update.message.peer_id.user_id
            if not self._is_in_whitelist(uid):
                return
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
            uid = event.original_update.message.peer_id.user_id
            if not self._is_in_whitelist(uid):
                return
            str = ''
            if len(self._threads) == 0:
                str = 'Ни одного процесса сбора базы не запущено'
            else:
                for th in self._threads:
                    str += f'Процесс {th[0]} работает\n'
            await self._session.send_message(
                event.message.peer_id.user_id, str)

        @self._session.on(events.CallbackQuery)
        async def _callback_query(event):
            uid = event.original_update.message.peer_id.user_id
            if not self._is_in_whitelist(uid):
                return
            event_id = event.original_update.msg_id

            if event.data == b'date_start':
                self._callback_dict[event_id]['stage'] = 1
                await event.edit(
                    inline.INLINE_MESSAGES['input_day']['message'],
                    buttons=inline.INLINE_MESSAGES['input_day']['buttons'])

            elif event.data == b'date_end':
                self._callback_dict[event_id]['stage'] = 2
                await event.edit(
                    inline.INLINE_MESSAGES['input_day']['message'],
                    buttons=inline.INLINE_MESSAGES['input_day']['buttons'])

            elif event.data == b'start':
                self._callback_dict[event_id]['stage'] = 3

                if check_dates(
                    start_date=(
                        self._callback_dict[event_id]['day_start'],
                        self._callback_dict[event_id]['month_start'],
                        self._callback_dict[event_id]['year_start']),
                    end_date=(
                        self._callback_dict[event_id]['day_end'],
                        self._callback_dict[event_id]['month_end'],
                        self._callback_dict[event_id]['year_end']
                    )
                ):
                    await event.edit(inline.MESSAGES['base_begin'].format(
                        event_id))
                    await self._start_thread(event_id, event)
                else:
                    await event.edit('Что-то пошло не так!')

            elif not str(event.data).find('day') == -1:
                _, number = event.data.decode('utf-8').split(':')

                # if user choise was start date
                if self._callback_dict[event_id]['stage'] == 1:
                    self._callback_dict[event_id]['day_start'] = int(number)

                # if user choise was end date
                elif self._callback_dict[event_id]['stage'] == 2:
                    self._callback_dict[event_id]['day_end'] = int(number)

                await event.edit(
                    inline.INLINE_MESSAGES['input_month']['message'],
                    buttons=inline.INLINE_MESSAGES['input_month']['buttons'])

            elif not str(event.data).find('month') == -1:
                _, number = event.data.decode('utf-8').split(':')

                # if user choise was start date
                if self._callback_dict[event_id]['stage'] == 1:
                    self._callback_dict[event_id]['month_start'] = int(number)

                # if user choise was end date
                elif self._callback_dict[event_id]['stage'] == 2:
                    self._callback_dict[event_id]['month_end'] = int(number)

                await event.edit(
                    inline.INLINE_MESSAGES['input_year']['message'],
                    buttons=inline.INLINE_MESSAGES['input_year']['buttons'])

            elif not str(event.data).find('year') == -1:
                _, number = event.data.decode('utf-8').split(':')

                # if user choise was start date
                if self._callback_dict[event_id]['stage'] == 1:
                    self._callback_dict[event_id]['year_start'] = int(number)

                # if user choise was end date
                elif self._callback_dict[event_id]['stage'] == 2:
                    self._callback_dict[event_id]['year_end'] = int(number)

                await event.edit(
                    inline.INLINE_MESSAGES['start']['message'].format(
                        day_start=self._callback_dict[event_id]['day_start'],
                        month_start=self._callback_dict[event_id]['month_start'],
                        year_start=self._callback_dict[event_id]['year_start'],
                        day_end=self._callback_dict[event_id]['day_end'],
                        month_end=self._callback_dict[event_id]['month_end'],
                        year_end=self._callback_dict[event_id]['year_end'],
                    ),
                    buttons=inline.INLINE_MESSAGES['start']['buttons'],
                    parse_mode='html')

        @self._session.on(events.NewMessage(pattern='/users'))
        async def _get_white_list(event):
            uid = event.original_update.message.peer_id.user_id
            if not self._is_in_whitelist(uid):
                return
            result = ''
            for index, user in enumerate(self._whitelist):
                result += f'{index + 1}. @{user[0]}\n'
            await self._session.send_message(uid, result)

        @self._session.on(events.NewMessage(pattern='/adduser'))
        async def _add_new_user(event):
            sender_id = event.original_update.message.peer_id.user_id
            if not self._is_in_whitelist(sender_id):
                return
            input = event.original_update.message.message.split()[1:]
            if len(input) > 1 or not input[0][0] == '@':
                await self._session.send_message(
                    sender_id,
                    'Команда введена неправильно. Шаблон команды: '
                    + '/adduser @username')
                return

            try:
                user = await self._session.get_entity(input[0])
                self._whitelist.append((input[0][1:], user.id))
                self._update_whitelist_file()
                await self._session.send_message(
                    sender_id,
                    f'Пользователь {input[0]} успешно добавлен'
                )
            except ValueError:
                await self._session.send_message(
                    sender_id, 'Такого пользователя не найдено')

        @self._session.on(events.NewMessage(pattern='/deleteuser'))
        async def _delete_user(event):
            uid = event.original_update.message.peer_id.user_id
            if not self._is_in_whitelist(uid):
                return
            sender_id = event.original_update.message.peer_id.user_id
            input = event.original_update.message.message.split()[1:]
            if len(input) > 1 or not input[0][0] == '@':
                await self._session.send_message(
                    sender_id,
                    'Команда введена неправильно. Шаблон команды: '
                    + '/deleteuser @username')
                return

            uindex = None
            for index, item in enumerate(self._whitelist):
                if input[0][1:] == item[0]:
                    uindex = index
                    break

            success_msg = None
            if uindex is not None:
                self._whitelist.pop(uindex)
                self._update_whitelist_file()
                success_msg = f'Пользователь {input[0]} успешно удален'
            else:
                success_msg = f'Пользователь {input[0]} не найден'
            await self._session.send_message(sender_id, success_msg)

        @self._session.on(events.NewMessage())
        async def _any_message(event):
            print(f'Event {event.original_update}')

        await self._session.run_until_disconnected()

    def _update_whitelist_file(self):
        with open('assets/whitelist.txt', 'w', encoding='utf-8') as file:
            for item in self._whitelist:
                file.write(f'{item[0]}:{item[1]}')

    def _get_whitelist_file(self):
        self._whitelist = list()
        with open('assets/whitelist.txt', 'r', encoding='utf-8') as file:
            for line in file:
                uname, uid = line.split(':')
                # print(uid, uname)
                self._whitelist.append((uname, int(uid)))

    def _is_in_whitelist(self: 'BotFather', user_id) -> bool:
        for item in self._whitelist:
            if item[1] == user_id:
                return True
        return False

    async def _start_thread(self: 'BotFather', event_id, event):
        thread = ThreadWithReturn(
            target=self._get_base, args=(event_id, event), name=event_id)
        thread.start()
        self._threads.append((event_id, thread))

        while thread.is_alive():
            await asyncio.sleep(30)
        result = thread.get_result()
        print(f'Thread: {result}')

        await self._send_base(result, event)
        for th in self._threads:
            if th[0] == event_id:
                self._threads.remove(th)
                break
        # return thread.result

    def _get_base(self: 'BotFather', event_id, event):
        mails = scrapper.GMail(
            token_filename=self._token_filename,
            creds_filename=self._creds_filename)

        f_name = mails.get_file(
            from_date=(
                self._callback_dict[event_id]['day_start'],
                self._callback_dict[event_id]['month_start'],
                self._callback_dict[event_id]['year_start']),
            to_date=(
                self._callback_dict[event_id]['day_end'],
                self._callback_dict[event_id]['month_end'],
                self._callback_dict[event_id]['year_end']
            ),
            message_id=str(event_id),
        )

        print(f'Send Base {f_name}')
        return f_name
        # asyncio.run(self._send_base(f_name, event))

    async def _send_base(self: 'BotFather', f_name, event):
        print('Send Base function')
        print(event)
        if f_name is None:
            print('base failed')
            await event.edit(inline.MESSAGES['base_failed'])
        else:
            print('Edit')
            await event.edit(inline.MESSAGES['base_end'].format(
                f_name.split('/')[1]))
            print('Upload')
            f_upd = await self._session.upload_file(f_name)
            print('Send file')
            await self._session.send_file(
                event.original_update.user_id,
                file=f_upd)

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
