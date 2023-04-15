class Item:
    def __init__(self, name, description, defence_bonus=0, attack_bonus=0, health_bonus=0):
        self.name = name
        self.defence_bonus = defence_bonus
        self.attack_bonus = attack_bonus
        self.description = description
        self.health_bonus = health_bonus

    def show(self):
        return f'{self.name.upper()}\n' \
               f'Бонус к броне: +{self.defence_bonus}\n' \
               f'Бонус к урону: +{self.attack_bonus}\n' \
               f'Бонус к здоровью: +{self.health_bonus}\n' \
               f'Описание: {self.description}'


camomile = Item(name='Ромашка', description='она защищает вашу душу', defence_bonus=5)
