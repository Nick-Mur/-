import project_data.game.weapons as weapons
import project_data.game.armors as armors


class Seller:
    def __init__(self, name, cash, discount, **items):
        self.name = name
        self.cash = cash
        self.discount = discount
        self.items = items


class Enemy:
    def __init__(self, health, weapon, name, armor):
        self.health = health
        self.weapon = weapon
        self.name = name
        self.status = 'alive'
        self.defence = armor.defence
        self.armor = armor

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
               f'Показатель защиты: {self.defence}\n' \
               f'Оружие: {self.weapon.name}\n' \
               f'Броня: {self.armor.name}'


class Peasant:
    def __init__(self, name, weapon, health, armor, hero_class):
        self.name = name
        self.weapon = weapon
        self.health = health
        self.base_defence = armor.defence
        self.defence = armor.defence
        self.armor = armor
        self.level = 0
        self.status = 'alive'
        self.hero_class = hero_class
        self.items = list()
        self.cash = 0

    def attack(self, other):
        damage = self.weapon.attack()
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
               f'Здоровье: {self.health}\n' \
               f'Показатель защиты: {self.defence}\n' \
               f'Оружие: {self.weapon.name}\n' \
               f'Броня: {self.armor.name}'

    def show_items(self):
        text = list()
        for i in self.items:
            text.append(i.show())
        return text


class Warrior(Peasant):
    def use_super(self):
        pass


class Mage(Peasant):
    def use_super(self):
        pass


hero = Peasant(health=25, weapon=weapons.pitchfork, name='Мистер Крестьянин',
               armor=armors.peasants_robe, hero_class='Крестьянин')
monster = Enemy(health=15, weapon=weapons.monster_fists, name='Монстр', armor=armors.tattered_clothing)
miss_seller = Seller(name='Даша', cash=100, discount=0)
