import unittest

from functools import partial

from src.game.game import Game
from src.game.player import NotEnoughCoinsException
from src.game.consumable import *


class TestConsumables(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.player = game.create_player("Player0")

    def test_initialize_consumables(self):
        self.assertTrue(self.player.consumables)
        self.assertTrue(self.player.consumables['Potion'])
        self.assertTrue(self.player.consumables['Potion']['Healing'])
        self.assertTrue(self.player.consumables['Potion']['Damage'])

        self.assertFalse(self.player.consumables['Potion']['Healing'].item_count, 0)

    def test_buyPotion_notEnoughCoins(self):
        self.assertRaises(NotEnoughCoinsException, partial(self.player.buy_item, self.player.consumables['Potion']['Healing']))

    def test_buyPotion_enoughCoins(self):
        self.get_money(10)

        self.player.buy_item(self.player.consumables['Potion']['Healing'])

        self.assertEqual(self.player.cookies, 0)
        self.assertEqual(self.player.consumables['Potion']['Healing'].item_count, 1)

    def test_useHealingPotion_noPotionsInInventory(self):
        self.assertRaises(ItemNotInInventoryException, partial(self.player.use_item, self.player.consumables['Potion']['Healing'], self.player))

    def test_useHealingPotion_potionsInInventory(self):
        self.get_money(10)
        self.player.buy_item(self.player.consumables['Potion']['Healing'])
        self.player.get_hit(20)

        self.assertEqual(self.player.hp, 80)

        self.player.use_item(self.player.consumables['Potion']['Healing'], self.player)

        self.assertEqual(self.player.hp, 90)
        self.assertEqual(self.player.consumables['Potion']['Healing'].item_count, 0)

    def test_useHealingPotion_dontOverheal(self):
        self.get_money(10)
        self.player.buy_item(self.player.consumables['Potion']['Healing'])
        self.player.get_hit(5)

        self.assertEqual(self.player.hp, 95)

        self.player.use_item(self.player.consumables['Potion']['Healing'], self.player)

        self.assertEqual(self.player.hp, 100)
        self.assertEqual(self.player.consumables['Potion']['Healing'].item_count, 0)

    def test_useDamagePotion_noPotionsInInventory(self):
        self.assertRaises(ItemNotInInventoryException, partial(self.player.use_item, self.player.consumables['Potion']['Damage'], self.player))

    def test_useDamagePotion_potionsInInventory(self):
        self.get_money(10)
        self.player.buy_item(self.player.consumables['Potion']['Damage'])
        self.assertEqual(self.player.hp, 100)

        self.player.use_item(self.player.consumables['Potion']['Damage'], self.player)

        self.assertEqual(self.player.hp, 90)
        self.assertEqual(self.player.consumables['Potion']['Damage'].item_count, 0)

    def test_useDamagePotion_dontOverkill(self):
        self.get_money(10)
        self.player.buy_item(self.player.consumables['Potion']['Damage'])
        self.player.get_hit(95)
        self.assertEqual(self.player.hp, 5)

        self.player.use_item(self.player.consumables['Potion']['Damage'], self.player)

        self.assertEqual(self.player.hp, 0)
        self.assertEqual(self.player.consumables['Potion']['Damage'].item_count, 0)
        self.assertFalse(self.player.is_alive())

    def get_money(self, amount):
        for i in range(amount):
            self.player.click()

if __name__ == '__main__':
    unittest.main()
