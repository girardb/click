# TODO: fix/ the upgrade needs to be aware of who buys it


class Upgrade:
    def __init__(self, name, cost, increase, cost_hike_ratio):
        self.name = name
        self.cost = cost
        self.increase = increase
        self.cost_hike_ratio = cost_hike_ratio
        self.level = 0
        self.bought = False

    def buy(self, player):
        if self.bought:
            raise AlreadyBoughtException("You have already bought this item.")

        self.bought = True
        self.upgrade(player)

    def upgrade(self, player):
        raise NotImplementedError()


class IncomeUpgrade(Upgrade):
    def upgrade(self, player):
        player.income += self.increase
        player.cookies -= self.cost
        self.level += 1
        self.cost *= self.cost_hike_ratio


class ClickUpgrade(Upgrade):
    def upgrade(self, player):
        player.click_value += self.increase
        player.cookies -= self.cost
        self.level += 1
        self.cost *= self.cost_hike_ratio


class AlreadyBoughtException(Exception):
    pass


class NotBoughtException(Exception):
    pass
