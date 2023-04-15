class CommonArmor:
    def __init__(self, defence, name):
        self.defence = defence
        self.name = name
        self.special_bonus = 0

    def check_armor(self):
        text = [f'БРОНЯ\n',
                f'Название: {self.name}\n'
                f'Показатель защиты: {self.defence}\n'
                f'Бонус: {self.special_bonus}']
        return text

    def add_special(self, special):
        self.special_bonus += special.defence_bonus
        self.defence += special.defence_bonus


peasants_robe = CommonArmor(name='Роба', defence=5)
tattered_clothing = CommonArmor(name='Рваная одежда', defence=0)
mage_robe = CommonArmor(name='Роба мага', defence=5)
warrior_armor = CommonArmor(name='Доспех воина', defence=10)
