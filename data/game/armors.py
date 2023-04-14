class CommonArmor:
    def __init__(self, defence):
        self.defence = defence

    def check_armor(self):
        return f'показатель брони: {self.defence}'


peasants_robe = CommonArmor(5)
