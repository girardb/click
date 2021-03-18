from src.game.game import *
from src.game.driver import Driver
from src.game.tests.test_game import create_players

import unittest
from unittest.mock import patch, Mock


@patch("time.sleep", Mock())
class TestDrivingGame(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.driver = Driver(game)

    def test_game_is_over(self):
        create_players(self.driver.game, 3)
        self.driver.start_game()
        self.assertFalse(self.driver.game.ongoing)


if __name__ == '__main__':
    unittest.main()
