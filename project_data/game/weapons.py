from random import randint


class CommonWeapon:
    def __init__(self, level, damage, name):
        self.level = level
        self.damage = damage
        self.bonus = 0
        self.name = name

    def check_weapon(self):
        text = [f'ОРУЖИЕ\n',
                f'Название: {self.name}\n'
                f'Уровень оружия: {self.level}\n',
                f'Урон: {self.damage}'
                f'Бонусный урон: {self.bonus}']
        return text

    def attack(self):
        return self.damage


class Sword(CommonWeapon):
    def attack(self):
        dices = list()
        total = 0
        for i in range(self.level):
            dice = randint(1, 6)
            dices.append(dice)
            total += dice
        duplicates = 0
        for i in range(len(dices)):
            if i == 0:
                continue
            else:
                if dices[i] == dices[i - 1]:
                    duplicates += 1
        if duplicates == 2:
            print('У игрока 3 одинаковых кубика - X2 урона!')
            total *= 2
        elif duplicates == 1:
            print('У игрока 2 одинаковых кубика - X1.5 урона!')
            total *= 1.5
        else:
            if self.level > 1:
                print('Все кубики разные - крита нет')
        total += self.bonus
        return total


class Staff(CommonWeapon):
    def attack(self):
        pass


monster_fists = CommonWeapon(level=1, damage=3, name='Кулаки')
pitchfork = CommonWeapon(level=1, damage=5, name='Вилы')
start_sword = Sword(level=1, damage=0, name='Меч воина')
start_staff = Staff(level=1, damage=0, name='Посох мага')
