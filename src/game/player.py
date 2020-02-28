from src.game.upgrade import *
from src.game.consumable import *


class Player:
    def __init__(self, name):
        self.reset()
        self.name = name

    def reset(self):
        self.max_hp = 100
        self.hp = 100
        self.income = 1
        self.cookies = 0
        self.click_value = 1
        self.bleed_amount = 20
        self.total_damage_dealt = 0

        self.upgrades = {
            'Income': {
                'Bronze': IncomeUpgrade('Bronze Income Upgrade', 15, 1, 1.5)
            },
            'Click': {
                'Bronze': ClickUpgrade('Bronze Click Upgrade', 15, 1, 1.5)
                      }
        }

        self.consumables = {
            'Potion': {
                'Healing': HealingPotion('Healing Potion', 10, 10),
                'Damage': DamagePotion('Damage Potion', 10, -10)
            }
        }

    def is_alive(self):
        return self.hp > 0

    def income_tick(self):
        self.cookies += self.income

    def click(self):
        self.cookies += self.click_value

    def bleed(self):
        self.hp -= self.bleed_amount

    def get_hit(self, damage):
        self.hp -= damage

    def hits(self, damage):
        self.total_damage_dealt += damage

    def buy_item(self, item):
        if self.cookies < item.cost:
            raise NotEnoughCoinsException(f"Not enough coins to buy {item.name}.")
        item.buy(self)

    def upgrade(self, upgrade):
        if not upgrade.bought:
            raise NotBoughtException("You need to buy the upgrade before upgrading it.")
        upgrade.upgrade(self)

    def use_item(self, item, target):
        if item.item_count <= 0:
            raise ItemNotInInventoryException("This item is not in your inventory.")
        item.use(target)


class NotEnoughCoinsException(Exception):
    pass
