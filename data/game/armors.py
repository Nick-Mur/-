class CommonArmor:
    def __init__(self, defence, name):
        self.defence = defence
        self.name = name

    def check_armor(self):
        text = [f'БРОНЯ\n',
                f'Название: {self.name}\n'
                f'Показатель защиты: {self.defence}']
        return text


peasants_robe = CommonArmor(name='Роба', defence=5)
tattered_clothing = CommonArmor(name='Рваная одежда', defence=0)
