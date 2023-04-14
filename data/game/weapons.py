from random import randint


class Weapon:
    def __init__(self, level, bonus):
        self.level = level
        self.bonus = bonus


class Sword(Weapon):
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


class Fists:
    def __init__(self, damage):
        self.damage = damage

    def attack(self):
        return self.damage


start_sword = Sword(1, 0)
monster_fists = Fists(3)
