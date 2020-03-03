import unittest
from functools import partial

from src.game.game import *


class TestTypicalGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_one_player(self):
        create_players(self.game, 1)
        self.assertRaises(EmptyGameException, self.game.start_game)

    def test_regular_ticks(self):
        nb_players = 3
        nb_turns = 3
        create_players(self.game, nb_players)
        self.game.start_game()

        for i in range(nb_turns):
            self.game.single_tick()

        self.assertEqual(len(self.game.players_alive()), nb_players)
        self.assertEqual([self.game._players[username].coins for username in self.game._players], [3, 3, 3])
        self.assertTrue(self.game.ongoing)

    def test_clicks_existing_user(self):
        nb_players = 3
        create_players(self.game, nb_players)
        self.game.start_game()

        self.game.click('player0')
        self.game.click('player0')

        self.assertEqual(len(self.game.players_alive()), nb_players)
        self.assertEqual([self.game._players[username].coins for username in self.game._players], [2, 0, 0])

    def test_clicks_non_existent_user(self):
        nb_players = 3
        create_players(self.game, nb_players)
        self.game.start_game()

        self.assertRaises(NonExistentUserException, partial(self.game.click, 'player3'))

    def test_clicks_and_ticks(self):
        nb_turns = 3
        nb_players = 3
        create_players(self.game, nb_players)
        self.game.start_game()

        for i in range(nb_turns):
            self.game.single_tick()

        self.game.click('player0')
        self.game.click('player1')
        self.game.click('player1')
        self.game.click('player1')

        self.assertEqual(len(self.game.players_alive()), nb_players)
        self.assertEqual([self.game._players[username].coins for username in self.game._players], [4, 6, 3])

    def test_player_dies(self):
        nb_turns = 3
        nb_players = 3
        create_players(self.game, nb_players)
        self.game.start_game()

        for i in range(nb_turns):
            self.game.single_tick()

        action = {
            'damage': 100
        }
        self.game.hit('player0', 'player1', action)
        self.assertEqual([player.name for player in self.game.players_alive()], ['player0', 'player2'])
        self.assertFalse(self.game._players['player1'].is_alive())

    def test_reset_players(self):
        create_players(self.game, 3)
        self.game.start_game()

        action = {
            'damage': 50
        }
        self.game.hit('player0', 'player1', action)
        self.game.single_tick()
        self.game.reset_players()

        self.assertTrue(all(True if player.hp == 100 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.get_income() == 1 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.coins == 0 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.get_click_value() == 1 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.bleed_amount == 20 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.total_damage_dealt == 0 else False for player in self.game._players.values()))

    def test_add_player(self):
        username = 'Player0'
        player = self.game.create_player(username)
        self.game.add_player(player)

        self.assertTrue(len(self.game._players) == 1)
        self.assertEqual(self.game._players[username], player)

    def test_game_over_one_player_left(self):
        pass

    def test_game_over_tied_game(self):
        pass

    def test_dead_player_cant_hit(self):
        pass

    def test_dead_player_cant_click(self):
        pass


def create_players(game, nb_players):
    for i in range(nb_players):
        player = game.create_player(f"player{i}")
        game.add_player(player)


if __name__ == '__main__':
    unittest.main()
