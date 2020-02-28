class Consumable:
    def __init__(self, name, cost, effect):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.item_count = 0

    def buy(self):
        raise NotImplementedError()

    def use(self):
        raise NotImplementedError()


class HealingPotion(Consumable):
    pass


class DamagePotion(Consumable):
    pass
