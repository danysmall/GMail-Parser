"""Main file of bot."""

import bot.TelegramBot


if __name__ == '__main__':
    try:
        bot = bot.TelegramBot.BotFather(
            token_filename='assets/token.json',
            creds_filename='assets/credentials.json')
        bot.run()

    except KeyboardInterrupt:
        print('Program exit by pressed ^C')

    finally:
        bot.stop()
