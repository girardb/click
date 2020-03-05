from src.game.upgrade import *
from src.game.consumable import *


class Player:
    def __init__(self, name):
        self.reset()
        self.name = name

    def reset(self):
        self.max_hp = 100
        self.hp = 100
        self.base_income = 1
        self.coins = 0
        self.base_click_value = 1
        self.bleed_amount = 20
        self.total_damage_dealt = 0
        self.current_room = None
        self.visited_rooms = set()

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

    def get_click_value(self):
        item_click_value = sum(item.increase if item.bought else 0 for item in self.upgrades['Click'].values())
        room_click_value = self.current_room.click_bonus
        return self.base_click_value + item_click_value + room_click_value

    def get_income(self):
        upgrade_income = sum(item.increase if item.bought else 0 for item in self.upgrades['Income'].values())
        room_income = self.current_room.income_bonus
        return self.base_income + upgrade_income + room_income

    def income_tick(self):
        self.coins += self.get_income()

    def click(self):
        self.coins += self.get_click_value()

    def bleed(self):
        self.hp -= self.bleed_amount

    def get_hit(self, damage):
        self.hp -= damage

    def hits(self, damage):
        self.total_damage_dealt += damage

    def buy_item(self, item):
        if self.coins < item.cost:
            raise NotEnoughCoinsException(f"Not enough coins to buy {item.name}.")
        self.coins -= item.cost
        item.buy()

    def upgrade(self, upgrade):
        if not upgrade.bought:
            raise NotBoughtException("You need to buy the upgrade before upgrading it.")
        self.coins -= upgrade.cost
        upgrade.upgrade()

    def use_item(self, item, target):
        if item.item_count <= 0:
            raise ItemNotInInventoryException("This item is not in your inventory.")
        item.use(target)

    def enter_room(self, room):
        if self.current_room is not None:
            self.current_room.remove_player(self)
        self.current_room = room
        self.current_room.add_player(self)
        self.visited_rooms.add(self.current_room)


class NotEnoughCoinsException(Exception):
    pass
