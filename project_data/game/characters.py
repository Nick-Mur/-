import project_data.game.weapons as weapons
import project_data.game.armors as armors
import project_data.game.special_items as special_items
from random import randint


class Seller:
    def __init__(self, name, cash, items):
        self.name = name
        self.cash = cash
        self.items = items
        self.discount = False
        self.items_with_discount = {}
        for i in items:
            self.items_with_discount[i] = items[i] // 2

    def show_items(self):
        text = ''
        if not self.discount:
            for i in self.items:
                text += f'{i.name}: {self.items[i]} золотых.\n' \
                        f'О предмете: ' \
                        f'{i.description}\n'
        else:
            for i in self.items_with_discount:
                text += f'{i.name}: {self.items_with_discount[i]} золотых.\n' \
                        f'О предмете: ' \
                        f'{i.description}\n'
        return text


class Enemy:
    def __init__(self, health, weapon, name, armor):
        self.health = health
        self.weapon = weapon
        self.name = name
        self.status = 'alive'
        self.defence = armor.defence
        self.armor = armor
        self.action = None

    def attack(self, hero):
        damage = self.weapon.attack()
        if hero.defence == 0:
            hero.health -= damage
        else:
            hero.defence -= damage
            if hero.defence < 0:
                hero.defence = 0
        return damage

    def check_status(self):
        return f'Имя: {self.name}\n' \
               f'Здоровье: {self.health}\n' \
               f'Урон: {self.weapon.min_damage} - {self.weapon.max_damage}\n' \
               f'Показатель защиты: {self.defence}\n' \
               f'Оружие: {self.weapon.name}\n' \
               f'Броня: {self.armor.name}'

    def doing(self):
        if randint(1, 10) < 7:
            self.action = f'{self.name} готовится нанести удар!'
        else:
            self.action = f'{self.name} отдыхает'
        return self.action


class Peasant:
    def __init__(self, name, weapon, health, armor, hero_class, min_block, max_block, items, ability):
        self.name = name
        self.weapon = weapon
        self.health = health
        self.base_defence = armor.defence
        self.defence = armor.defence
        self.armor = armor
        self.level = 0
        self.status = 'alive'
        self.hero_class = hero_class
        self.special_items = list()
        self.expendables = items
        self.cash = 0
        self.min_block = min_block
        self.max_block = max_block
        self.max_health = health
        self.name_expendables = [i.name for i in items]
        self.ability = ability

    def attack(self, other, text):
        if type(self.weapon) == weapons.CommonWeapon:
            damage = self.weapon.attack()
        elif type(self.weapon) == weapons.Sword:
            damage = self.weapon.sword_attack(self)
        elif type(self.weapon) == weapons.Staff:
            damage = self.weapon.cast(text, other, self)
        elif type(self.weapon) == weapons.MaceWithShield:
            damage, block = self.weapon.series_attacks(text)
            self.defence += block
        if other.defence == 0:
            other.health -= damage
        else:
            other.defence -= damage
            if other.defence < 0:
                other.defence = 0
        return damage

    def check_status(self):
        return f'Имя: {self.name}\n' \
               f'Уровень: {self.level}\n' \
               f'Класс: {self.hero_class}\n' \
               f'Здоровье: {self.health} из {self.max_health}\n' \
               f'Показатель защиты: {self.defence} из {self.base_defence}\n' \
               f'Оружие: {self.weapon.name}\n' \
               f'Броня: {self.armor.name}\n' \
               f'Блок: {self.min_block} - {self.max_block}\n' \
               f'Способность: {self.ability}'

    def show_items(self):
        text = list()
        for i in self.special_items:
            text.append(i.show())
        return text

    def show_expendables(self):
        text = list()
        for i in self.expendables:
            text.append(i.info())
        return text

    def use_expendable(self, expendable):
        for i in self.expendables:
            if i.name == expendable:
                i.use(hero)
                self.expendables.remove(i)
                self.name_expendables.remove(expendable)
            break

    def use_block(self):
        return randint(self.min_block, self.max_block)


hero = Peasant(health=25, weapon=weapons.pitchfork, name=None,
               armor=armors.peasants_robe, hero_class='Крестьянин', min_block=1, max_block=2,
               items=[special_items.loaf],
               ability='способностей нет'
               )
monster = Enemy(health=15, weapon=weapons.monster_fists, name='Монстр', armor=armors.tattered_clothing)
miss_seller = Seller(name='Даша', cash=100,
                     items={weapons.start_balanced_weapon: 150, special_items.loaf: 50})
