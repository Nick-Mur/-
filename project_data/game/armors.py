class CommonArmor:
    def __init__(self, defence, name):
        self.defence = defence
        self.name = name

    def info(self):
        text = f'Название: {self.name}\n' \
               f'Показатель защиты: {self.defence}'
        return text


peasants_robe = CommonArmor(name='Роба', defence=5)
tattered_clothing = CommonArmor(name='Рваная одежда', defence=0)
mage_robe = CommonArmor(name='Роба мага', defence=5)
warrior_armor = CommonArmor(name='Доспех воина', defence=10)
armors = [peasants_robe, tattered_clothing, mage_robe, warrior_armor]