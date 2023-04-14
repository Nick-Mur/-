class Enemy:
    def __init__(self, health, weapon, name):
        self.health = health
        self.weapon = weapon
        self.name = name
        self.status = 'alive'

    def attack(self, hero):
        damage = self.weapon.attack()
        if hero.defence <= 0:
            hero.health -= damage
        else:
            hero.defence -= damage
        print(f'{self.name} нанёс вам {damage} урона! Теперь у вас {hero.health}'
              f' жизни и {hero.defence} брони')
        if hero.health <= 0:
            print(f'{self.name} победил вас')
            hero.status = 'dead'


class Peasant:
    def __init__(self, name, weapon, health, defence, armor):
        self.name = name
        self.weapon = weapon
        self.health = health
        self.base_defence = defence + armor.defence
        self.defence = defence + armor.defence
        self.armor = armor
        self.level = 0
        self.status = 'alive'

    def attack(self, other):
        damage = self.weapon.attack()
        other.health -= damage
        print(f'Вы нанесли {other.name} {damage} урона! Теперь у {other.name} {other.health} жизни')
        if other.health <= 0:
            print(f'Вы победили {other.name}')
            other.status = 'dead'
            self.defence = self.base_defence

