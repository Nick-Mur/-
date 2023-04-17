import telebot
import project_data.game.armors as armors
import project_data.game.weapons as weapons
import project_data.game.special_items as special_items
import project_data.game.characters as characters
from telebot import types
from telebot.types import WebAppInfo
from project_data.config import bot_token
from project_data.db_talesword.db_operation import db_viewer_nickname
from project_data.db_talesword.db_operation import insert_nickname_in_table
from project_data.db_talesword.db_operation import edit_nickname_in_table
from random import randint


# region DB
def register_nickname(userid, nickname):
    if db_viewer_nickname(userid):
        insert_nickname_in_table(userid, nickname)
    else:
        edit_nickname_in_table(userid, nickname)


# endregion

# region settings
# telegram bot
bot = telebot.TeleBot(token=bot_token)

# Game
hero = characters.hero
monster = characters.monster
miss_seller = characters.miss_seller
enemy = monster
first_move = True
way = 'pacifist'
first_fight = True

# endregion

# region blocks
block_start_game = False
block_name = False
block_story_start = False
# endregion


@bot.message_handler(commands=['start'])
def telegram_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_game_btn = types.KeyboardButton('Начать игру')
    markup.add(start_game_btn)
    bot.send_message(
        message.chat.id,
        f'Здравствуй, {message.from_user.first_name}! Добро пожаловать в мой мир - Talesworld.\n'
        f'Зови меня сказочником или рассказчиком, сейчас я тебе расскажу одну историю. Готов ли ты?',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def game(message):
    global block_start_game, block_name, block_story_start
    remove = types.ReplyKeyboardRemove()
    if message.text == 'Начать игру' and block_start_game is False:
        start_game(message, remove)
        block_start_game = True
    if block_name is True and hero.name is None and message.text != 'Начать игру':
        if message.text.isalpha():
            hero.name = message.text
        else:
            hero.name = 'Мистер Крестьянин'
    if hero.name and block_story_start is False:
        story_start(message, remove)
        block_story_start = True
    bot.register_next_step_handler(message, game)


def start_game(message, remove):
    global block_name
    bot.send_message(
        message.chat.id,
        '<b>Введи имя счастливца, что станет центром нашей истории</b>',
        parse_mode='html',
        reply_markup=remove
    )
    block_name = True


def story_start(message, remove):
    print(1)


bot.infinity_polling()
