class Upgrade:
    def __init__(self):
        self.cost = 1
        self.upgrade = 1

    def buy(self):
        raise NotImplementedError()

    def upgrade(self):
        raise NotImplementedError()


class Consumable:
    def __init__(self):
        self.cost = 1
        self.effect = 1

    def buy(self):
        raise NotImplementedError()

    def use(self):
        raise NotImplementedError()
