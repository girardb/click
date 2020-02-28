import unittest

from src.game.game import Game
from src.game.upgrade import *


class TestUpgrades(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.player = game.create_player("Player0")

    def test_click_noUpgrades(self):
        pass

    def test_click_withUpgrades(self):
        pass

    def test_income_noUpgrade(self):
        pass

    def test_income_withUpgrades(self):
        pass

    def test_buyUpgrade_notEnoughCoins(self):
        pass

    def test_buyUpgrade_enoughCoins(self):
        pass

    def test_buyUpgrade_notBought(self):
        pass

    def test_buyUpgrade_alreadyBought(self):
        pass

    def test_levelUpUpgrade_upgradeNotBought(self):
        pass

    def test_levelUpUpgrade_upgradeBought(self):
        pass


if __name__ == '__main__':
    unittest.main()
