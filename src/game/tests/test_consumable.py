import unittest

from src.game.game import Game
from src.game.consumable import *


class TestConsumables(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.player = game.create_player("Player0")

    def test_buyPotion_notEnoughCoins(self):
        pass

    def test_buyPotion_enoughCoins(self):
        pass

    def test_useHealingPotion_noPotionsInInventory(self):
        pass

    def test_useHealingPotion_potionsInInventory(self):
        pass

    def test_useDamagePotion_noPotionsInInventory(self):
        pass

    def test_useDamagePotion_potionsInInventory(self):
        pass

if __name__ == '__main__':
    unittest.main()
