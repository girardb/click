# TODO: Damage from consumables is not added to player.total_damage_dealt


class Consumable:
    def __init__(self, name, cost, effect):
        self.name = name
        self.cost = cost
        self.effect = effect
        self.item_count = 0

    def buy(self, player):
        player.cookies -= self.cost
        self.item_count += 1

    def use(self, target):
        raise NotImplementedError()


class HealingPotion(Consumable):
    def use(self, target):
        target.hp += self.effect
        if target.hp > target.max_hp:
            target.hp = target.max_hp

        self.item_count -= 1


class DamagePotion(Consumable):
    def use(self, target):
        target.hp += self.effect
        if target.hp < 0:
            target.hp = 0

        self.item_count -= 1


class ItemNotInInventoryException(Exception):
    pass