import unittest
from functools import partial

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
        self.assertEqual([self.game._players[username].cookies for username in self.game._players], [3, 3, 3])
        self.assertTrue(self.game.ongoing)

    def test_clicks_existing_user(self):
        nb_players = 3
        self.create_players(nb_players)
        self.game.pregame_setup()

        self.game.click('player0')
        self.game.click('player0')

        self.assertEqual(len(self.game.players_alive()), nb_players)
        self.assertEqual([self.game._players[username].cookies for username in self.game._players], [2, 0, 0])

    def test_clicks_non_existent_user(self):
        nb_players = 3
        self.create_players(nb_players)
        self.game.pregame_setup()

        self.assertRaises(NonExistentUserException, partial(self.game.click, 'player3'))

    def test_click_and_ticks(self):
        nb_turns = 3
        nb_players = 3
        self.create_players(nb_players)
        self.game.pregame_setup()

        for i in range(nb_turns):
            self.game.single_tick()

        self.game.click('player0')
        self.game.click('player1')
        self.game.click('player1')
        self.game.click('player1')

        self.assertEqual(len(self.game.players_alive()), nb_players)
        self.assertEqual([self.game._players[username].cookies for username in self.game._players], [4, 6, 3])

    def test_player_dies(self):
        nb_turns = 3
        nb_players = 3
        self.create_players(nb_players)
        self.game.pregame_setup()

        for i in range(nb_turns):
            self.game.single_tick()

        action = {
            'damage': 80
        }
        self.game.hit('player0', 'player1', action)
        self.assertEqual(self.game.players_alive(), ['player0', 'player2'])
        self.assertFalse(self.game._players['player1'].is_alive())

    def test_game_over_one_player_left(self):
        pass

    def test_game_over_tied_game(self):
        pass

    def test_dead_player_cant_hit(self):
        pass

    def test_dead_player_cant_click(self):
        pass

    def create_players(self, nb_players):
        for i in range(nb_players):
            self.game.add_player(f"player{i}")


if __name__ == '__main__':
    unittest.main()
