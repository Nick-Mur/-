from random import randint


class CommonWeapon:
    def __init__(self, level, max_damage, min_damage, name, description=None, mechanics=None):
        self.level = level
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.bonus = 0
        self.name = name
        self.description = description
        self.mechanics = mechanics

    def info(self):
        text = f'Название: {self.name}\n' \
               f'Уровень оружия: {self.level}\n' \
               f'Урон: {self.min_damage} - {self.max_damage}\n' \
               f'Бонусный урон: {self.bonus}\n' \
               f'Описание: {self.description}\n' \
               f'Механика: {self.mechanics}'
        return text

    def attack(self):
        return randint(self.min_damage, self.max_damage)


class Sword(CommonWeapon):
    def sword_attack(self, hero):
        dice1 = randint(self.min_damage, self.max_damage)
        dice2 = randint(self.min_damage, self.max_damage)
        damage = max(dice1, dice2)
        if hero.hero_class == 'Воин':
            if dice1 == dice2:
                damage *= 1.5
        return damage


class Staff(CommonWeapon):
    def cast(self, spell, enemy, hero):
        if spell == 'hell' and hero.hero_class == 'Маг':
            if randint(1, 10) == 1:
                return enemy.health // 2
        elif spell == 'triad':
            if randint(1, 3) == 1:
                damage = 0
                for i in range(3):
                    damage += randint(self.min_damage, self.max_damage)
                return damage
        return 0


class MaceWithShield(CommonWeapon):
    def series_attacks(self, text):
        damage = 0
        block = 0
        for i in text:
            if i == 'удар':
                damage += randint(self.min_damage, self.max_damage)
            elif i == 'блок':
                block += randint(self.min_damage, self.max_damage)
        return [damage, block]


monster_fists = CommonWeapon(level=1, min_damage=1, max_damage=3, name='Кулаки')
pitchfork = CommonWeapon(level=1, min_damage=3, max_damage=5, name='Вилы',
                         mechanics='Простейшее оружие, требующее лишь нажатие кнопки',
                         description='Инструмент, созданный для блага и процветания,'
                                     ' он окажете тебе хорошую услугу по началу.')
dice_sword = Sword(level=1, min_damage=1, max_damage=6, name='Кубомеч',
                   mechanics='Оружие из разряда всё или ничего, нажимаешь на кнопку и молишься.'
                             ' После броска кубиков, нанесённый урон - максимальное значение из них.',
                   description='Говорят, это оружие зачаровал какой-то азартный маг, любящий кубы.'
                               'А может он и сам был каким-то кубом из какого-то подземелья, уже не поймёшь...')
stick_nerd = Staff(level=1, min_damage=1, max_damage=3, name='Палка ботаника',
                   mechanics='Тут всё сложно, нужно выбрать одно из заклинаний,'
                             ' написав его название, и надеяться, что оно сработает.'
                             ' Ну или просто кого-то ударить палкой.',
                   description='Маг, обладавший этим посох, был помешен на заклинаниях и'
                               ' сделал для них отдельную книжицу, а остальным теперь с этим разбираться.')
start_balanced_weapon = MaceWithShield(level=1, min_damage=1, max_damage=2, name='Мега убивалка',
                                       mechanics='Введи 3 слова с маленькой буквы: либо "удар", либо "блок".'
                                                 'Блок даст тебе защиты, а удар - урон!',
                                       description='Герой, использовавший это оружие явно знал толк как в защите,'
                                                   'так и названиях.')
weapons = [monster_fists, pitchfork, dice_sword, stick_nerd, start_balanced_weapon]
