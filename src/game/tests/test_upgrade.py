import unittest

from functools import partial

from src.game.game import Game
from src.game.upgrade import *
from src.game.player import *


class TestUpgrades(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.player = game.create_player("Player0")
        player1 = game.create_player('Player1')
        game.add_player(self.player)
        game.add_player(player1)
        game.start_game()

    def test_initialize_upgrades(self):
        self.assertTrue(self.player.upgrades)
        self.assertTrue(self.player.upgrades['Income'])
        self.assertTrue(self.player.upgrades['Click'])

        self.assertFalse(self.player.upgrades['Income']['Bronze'].bought)

    def test_buyUpgrade_notEnoughCoins(self):
        self.assertRaises(NotEnoughCoinsException, partial(self.player.buy_item, self.player.upgrades['Income']['Bronze']))

    def test_buyUpgrade_enoughCoins(self):
        for i in range(15):
            self.player.click()

        self.player.buy_item(self.player.upgrades['Income']['Bronze'])

        self.assertTrue(self.player.upgrades['Income']['Bronze'].bought)

    def test_buyUpgrade_alreadyBought(self):
        for i in range(50):
            self.player.click()
        self.player.buy_item(self.player.upgrades['Income']['Bronze'])

        self.assertRaises(AlreadyBoughtException, partial(self.player.buy_item, self.player.upgrades['Income']['Bronze']))

    def test_levelUpUpgrade_upgradeNotBought(self):
        for i in range(50):
            self.player.click()

        self.assertRaises(NotBoughtException, partial(self.player.upgrade, self.player.upgrades['Income']['Bronze']))

    def test_levelUpUpgrade_upgradeBought(self):
        for i in range(50):
            self.player.click()
        self.player.buy_item(self.player.upgrades['Income']['Bronze'])

        self.player.upgrade(self.player.upgrades['Income']['Bronze'])

        self.assertEqual(self.player.get_income(), 2 + self.player.base_income + self.player.current_room.income_bonus)

    def test_click_noUpgrades(self):
        self.player.click()

        self.assertEqual(self.player.coins, self.player.base_click_value + self.player.current_room.click_bonus)
        self.assertEqual(self.player.get_click_value(), self.player.base_click_value + self.player.current_room.click_bonus)

    def test_click_withUpgrades(self):
        for i in range(15):
            self.player.click()
        self.player.buy_item(self.player.upgrades['Click']['Bronze'])

        # Reset coins
        self.player.coins = 0

        self.player.click()

        self.assertEqual(self.player.coins, 1 + self.player.base_click_value + self.player.current_room.click_bonus)
        self.assertEqual(self.player.get_click_value(), 1 + self.player.base_click_value + self.player.current_room.click_bonus)

    def test_income_noUpgrade(self):
        self.player.income_tick()

        self.assertEqual(self.player.coins, self.player.base_income + self.player.current_room.income_bonus)
        self.assertEqual(self.player.get_income(), self.player.base_income + self.player.current_room.income_bonus)

    def test_income_withUpgrades(self):
        for i in range(15):
            self.player.click()
        self.player.buy_item(self.player.upgrades['Income']['Bronze'])

        # Reset coins
        self.player.coins = 0

        self.player.income_tick()

        self.assertEqual(self.player.coins, 1 + self.player.base_income + self.player.current_room.income_bonus)
        self.assertEqual(self.player.get_income(), 1 + self.player.base_income + self.player.current_room.income_bonus)


if __name__ == '__main__':
    unittest.main()
