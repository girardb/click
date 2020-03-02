# TODO: fix/ the upgrade needs to be aware of who buys it


class Upgrade:
    def __init__(self, name, cost, increase, cost_hike_ratio):
        self.name = name
        self.cost = cost
        self.base_increase = increase
        self.cost_hike_ratio = cost_hike_ratio
        self.level = 0
        self.increase = increase
        self.bought = False

    def buy(self):
        if self.bought:
            raise AlreadyBoughtException("You have already bought this item.")
        self.bought = True

    def upgrade(self):
        raise NotImplementedError()


class IncomeUpgrade(Upgrade):
    def upgrade(self):
        self.increase += self.base_increase
        self.level += 1
        self.cost *= self.cost_hike_ratio


class ClickUpgrade(Upgrade):
    def upgrade(self):
        self.increase += self.base_increase
        self.level += 1
        self.cost *= self.cost_hike_ratio


class AlreadyBoughtException(Exception):
    pass


class NotBoughtException(Exception):
    pass
