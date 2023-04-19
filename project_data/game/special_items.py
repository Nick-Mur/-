class SpecialItem:
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


class HealItem:
    def __init__(self, heal, description, name):
        self.heal = heal
        self.description = description
        self.name = name

    def use(self, hero):
        hero.health += self.heal
        if hero.health > hero.max_health:
            hero.health = hero.max_health

    def info(self):
        return f"{self.name} - восстанавливает {self.heal} здоровья. Описание: {self.description}"


camomile = SpecialItem(name='Ромашка', description='она защищает вашу душу', defence_bonus=5)
loaf = HealItem(name='Буханка', heal=5, description='Вкусная и полезная еда')
items = [loaf]
