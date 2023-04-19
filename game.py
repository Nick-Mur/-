import telebot
from telebot import types

import project_data.game.armors as armors
import project_data.game.weapons as weapons
import project_data.game.special_items as special_items
import project_data.game.characters as characters
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
miss_seller = characters.miss_seller
enemy = characters.monster
first_move = True
way = 'pacifist'
first_fight = True
fight_now = False
in_inventory = False
remove = types.ReplyKeyboardRemove()
in_shop = False
# endregion

# region blocks
block_start_game = False
block_name = False
block_story_start = False
block_fight1 = False
block_finish_sparing1 = False
block_choice_class = False
block_go_to_tavern = False
block_tavern = False
block_question = False
block_view_product = False
# endregion


# region telegram_start
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
# endregion


# region game
@bot.message_handler(content_types=['text'])
def game(message):
    # region story_blocks
    global block_start_game, block_name, block_story_start,\
        block_fight1, block_finish_sparing1, block_choice_class,\
        block_go_to_tavern, block_tavern, block_question, block_view_product
    # endregion
    global in_inventory, in_shop
    # region hero_is_dead
    if hero.health <= 0:
        bot.send_message(
            message.chat.id,
            f'Прости, {hero.name}, не смог тебя я защитить.',
            reply_markup=remove
        )
        hero_lose(message)
    # endregion
    # region /start
    if message.text == 'Начать игру' and block_start_game is False:
        start_game(message)
        block_start_game = True
    # endregion
    # region name
    if block_name is True and hero.name is None and message.text != 'Начать игру':
        if message.text.isalpha():
            hero.name = message.text
        else:
            hero.name = 'Мистер Крестьянин'
    # endregion
    # region story_start
    if hero.name and block_story_start is False and block_name is True:
        story_start(message)
        block_story_start = True
    # endregion
    # region start_fight
    if message.text == 'Подойти к Монстру' and block_fight1 is False and block_story_start is True:
        # todo: сделать доп блок от следующего этапа
        if block_story_start is True:
            start_fight(message)
    # endregion
    # region fight
    if fight_now is True:
        # region check_self
        if message.text == 'Проверить своё состояние':
            bot.send_message(
                message.chat.id,
                hero.check_status()
            )
        # endregion
        # region punch
        elif message.text == 'Ударить':
            damage = hero.attack(enemy, message.text)
            bot.send_message(
                message.chat.id,
                f'Ты нанёс {damage} урона! Теперь у {enemy.name} {enemy.health} жизни и {enemy.defence} брони.'
            )
        # endregion
        # region block
        elif message.text == 'Блок':
            block = hero.use_block()
            bot.send_message(
                message.chat.id,
                f'Твоя защита увеличена на {block}!'
            )
            hero.defence += block
        # endregion
        # todo: доделать инвентарь
        # region inventory
        elif message.text == 'Открыть инвентарь':
            create_inventory(message)
        elif message.text == 'Посмотреть оружие':
            check_weapon(message)
        elif message.text == 'Посмотреть броню':
            check_armor(message)
        elif message.text == 'Посмотреть расходники':
            check_expendables(message)
        elif message.text in hero.name_expendables and in_inventory:
            hero.use_expendable(message.text)
            in_inventory = False
            bot.send_message(
                message.chat.id,
                'Расходник был использован!',
                reply_markup=remove
            )
            bot.send_message(
                message.chat.id,
                'Вернёмся к бою.',
                reply_markup=create_all_battles_btn()
            )
        elif message.text == 'Закрыть инвентарь' and in_inventory:
            bot.send_message(
                message.chat.id,
                'Хорошо.',
                reply_markup=remove
            )
            bot.send_message(
                message.chat.id,
                'Вернёмся к бою.',
                reply_markup=create_all_battles_btn()
            )
            in_inventory = False
        # endregion
        # region check_enemy
        elif message.text == 'Проверить состояние противника':
            check_enemy(message)
        # endregion
        if message.text == 'Ударить' or message.text == 'Блок':
            # region fight_start
            if first_move:
                first_move_in_fight(message)
            # endregion
            # region enemy do
            elif enemy.health > 0 and not first_move:
                if enemy.action == f'{enemy.name} готовится нанести удар!':
                    enemy_attack(message)
                # region enemy think
                enemy.doing()
                bot.send_message(
                    message.chat.id,
                    f'{enemy.action}'
                )
                # endregion
            # endregion
            # region win
            elif enemy.health <= 0:
                with open('project_data/video_and_images/finish_punch.gif', 'rb') as f:
                    bot.send_animation(
                        message.chat.id,
                        f
                    )
                enemy_defeat(message)
                block_fight1 = True
            # endregion
    # endregion
    # region after_first_fight
    if message.text == 'Добить' and block_finish_sparing1 is False and block_fight1 is True:
        finish_off_the_enemy(message)
        block_finish_sparing1 = True
    bot.register_next_step_handler(message, game)
    if message.text == 'Пощадить' and block_finish_sparing1 is False and block_fight1 is True:
        spare_the_enemy(message)
        block_finish_sparing1 = True
    if message.text == 'Стать магом' and block_choice_class is False and block_finish_sparing1 is True:
        become_mage(message)
        block_choice_class = True
    if message.text == 'Стать воином' and block_choice_class is False and block_finish_sparing1 is True:
        become_warrior(message)
        block_choice_class = True
    # endregion
    # region tavern
    if message.text == 'Идти дальше' and block_go_to_tavern is False and block_finish_sparing1 is True:
        go_to_tavern(message)
        block_go_to_tavern = True
    if message.text == 'Войти в таверну' and block_tavern is False and block_go_to_tavern is True:
        tavern(message)
        block_tavern = True
    if message.text == 'Спросить, что интересного говорят в последнее время'\
            and block_question is False and block_tavern is True:
        ask(message)
        block_question = True
    if message.text == 'Посмотреть товар' and block_view_product is False and block_tavern is True:
        view_item(message)
        block_view_product = True
    if in_shop:
        for i in miss_seller.items:
            if message.text == i.name:
                if way == 'murder':
                    if hero.cash >= miss_seller.items[i]:
                        hero.cash -= miss_seller.items[i]
                        if i in weapons.weapons:
                            hero.weapon = i
                        elif i in armors.armors:
                            hero.armor = i
                        elif i in special_items.items:
                            hero.expendables.append(i)
                        bot.send_message(
                            message.chat.id,
                            f'Предмет был куплен.'
                        )
                elif way == 'pacifist':
                    if hero.cash >= miss_seller.items_with_discount[i]:
                        hero.cash -= miss_seller.items_with_discount[i]
                        if i in weapons.weapons:
                            hero.weapon = i
                        elif i in armors.armors:
                            hero.armor = i
                        elif i in special_items.items:
                            hero.expendables.append(i)
                        bot.send_message(
                            message.chat.id,
                            f'Предмет был куплен.'
                        )
    if message.text == 'Уйти из магазина' and block_tavern is True:
        if way == 'pacifist':
            bot.send_message(
                message.chat.id,
                f'{hero.name}: спасибо тебе, {miss_seller.name}, мне пора идти, удачи!'
            )
        bot.send_message(
            message.chat.id,
            f'{miss_seller.name}: до новых встреч, {hero.name}.',
            reply_markup=remove
        )
        in_shop = False
    # endregion


# endregion


# region func
def start_game(message):
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
    with open('project_data/video_and_images/village.gif', 'rb') as f:
        bot.send_animation(
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


def start_fight(message):
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


def finish_off_the_enemy(message):
    global way, block_finish_sparing1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mage = types.KeyboardButton('Стать магом')
    warrior = types.KeyboardButton('Стать воином')
    enemy.status = 'dead'
    way = 'murder'
    bot.send_message(
        message.chat.id,
        f'Ты добил монстра.',
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'Поздравляю, {hero.name}, ты стал ближе к тому, чтобы стать НАСТОЯЩИМ героем!',
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


def spare_the_enemy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go_btn = types.KeyboardButton('Идти дальше')
    bot.send_message(
        message.chat.id,
        f'{hero.name}: У меня не было выбора {enemy.name},'
        f' но теперь, когда он у меня есть, я не стану тебя добивать тебя.',
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'{enemy.name}: я понимаю, ты ведь герой. Вот, держи, мне не жалко.',
    )
    hero.expendables.append(special_items.loaf)
    bot.send_message(
        message.chat.id,
        f'Получен предмет *Буханка*!',
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


# todo: доделать
def become_mage(message):
    global hero
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go_btn = types.KeyboardButton('Идти дальше')
    bot.send_message(
        message.chat.id,
        f'Теперь ты маг 1 уровня!',
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'Получены новые предметы: Палка ботаника и Роба мага!',
    )
    markup.add(go_btn)
    bot.send_message(
        message.chat.id,
        f'Пойдём же дальше в путь, мой добрый друг, на встречу приключениям!',
        reply_markup=markup
    )
    characters.hero = \
        characters.Peasant(health=30, weapon=weapons.stick_nerd, name=hero.name,
                           armor=armors.mage_robe, hero_class='Маг', min_block=1, max_block=2,
                           items=hero.expendables,
                           ability='раскрывает истинную мощь посохов, открывая новые заклинания.'
                           )
    hero = characters.hero


# todo: доделать
def become_warrior(message):
    global hero
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go_btn = types.KeyboardButton('Идти дальше')
    bot.send_message(
        message.chat.id,
        f'Теперь ты воин 1 уровня!',
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'Получены новые предметы: Кубомеч и Доспех воина!',
    )
    markup.add(go_btn)
    bot.send_message(
        message.chat.id,
        f'Пойдём же дальше в путь, мой добрый друг, на встречу приключениям!',
        reply_markup=markup
    )
    characters.hero = \
        characters.Peasant(health=35, weapon=weapons.dice_sword, name=hero.name,
                           armor=armors.warrior_armor, hero_class='Воин', min_block=2, max_block=3,
                           items=hero.expendables,
                           ability='делает тебя мастером меча, увеличивает твой урон в 1.5 раз,'
                                   ' если при атаке мечом выпадает дубль.'
                           )
    hero = characters.hero


def go_to_tavern(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    enter_btn = types.KeyboardButton('Войти в таверну')
    markup.add(enter_btn)
    bot.send_message(
        message.chat.id,
        f'Смотри, {hero.name}, таверна! Думаю, там можно будет найти то, что поможет тебе в пути.',
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'Держи, тебе это тебе понадобится.'
    )
    bot.send_message(
        message.chat.id,
        f'Получено 100 золота!'
    )
    hero.cash = 100
    bot.send_message(
        message.chat.id,
        f'Идём?',
        reply_markup=markup
    )


def tavern(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    view_btn = types.KeyboardButton('Посмотреть товар')
    asked_btn = types.KeyboardButton('Спросить, что интересного говорят в последнее время')
    if message.text == 'Войти в таверну':
        bot.send_message(
            message.chat.id,
            f'{miss_seller.name}: Добро пожаловать в мою таверну! Чего желаешь, путник?',
            reply_markup=remove
        )
        if way == 'pacifist':
            markup.add(view_btn, asked_btn)
            bot.send_message(
                message.chat.id,
                f'{miss_seller.name}:'
                f' Слышала, ты отличаешься от "сказочных героев", мне такое нравится.\n'
                f'Думаю я могу позволить себе выделить для тебя скидку в 50%, не обеднею.',
                reply_markup=markup
            )
            miss_seller.discount = 50
        else:
            markup.add(view_btn)
            bot.send_message(
                message.chat.id,
                f'{miss_seller.name}:'
                f' Знаешь, в наших краях не все любят героев. Удачи, конечно, на твоём на пути, но ты берегись.',
                reply_markup=markup
            )


def ask(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    view_btn = types.KeyboardButton('Посмотреть товар')
    bot.send_message(
        message.chat.id,
        f'{hero.name}:'
        f' Что интересного ты можешь рассказать?',
        reply_markup=remove
    )
    markup.add(view_btn)
    bot.send_message(
        message.chat.id,
        f'{miss_seller.name}:'
        f' Да в целом все не так плохо, все постепенно привыкают к новой жизни.\n'
        f'Хотя некоторые верят, что вражда ещё не окончена.',
        reply_markup=markup
    )


def view_item(message):
    global in_shop
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    view_btn = types.KeyboardButton('Уйти из магазина')
    markup.add(view_btn)
    bot.send_message(
        message.chat.id,
        f'{miss_seller.name}:'
        f' Вот, смотри, бери что хочешь, главное чтоб золотых хватило!',
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        miss_seller.show_items()
    )
    bot.send_message(
        message.chat.id,
        f'Введи название того предмета, который ты хочешь купить.',
        reply_markup=markup
    )
    in_shop = True


# region battle
def create_all_battles_btn():
    hit_btn = types.KeyboardButton('Ударить')
    # region inventory
    check_inventory_btn = types.KeyboardButton('Открыть инвентарь')
    # endregion
    block_btn = types.KeyboardButton('Блок')
    check_self_status_btn = types.KeyboardButton('Проверить своё состояние')
    check_enemy_status_btn = types.KeyboardButton('Проверить состояние противника')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(hit_btn, check_inventory_btn, block_btn)
    markup.add(check_self_status_btn, check_enemy_status_btn)
    return markup


def create_inventory(message):
    bot.send_message(
        message.chat.id,
        'Хорошо.',
        reply_markup=remove
    )
    # region buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    check_expendables_btn = types.KeyboardButton('Посмотреть расходники')
    check_special_items_btn = types.KeyboardButton('Посмотреть особые предметы')
    check_weapon_btn = types.KeyboardButton('Посмотреть оружие')
    check_armor_btn = types.KeyboardButton('Посмотреть броню')
    buttons = list()
    if len(hero.show_items()) != 0:
        buttons.append(check_special_items_btn)
    if len(hero.show_expendables()) != 0:
        buttons.append(check_expendables_btn)
    buttons.append(check_weapon_btn)
    buttons.append(check_armor_btn)
    markup.add(*buttons)
    # endregion
    bot.send_message(
        message.chat.id,
        'Что ты хочешь посмотреть?',
        reply_markup=markup
    )


def check_weapon(message):
    bot.send_message(
        message.chat.id,
        hero.weapon.info(),
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'Что же ты сделаешь, {hero.name}?',
        reply_markup=create_all_battles_btn()
    )


def check_armor(message):
    bot.send_message(
        message.chat.id,
        hero.armor.info(),
        reply_markup=remove
    )
    bot.send_message(
        message.chat.id,
        f'Что же ты сделаешь, {hero.name}?',
        reply_markup=create_all_battles_btn()
    )


def check_enemy(message):
    bot.send_message(
        message.chat.id,
        enemy.check_status()
    )


def first_move_in_fight(message):
    global first_move
    if first_move:
        bot.send_message(
            message.chat.id,
            f'{enemy.name} вступил в бой!'
        )
        first_move = False
        enemy.doing()
        bot.send_message(
            message.chat.id,
            f'{enemy.action}'
        )


def enemy_attack(message):
    if enemy.action == f'{enemy.name} готовится нанести удар!':
        enemy_damage = enemy.attack(hero=hero)
        bot.send_message(
            message.chat.id,
            f'{enemy.name} нанёс {enemy_damage} урона!'
            f' Теперь у тебя {hero.health} жизни и {hero.defence} брони.'
        )


def enemy_defeat(message):
    global first_move, fight_now
    mercy_btn = types.KeyboardButton('Пощадить')
    finish_of_btn = types.KeyboardButton('Добить')
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
    enemy.action = None
    first_move = True
    fight_now = False


def check_expendables(message):
    global in_inventory
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    close_inventory = types.KeyboardButton('Закрыть инвентарь')
    markup.add(close_inventory)
    bot.send_message(
        message.chat.id,
        'Вот, всё, что у тебя есть.',
        reply_markup=remove
    )
    for i in hero.show_expendables():
        bot.send_message(
            message.chat.id,
            i
        )
    bot.send_message(
        message.chat.id,
        f'Введи название того предмета, который ты хочешь использовать',
        reply_markup=markup
    )
    in_inventory = True


# todo: доделать
def hero_lose(message):
    global hero, enemy, miss_seller,\
        first_move, way, first_fight, fight_now, in_inventory,\
        block_start_game, block_name, block_story_start, block_fight1, block_finish_sparing1, block_choice_class,\
        block_go_to_tavern, block_tavern, block_question, block_view_product

    # todo: переделать в нормальный вид
    hero = characters.Peasant(health=25, weapon=weapons.pitchfork, name=None,
                              armor=armors.peasants_robe, hero_class='Крестьянин', min_block=1, max_block=2,
                              items=[special_items.loaf],
                              ability='Способностей нет'
                              )
    characters.monster = characters.Enemy(health=15, weapon=weapons.monster_fists, name='Монстр',
                                          armor=armors.tattered_clothing)
    characters.miss_seller = characters.Seller(name='Даша', cash=100,
                                               items={weapons.start_balanced_weapon: 150, special_items.loaf: 50}
                                               )
    miss_seller = characters.miss_seller
    enemy = characters.monster
    first_move = True
    way = 'pacifist'
    block_start_game = False
    block_name = False
    block_story_start = False
    block_fight1 = False
    block_finish_sparing1 = False
    block_choice_class = False
    block_go_to_tavern = False
    block_tavern = False
    block_question = False
    block_view_product = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_game_btn = types.KeyboardButton('Начать игру')
    markup.add(start_game_btn)
    bot.send_message(
        message.chat.id,
        f'Кажется, наша история пошла неправильно. Начнём же сначала, {message.from_user.first_name}?',
        reply_markup=markup
    )

# endregion
# endregion


bot.infinity_polling()
