class Upgrade:
    def __init__(self, name, cost, increase):
        self.name = name
        self.cost = cost
        self.increase = increase
        self.level = 0
        self.bought = False

    def buy(self):
        raise NotImplementedError()

    def upgrade(self):
        raise NotImplementedError()


class IncomeUpgrade(Upgrade):
    pass


class ClickUpgrade(Upgrade):
    pass