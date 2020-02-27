from src.game.game import *
from src.game.driver import TestDriver

import unittest


class TestDrivingGame(unittest.TestCase):
    def setUp(self) -> None:
        game = Game()
        self.driver = TestDriver(game)


if __name__ == '__main__':
    unittest.main()
