import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text('Привет!!! Я - бот от КнигаПоиска!\n'
                                    'Как я могу вам помочь?')


async def help_command(update, context):
    await update.message.reply_text('Помощь уже в пути!')


def main():
    TOKEN = '6192417970:AAG5Jb2pJVSGQvlW8LGVOGOZCI82D2qeFSU'
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.run_polling()


if __name__ == '__main__':
    main()