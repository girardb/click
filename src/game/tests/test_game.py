import unittest
from src.game.game import *


class TestTypicalGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_empty_game(self):
        self.assertRaises(EmptyGameException, self.game.start_game)

    def create_couple_players(self):
        self.game.add_player('player1')
        self.game.add_player('player2')
        self.game.add_player('player3')


if __name__ == '__main__':
    unittest.main()
