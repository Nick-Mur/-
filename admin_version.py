import telebot
from telebot import types
from config import bot_token
import data.game.characters as characters
import data.game.weapons as weapons
import data.game.armors as armors
import time

# region Const
MOVE = 0
HERO_CLASS = None
hero = characters.Peasant(health=100, weapon=weapons.start_sword, name='Мистер Крестьянин', defence=5,
                          armor=armors.peasants_robe)
monster = characters.Enemy(health=25, weapon=weapons.monster_fists, name='Монстр')

# endregion

# region telegram bot
bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def telegram_start(message):
    markup = types.ReplyKeyboardMarkup()
    start_game_btn = types.KeyboardButton('Начать игру')
    markup.add(start_game_btn)
    bot.send_message(
        message.chat.id,
        f'Здравствуй, {message.from_user.first_name}! Добро пожаловать в мой мир - Talesworld.\n'
        f'Зови меня сказочником или рассказчиком, сейчас я тебе расскажу одну историю. Готов ли ты?',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def telegram_handler(message):
    """
    Обработка любого отправленного текста
    """
    remove = types.ReplyKeyboardRemove()
    if message.text == 'Начать игру':
        bot.send_message(
            message.chat.id,
            '<b>Введи имя счастливца, что станет центром нашей истории</b>',
            parse_mode='html',
            reply_markup=remove
        )
        bot.register_next_step_handler(message, start_game)


# endregion

# region game

def move():
    global MOVE
    MOVE += 1
    if MOVE == 2:
        MOVE = 0


@bot.message_handler(content_types=['text'])
def start_game(message):
    if message.text.isalpha():
        hero.name = message.text
    bot.send_message(
        message.chat.id,
        'В этих краях давно водились монстры, разбойники и прочая нечисть.\n'
        f'Ты, {hero.name}, недовольный крестьянин.\n'
        'Тебе нужен король, ведь ты хочешь высказать ему всё, что у тебя накопилось.\n'
        'Для этого ты готов пройти долгий и сложный путь.\n'
        'Но не бойся, на протяжении всего пути я буду с тобой.'
    )
    bot.send_message(
        message.chat.id,
        'Итак, пока мы только в "деревне, над которой не садится солнце", а из вещей у тебя только роба, да вилы.\n'
        'Но это ничего, не все великие герои с самого начала были таковыми, так что и тебе не стоит беспокоиться.\n'
        'Главное держись меня, лишь я на твоей стороне.'
    )
    bot.send_message(
        message.chat.id,
        'Смотри, тебе навстречу идёт монстр!\n'
        'Из рассказов, сказок и легенд, ты должен знать, когда монстры приходят в деревни к людям,'
        ' ничем хорошим это не кончается. \n'
        ''
    )
    markup = types.ReplyKeyboardMarkup()
    come_up_btn = types.KeyboardButton('Подойти')
    markup.add(come_up_btn)
    bot.send_message(
        message.chat.id,
        'Иди, разберись с ним!',
        reply_markup=markup
    )
    bot.register_next_step_handler(message, fight_with_monster)


@bot.message_handler(content_types=['text'])
def fight_with_monster(message):
    remove = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup()
    check_inventory_btn = types.KeyboardButton('Проверить инвентарь')
    hit_btn = types.KeyboardButton('Ударить')
    markup.add(check_inventory_btn)
    markup.add(hit_btn)
    if message.text == 'Подойти':
        bot.send_message(
            message.chat.id,
            'FIGHT!!!',
            reply_markup=remove
        )
        bot.send_message(
            message.chat.id,
            f'Что же ты сделаешь, {hero.name}?',
            reply_markup=remove
        )


# endregion

bot.infinity_polling()
