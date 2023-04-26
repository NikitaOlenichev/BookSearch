import logging
from telegram.ext import Application, CommandHandler
import datetime
from requests import get

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

TOKEN = '6192417970:AAG5Jb2pJVSGQvlW8LGVOGOZCI82D2qeFSU'


async def start(update, context):
    greet = ''
    hi = {"hey": ('Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')}
    now = datetime.datetime.now()
    if now.hour > 4 and now.hour <= 12:
        greet = hi["hey"][0]
    if now.hour > 12 and now.hour <= 16:
        greet = hi["hey"][1]
    if now.hour > 16 and now.hour <= 24:
        greet = hi["hey"][2]
    if now.hour >= 0 and now.hour <= 4:
        greet = hi["hey"][3]
    await update.message.reply_text(f'{greet}!!! Я - бот от КнигаПоиска!\n'
                                    'Вот, что я умею:\n'
                                    '/start - для начала работы\n'
                                    '/search - расскажу вам основную информацию о книге\n'
                                    '/info - расскажу вам аннотацию по книге\n'
                                    '/genre - пришлю ссылку на страницу сайта с книгами\n'
                                    'нужного вам жанра\n'
                                    '/author - пришлю ссылку на страницу сайта с книгами\n'
                                    'нужного вам автора\n'
                                    '/read - покажу где можно почитать книгу\n'
                                    '/help - поддержка\n'
                                    'Пример: /команда название книги или жанр или автор.\n'
                                    'Что хотите узнать?')


async def help_command(update, context):
    await update.message.reply_text('Если у вас появились вопросы,\n'
                                    'напишите нам на электронную почту!\n'
                                    'Адрес электронной почты: b0oksea5ch_he1pers@yandex.ru')


async def search(update, context):
    if context.args != []:
        response = get(f'http://127.0.0.1:5000/api/book/{context.args[0]}')
        if response.status_code == 200:
            res = f"https://diamond-complex-gondola.glitch.me/search/1?title={context.args[0]}"
            response = get(f'http://127.0.0.1:5000/api/book/{context.args[0]}').json()
            await update.message.reply_text(f"Название: {response['book']['title']}\n"
                                            f"Оригинальное название: "
                                            f"{response['book']['orig_name']}\n"
                                            f"Автор: {response['book']['author']['name']}\n"
                                            f"Жанр: {response['book']['genre']['title']}\n"
                                            f"Год публикации: {response['book']['work_year']}\n"
                                            f"Ссылка на страницу сайта: {res}\n"
                                            f"Ссылка на фото: {response['book']['image']['link']}")
        else:
            await update.message.reply_text('К сожалению, я не знаю такую книгу!')
    else:
        await update.message.reply_text('Введите команду вот в таком виде:\n'
                                        '/search Название книги')


async def search_info(update, context):
    if context.args != []:
        response = get(f'http://127.0.0.1:5000/api/book/{context.args[0]}')
        if response.status_code == 200:
            res = f"https://diamond-complex-gondola.glitch.me/search/1?title={context.args[0]}"
            response = get(f'http://127.0.0.1:5000/api/book/{context.args[0]}').json()
            await update.message.reply_text(f"{response['book']['info']['info']}\n"
                                            f"Ссылка на страницу сайта: {res}")
        else:
            await update.message.reply_text('К сожалению, я не знаю такую книгу!')
    else:
        await update.message.reply_text('Введите команду вот в таком виде:\n'
                                        '/info Название книги')


async def genres_book(update, context):
    if context.args != []:
        res = f"https://diamond-complex-gondola.glitch.me/search/1?genre={context.args[0]}"
        await update.message.reply_text(f"Все книги в жанре {context.args[0]}\n"
                                        f"вы можете увидеть на нашем сайте!\n"
                                        f"Ссылка на страницу сайта: {res}")
    else:
        await update.message.reply_text('Введите команду вот в таком виде:\n'
                                        '/genre Название жанра')


async def authors_book(update, context):
    if context.args != []:
        res = f"https://diamond-complex-gondola.glitch.me/search/1?author={context.args[0]}"
        await update.message.reply_text(f"Все книги автора {context.args[0]}\n"
                                        f"вы можете увидеть на нашем сайте!\n"
                                        f"Ссылка на страницу сайта: {res}")
    else:
        await update.message.reply_text('Введите команду вот в таком виде:\n'
                                        '/author Автор')


async def read_book(update, context):
    if context.args != []:
        await update.message.reply_text(f"Книгу {context.args[0]} вы можете прочитать\n"
                                        f"по ссылке: "
                                        f"https://yandex.ru/search/?text={context.args[0]}+читать")
    else:
        await update.message.reply_text('Введите команду вот в таком виде:\n'
                                        '/read Название книги')


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('search', search))
    application.add_handler(CommandHandler('info', search_info))
    application.add_handler(CommandHandler('genre', genres_book))
    application.add_handler(CommandHandler('author', authors_book))
    application.add_handler(CommandHandler('read', read_book))
    application.run_polling()


if __name__ == '__main__':
    main()
