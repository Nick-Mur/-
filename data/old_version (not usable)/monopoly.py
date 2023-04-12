import random


class Player:
    def __init__(self, number, name=None):
        self.move = 0
        self.cash = 15
        self.areas = list()
        if name:
            self.nickname = name
        else:
            self.nickname = number

    def __str__(self):
        return self.nickname

    def dice(self):
        flag = False
        value = random.randint(1, 6)
        print(f'Игрок {self.nickname} выбросил {value}')
        self.move += value
        if self.move > 31:
            flag = True
            self.move = self.move - 32
        print(f'Игрок {self.nickname} перешёл на {MAP[self.move]}')
        if flag:
            print(f'Игрок {self.nickname} прошёл круг за это он получает +2$')
            self.cash += 2
            choice = int(input(f'{self.nickname}, хотите построить отель на одном из ваших участков?'
                               f' (+1$ к ренте). Введи 1 - да, 2 - нет.'))
            if choice == 1:
                while True:
                    choice = input('Введите название участка. Для отмены покупки введите "ОТМЕНА".')
                    if choice in self.areas:
                        if LOCATIONS[choice].hotel is False:
                            LOCATIONS[choice].rent += 1
                            LOCATIONS[choice].hotel = True
                            break
                        else:
                            print('У этого участка уже есть отель.')
                    elif choice == 'ОТМЕНА':
                        break
                    else:
                        print('У вас нет такого участка.')
        if MAP[self.move] == "Повторный ход":
            print('Ещё один ход')
            self.dice()
        elif MAP[self.move] == bank:
            bank.bank_time(self)
        elif type(MAP[self.move]) == CardLocation:
            MAP[self.move].player_on_card(self)


class ATM:
    def __init__(self):
        self.bank = ["единица"] * 45 + ["двойка"] * 10 + ["пятёрка"] * 5 + ["карта"] * 20
        self.count_cards = 80

    def __str__(self):
        return 'Банкомат'

    def bank_time(self, player):
        cards = list()
        if self.count_cards == 0:
            print('Банкомат пуст!')
            return
        elif self.count_cards < 4:
            for i in range(self.count_cards):
                cards.append(random.choice(self.bank))
            string_cards = ', '.join(cards)
            print(f'Игроку выпало: {string_cards}')
            print('Банкомат опустел!')
        else:
            for i in range(4):
                cards.append(random.choice(self.bank))
            string_cards = ', '.join(cards)
            print(f'Игроку выпало: {string_cards}')
        for i in cards:
            if i == "единица":
                player.cash += 1
            elif i == "двойка":
                player.cash += 2
            elif i == "пятёрка":
                player.cash += 5
            else:
                print('Игроку выпала карта: *придумать штуки для них*')


class CardLocation:
    def __init__(self, name, rent):
        self.name = name
        self.rent = rent
        self.owner = None
        self.hotel = None

    def __str__(self):
        return self.name

    def player_on_card(self, player):
        if self.owner is None:
            choice = int(input('напишите 1 или 2, чтобы купить локацию или пройти мимо'))
            if choice == 1:
                self.owner = player
                player.areas.append(self.name)
                player.cash -= self.rent
            else:
                print('Вы прошли мимо')
        else:
            print(f'Игрок {player.nickname} должен заплатить игроку {self.owner} {self.rent}')
            player.cash -= self.rent
            self.owner.cash += self.rent


bank = ATM()
MOVE = 1
a = CardLocation('Шоколадный угол', 1)
b = CardLocation('Блинная площадь', 1)
c = CardLocation('Улица улыбок', 1)
d = CardLocation('Хмурая улица', 1)
e = CardLocation('Аллея роботов', 2)
f = CardLocation('Сады Принцессы', 2)
g = CardLocation('Площадь слонов', 2)
h = CardLocation('Проезд динозавров', 2)
i = CardLocation('Радужная дорога', 3)
j = CardLocation('Волшебная улица', 3)
k = CardLocation('Солнечная улица', 3)
l = CardLocation('Звёздная улица', 3)
m = CardLocation('Желейная дорога', 4)
n = CardLocation('Проспект мороженого', 4)
o = CardLocation('Акулья улица', 5)
p = CardLocation('Переулок голубого кита', 5)
LOCATIONS = {
    'Шоколадный угол': a,
    'Блинная площадь': b,
    'Улица улыбок': c,
    'Хмурая улица': d,
    'Аллея роботов': e,
    'Сады Принцессы': f,
    'Площадь слонов': g,
    'Проезд динозавров': h,
    'Радужная дорога': i,
    'Волшебная улица': j,
    'Солнечная улица': k,
    'Звёздная улица': l,
    'Желейная дорога': m,
    'Проспект мороженого': n,
    'Акулья улица': o,
    'Переулок голубого кита': p,
}
MAP = ["Старт", bank, a, b, "Повторный ход",
       c, d, bank, "Экскурсия", bank, e, f, "Повторный ход",
       j, h, bank, "Парковка", bank, i, j, "Повторный ход",
       k, l, bank, "Тюрьма", bank, m, n, "Повторный ход", o, p, bank]
# карта
#     "Старт", bank, a, b, "Повторный ход", c, d, bank, "Экскурсия"
#     bank                                             bank
#     p                                                 e
#     o                                                 f
# "Повторный ход"                               "Повторный ход"
#     n                                                 g
#     m                                                 h
#     bank                                              bank
#     "Тюрьма", bank, l, k, "Повторный ход", j, i, bank,       "Парковка"
player1 = Player('1')
player2 = Player('2')
players = {1: player1, 2: player2}

while player1.cash > 0 or player2.cash > 0 or bank.count_cards > 0:
    print(f'Ход игрока {players[MOVE]}!')
    choice = input('Хотите посмотреть свой счёт? Введите "ДА" или "НЕТ".')
    if choice == 'ДА':
        print(players[MOVE].cash)
    choice = input('Хотите посмотреть свои участки? Введите "ДА" или "НЕТ".')
    if choice == 'ДА':
        for i in players[MOVE].areas:
            print(LOCATIONS[i], LOCATIONS[i].rent)
    players[MOVE].dice()
    MOVE += 1
    if MOVE > 2:
        MOVE = 1
