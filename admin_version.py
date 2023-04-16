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
enemy = monster
first_move = True
way = 'pacifist'


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


@bot.message_handler(content_types=['text'])
def start_game(message):
    global enemy, first_move
    if message.text.isalpha():
        hero.name = message.text

    register_nickname(message.from_user.id, hero.name)

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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    come_up_btn = types.KeyboardButton('Подойти')
    markup.add(come_up_btn)
    bot.send_message(
        message.chat.id,
        'Иди, разберись с ним!',
        reply_markup=markup
    )
    bot.register_next_step_handler(message, fight_with_enemy1)


@bot.message_handler(content_types=['text'])
def fight_with_enemy1(message):
    global enemy, first_move
    # region buttons
    remove = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    check_self_status_btn = types.KeyboardButton('Проверить своё состояние')
    check_inventory_btn = types.KeyboardButton('Проверить инвентарь')
    hit_btn = types.KeyboardButton('Ударить')
    check_enemy_status_btn = types.KeyboardButton('Проверить состояние противника')
    mercy_btn = types.KeyboardButton('Пощадить')
    finish_of_btn = types.KeyboardButton('Добить')
    markup.add(hit_btn, check_enemy_status_btn)
    markup.add(check_self_status_btn, check_inventory_btn)
    # endregion
    if message.text == 'Подойти':
        bot.send_message(
            message.chat.id,
            'FIGHT!!!',
            reply_markup=remove
        )

        bot.send_message(
            message.chat.id,
            f'Что же ты сделаешь, {hero.name}?',
            reply_markup=markup
        )
    if message.text == 'Проверить своё состояние':
        bot.send_message(
            message.chat.id,
            hero.check_status()
        )
    # region fight
    elif message.text == 'Ударить':
        damage = hero.attack(monster)
        bot.send_message(
            message.chat.id,
            f'Ты нанёс {damage} урона! Теперь у {enemy.name} {enemy.health} жизни и {enemy.defence} брони.'
        )
        if first_move:
            bot.send_message(
                message.chat.id,
                f'{enemy.name} вступил в бой!'
            )
        enemy_damage = enemy.attack(hero=hero)
        if monster.health > 0 and not first_move:
            bot.send_message(
                message.chat.id,
                f'{enemy.name} нанёс {enemy_damage} урона!'
                f' Теперь у тебя {hero.health} жизни и {hero.defence} брони.'
            )
        elif monster.health <= 0:
            bot.send_message(
                message.chat.id,
                f'{enemy.name} повержен.',
                reply_markup=remove
            )
            bot.send_message(
                message.chat.id,
                f'Ваш показатель брони восстановлен.',
            )
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(mercy_btn, finish_of_btn)
            bot.send_message(
                message.chat.id,
                'Добей его, чтобы получить новый уровень и возможность стать настоящим героем!',
                reply_markup=markup
            )
            hero.defence = hero.base_defence
            bot.register_next_step_handler(message, take_a_decision1)
        if monster.health > 0:
            bot.send_message(
                message.chat.id,
                f'{enemy.name} готовится нанести {enemy.weapon.damage} урона.'
            )
            first_move = False
    # endregion
    elif message.text == 'Проверить инвентарь':
        text = list()
        text += hero.weapon.check_weapon() + ['\n'] + hero.armor.check_armor()
        text = ''.join(text)
        bot.send_message(
            message.chat.id,
            text
        )
    elif message.text == 'Проверить состояние противника':
        bot.send_message(
            message.chat.id,
            enemy.check_status()
        )
    bot.register_next_step_handler(message, fight_with_enemy1)


@bot.message_handler(content_types=['text'])
def take_a_decision1(message):
    global hero, way
    # region buttons
    remove = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go_btn = types.KeyboardButton('Идти дальше')
    mage = types.KeyboardButton('Стать магом')
    warrior = types.KeyboardButton('Стать воином')
    # endregion
    # region pacifist
    if message.text == 'Пощадить':
        bot.send_message(
            message.chat.id,
            f'{hero.name}: У меня не было выбора {enemy.name},'
            f' но теперь, когда он у меня есть, я не стану тебя добивать тебя.',
            reply_markup=remove
        )
        bot.send_message(
            message.chat.id,
            f'{enemy.name}: я понимаю, ты ведь герой. Вот, держи, она защитит твою душу!',
        )
        hero.armor.add_special(special=special_items.camomile)
        bot.send_message(
            message.chat.id,
            f'Получен предмет *Ромашка*!',
        )
        bot.send_message(
            message.chat.id,
            f'...',
        )
        markup.add(go_btn)
        bot.send_message(
            message.chat.id,
            f'Что ж, {hero.name}, твой уровень повысился на 0.\n'
            f'В этот раз ты не смог стать настоящим героем, но у тебя ещё будет возможность.',
            reply_markup=markup
        )
        bot.register_next_step_handler(message, tavern_approach)
    # endregion
    # region murder
    elif message.text == 'Добить':
        enemy.status = 'dead'
        way = 'murder'
        bot.send_message(
            message.chat.id,
            f'Ты добил монстра.',
            reply_markup=remove
        )
        bot.send_message(
            message.chat.id,
            f'Поздравляю, {hero.name}, ты стал ближе к тому, чтобы стать НАСТОЯЩИМ героем! Теперь ты герой 1 уровня!',
        )
        bot.send_message(
            message.chat.id,
            f'Уровень повышен на 1.',
        )
        markup.add(mage, warrior)
        bot.send_message(
            message.chat.id,
            f'И теперь ты можешь выбрать себе класс и получить новое оружие!',
            reply_markup=markup
        )
    elif message.text == 'Стать магом':
        bot.send_message(
            message.chat.id,
            f'Теперь ты маг 1 уровня!',
            reply_markup=remove
        )
        bot.send_message(
            message.chat.id,
            f'Получены новые предметы: Посох мага и Роба мага!',
        )
        markup.add(go_btn)
        bot.send_message(
            message.chat.id,
            f'Пойдём же дальше в путь, мой добрый друг, на встречу приключениям!',
            reply_markup=markup
        )
        hero = characters.Mage(health=25, weapon=weapons.start_staff, name=hero.name,
                               armor=armors.mage_robe, hero_class='Маг')
        bot.register_next_step_handler(message, tavern_approach)
    elif message.text == 'Стать воином':
        bot.send_message(
            message.chat.id,
            f'Теперь ты воин 1 уровня!',
            reply_markup=remove
        )
        bot.send_message(
            message.chat.id,
            f'Получены новые предметы: Меч воина и Доспех воина!',
        )
        markup.add(go_btn)
        bot.send_message(
            message.chat.id,
            f'Пойдём же дальше в путь, мой добрый друг, на встречу приключениям!',
            reply_markup=markup
        )
        hero = characters.Mage(health=30, weapon=weapons.start_sword, name=hero.name,
                               armor=armors.warrior_armor, hero_class='Воин')
        bot.register_next_step_handler(message, tavern_approach)
    # endregion
    bot.register_next_step_handler(message, take_a_decision1)


@bot.message_handler(content_types=['text'])
def tavern_approach(message):
    remove = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    enter_btn = types.KeyboardButton('Войти в таверну')
    markup.add(enter_btn)
    if message.text == 'Идти дальше':
        bot.send_message(
            message.chat.id,
            f'Смотри, {hero.name}, таверна! Думаю, там можно будет найти то, что поможет тебе в пути.',
            reply_markup=remove
        )
        bot.send_message(
            message.chat.id,
            f'Идём?',
            reply_markup=markup
        )
        bot.register_next_step_handler(message, tavern)


@bot.message_handler(content_types=['text'])
def tavern(message):
    remove = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    enter_btn = types.KeyboardButton('Войти в таверну')
    markup.add(enter_btn)
    if message.text == 'Войти в таверну':
        bot.send_message(
            message.chat.id,
            f'{characters.miss_seller.name}: Добро пожаловать в мою таверну! Чего желаешь, путник?',
            reply_markup=remove
        )
        if way == 'pacifist':
            bot.send_message(
                message.chat.id,
                f'{characters.miss_seller.name}:'
                f' Слышала, ты отличаешься от "классических героев", мне такое нравится.\n'
                f'Думаю я могу позволить себе выделить для тебя скидку в 50%, не обеднею.',
                reply_markup=remove
            )


bot.infinity_polling()
