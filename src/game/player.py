from src.game.upgrade import *


class Player:
    def __init__(self, name):
        self.reset()
        self.name = name

    def reset(self):
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

    def use_item(self):
        pass


class NotEnoughCoinsException(Exception):
    pass
