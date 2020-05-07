from src.game.game import *
from src.game.driver import Driver
from src.game.tests.test_game import create_players

import unittest


class TestDrivingGame(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.driver = TestDriver(game)

    def test_game_is_over(self):
        create_players(self.driver.game, 3)
        self.driver.start_game()
        self.assertFalse(self.driver.game.ongoing)


class TestDriver(Driver):
    """
    Runs game for tests
    """
    def _play_game(self):
        while self.game.custom_tick():
            pass


if __name__ == '__main__':
    unittest.main()
