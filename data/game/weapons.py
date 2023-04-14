from random import randint


class CommonWeapon:
    def __init__(self, level, bonus, name):
        self.level = level
        self.bonus = bonus
        self.name = name

    def check_weapon(self):
        text = [f'ОРУЖИЕ\n',
                f'Название: {self.name}\n'
                f'Уровень оружия: {self.level}\n',
                f'Бонусный урон: {self.bonus}\n']
        return text

    def attack(self):
        return self.bonus


# class Sword(CommonWeapon):
#     def attack(self):
#         dices = list()
#         total = 0
#         for i in range(self.level):
#             dice = randint(1, 6)
#             dices.append(dice)
#             total += dice
#         duplicates = 0
#         for i in range(len(dices)):
#             if i == 0:
#                 continue
#             else:
#                 if dices[i] == dices[i - 1]:
#                     duplicates += 1
#         if duplicates == 2:
#             print('У игрока 3 одинаковых кубика - X2 урона!')
#             total *= 2
#         elif duplicates == 1:
#             print('У игрока 2 одинаковых кубика - X1.5 урона!')
#             total *= 1.5
#         else:
#             if self.level > 1:
#                 print('Все кубики разные - крита нет')
#         total += self.bonus
#         return total
#

# start_sword = Sword(level=1, bonus=0, name='Обычный меч')
monster_fists = CommonWeapon(level=1, bonus=3, name='Кулаки')
pitchfork = CommonWeapon(level=1, bonus=5, name='Вилы')
