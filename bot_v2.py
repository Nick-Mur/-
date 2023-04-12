import telebot
from telebot import types
from config import bot_token

bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    start_game_btn = types.KeyboardButton('Начать игру')
    help_btn = types.KeyboardButton('Информация о боте')
    markup.add(start_game_btn)
    markup.add(help_btn)
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}! Хочешь сыграть в RPG?',
        reply_markup=markup
    )


@bot.message_handler(commands=['info_about_me'])
def info_about_person(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler()
def handler(message):
    """
    Обработка любого отправленного текста
    """

    if message.text in ['/help', 'Информация о боте']:
        bot.send_message(
            message.chat.id,
            '<b>Привет!!</b>\nЯ бот Whismy, '
            'и я поиграю с тобой в ожну очень увлекательную игру)',
            parse_mode='html'
        )

    elif message.text.lower() == 'начать игру':
        '''Здесь функция на начало игры'''

    elif message.text.lower() == '00000':
        bot.reply_to(message, 'Пять нулей?')


bot.infinity_polling()
