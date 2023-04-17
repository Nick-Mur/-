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
fight_now = False
# endregion

# region blocks
block_start_game = False
block_name = False
block_story_start = False
block_fight1 = False
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
    global block_start_game, block_name, block_story_start, block_fight1
    remove = types.ReplyKeyboardRemove()
    # region /start
    if message.text == 'Начать игру' and block_start_game is False:
        start_game(message, remove)
        block_start_game = True
    # endregion
    # region name
    if block_name is True and hero.name is None and message.text != 'Начать игру':
        if message.text.isalpha():
            hero.name = message.text
        else:
            hero.name = 'Мистер Крестьянин'
    # endregion
    # region store_start
    if hero.name and block_story_start is False:
        story_start(message)
        block_story_start = True
    # endregion
    # region start_fight
    if message.text == 'Подойти к Монстру':
        # todo: сделать доп блок от следующего этапа
        if block_story_start is True:
            start_fight(message, remove)
    # endregion
    # region fight
    if fight_now is True:
        pass
    # endregion
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


def story_start(message):
    # region buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    come_up_btn = types.KeyboardButton(f'Подойти к Монстру')
    markup.add(come_up_btn)
    # endregion
    register_nickname(message.from_user.id, hero.name)
    # region text
    bot.send_message(
        message.chat.id,
        'В этих краях давно водились монстры, разбойники и прочая нечисть.\n'
        f'Ты, {hero.name}, недовольный крестьянин.\n'
        'Тебе нужен король, ведь ты хочешь высказать ему всё, что у тебя накопилось.\n'
        'Для этого ты готов пройти долгий и сложный путь.\n'
        'Но не бойся, на протяжении всего пути я буду с тобой.'
    )
    with open('project_data/video_and_images/village.mp4', 'rb') as f:
        bot.send_video(
            message.chat.id,
            f
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
    bot.send_message(
        message.chat.id,
        'Иди, разберись с ним!',
        reply_markup=markup
    )
    # endregion


def start_fight(message, remove):
    global first_fight, fight_now
    # region "FIGHT!!!"
    bot.send_message(
        message.chat.id,
        'FIGHT!!!',
        reply_markup=remove
    )
    # endregion
    # region training
    if first_fight:
        bot.send_message(
            message.chat.id,
            f'Краткий экскурс, чтобы не умереть в самом начале наше великого пути:\n'
            f'1) первом делом, советую посмотреть свои показатели и показатели врага,'
            f' а то можно попасть в неловкую ситуацию\n'
            f'2) балансируй между атакой и защитой - это важно\n'
            f'3) не забывай использовать расходники, в случае чего они спасут твою жизнь'
        )
    first_fight = False
    # endregion
    bot.send_message(
        message.chat.id,
        f'Что же ты сделаешь, {hero.name}?',
        reply_markup=create_all_battles_btn()
    )
    fight_now = True


def create_all_battles_btn():
    hit_btn = types.KeyboardButton('Ударить')
    # region inventory
    check_inventory_btn = types.KeyboardButton('Открыть инвентарь')
    check_expendables_btn = types.KeyboardButton('Посмотреть расходники')
    check_special_items_btn = types.KeyboardButton('Посмотреть особые предметы')
    check_weapon = types.KeyboardButton('Посмотреть оружие')
    # endregion
    block_btn = types.KeyboardButton('Блок')
    check_self_status_btn = types.KeyboardButton('Проверить своё состояние')
    check_enemy_status_btn = types.KeyboardButton('Проверить состояние противника')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(hit_btn, check_inventory_btn, block_btn)
    markup.add(check_self_status_btn, check_enemy_status_btn)
    return markup


bot.infinity_polling()
