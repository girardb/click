import unittest
from src.game.game import *


class TestTypicalGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_no_players(self):
        self.assertRaises(EmptyGameException, self.game.pregame_setup)

    def test_regular_ticks(self):
        nb_players = 3
        nb_turns = 3
        self.create_players(nb_players)
        self.game.pregame_setup()

        for i in range(nb_turns):
            self.game.single_tick()

        self.assertEqual(len(self.game.players_alive()), nb_players)
        self.assertEqual([self.game._players[username].cookies for username in self.game._players], [3 for i in range(nb_players)])
        self.assertTrue(self.game.ongoing)

    def create_players(self, nb_players):
        for i in range(nb_players):
            self.game.add_player(f"player{i}")


if __name__ == '__main__':
    unittest.main()
