import unittest
from functools import partial

from src.game.game import *


class TestTypicalGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        nb_players = 3
        create_players(self.game, nb_players)
        self.game.start_game()
        for player in self.game._players.values():
            player.enter_room(self.game._players['player0'].current_room)

    def test_one_player(self):
        self.game = Game()
        create_players(self.game, 1)
        self.assertRaises(EmptyGameException, self.game.start_game)

    def test_regular_ticks(self):
        nb_turns = 3

        for i in range(nb_turns):
            self.game.single_tick()

        self.assertEqual(len(self.game.players_alive()), 3)
        self.assertEqual([player.coins for player in self.game._players.values()], [nb_turns*(1 + player.current_room.income_bonus) for player in self.game._players.values()])
        self.assertTrue(self.game.ongoing)

    def test_clicks_existing_user(self):
        self.game.click('player0')
        self.game.click('player0')

        self.assertEqual(len(self.game.players_alive()), 3)
        self.assertEqual([player.coins for player in self.game._players.values()], [2*(1 + self.game._players['player0'].current_room.click_bonus), 0, 0])

    def test_clicks_non_existent_user(self):
        self.assertRaises(NonExistentUserException, partial(self.game.click, 'player3'))

    def test_clicks_and_ticks(self):
        nb_turns = 3

        for i in range(nb_turns):
            self.game.single_tick()

        self.game.click('player0')
        self.game.click('player1')
        self.game.click('player1')
        self.game.click('player1')

        self.assertEqual(len(self.game.players_alive()), 3)
        self.assertEqual([player.coins for player in self.game._players.values()],
                         [
                             nb_turns*(1 + self.game._players['player0'].current_room.income_bonus) + 1*(1 + self.game._players['player0'].current_room.click_bonus),
                             nb_turns*(1 + self.game._players['player1'].current_room.income_bonus) + 3*(1 + self.game._players['player1'].current_room.click_bonus),
                             nb_turns*(1 + self.game._players['player2'].current_room.income_bonus) + 0*(1 + self.game._players['player2'].current_room.click_bonus),
                         ])

    def test_player_dies(self):
        nb_turns = 3

        for i in range(nb_turns):
            self.game.single_tick()

        action = {
            'damage': 100
        }
        self.game.hit('player0', 'player1', action)
        self.assertEqual([player.name for player in self.game.players_alive()], ['player0', 'player2'])
        self.assertFalse(self.game._players['player1'].is_alive())

    def test_reset_players(self):
        action = {
            'damage': 50
        }
        self.game.hit('player0', 'player1', action)
        self.game.single_tick()
        self.game.reset_players()

        self.assertTrue(all(True if player.hp == 100 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.base_income == 1 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.coins == 0 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.base_click_value == 1 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.bleed_amount == 0 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.total_damage_dealt == 0 else False for player in self.game._players.values()))
        self.assertTrue(all(True if player.current_room is None else False for player in self.game._players.values()))
        self.assertTrue(all(True if all_items_arent_bought(player) else False for player in self.game._players.values()))

    def test_add_player(self):
        self.game = Game()
        username = 'Player0'
        player = self.game.create_player(username)
        self.game.add_player(player)

        self.assertTrue(len(self.game._players) == 1)
        self.assertEqual(self.game._players[username], player)

    def test_zone_shrinks_over_time(self):
        zone_range = self.game.map.zone.distance_to_be_affected
        for i in range(59):
            self.game.single_tick()
        self.assertEqual(self.game.map.zone.distance_to_be_affected, zone_range)

        self.game.single_tick()
        self.assertEqual(self.game.map.zone.distance_to_be_affected, zone_range-1)

    def test_tied_game(self):
        player0_room = self.game._players['player0'].current_room
        for player in self.game._players.values():
            player.enter_room(player0_room)

        while self.game.single_tick():
            pass

        self.assertEqual(len(self.game.players_alive()), 0)
        self.assertFalse(self.game.ongoing)

    def test_game_won(self):
        final_room = self.game.map.zone.final_room
        neighbor_room = list(final_room.neighboring_rooms)[0]
        for player in self.game._players.values():
            player.enter_room(neighbor_room)
        self.game._players['player0'].enter_room(final_room)

        while self.game.single_tick():
            pass

        self.assertEqual(len(self.game.players_alive()), 1)
        self.assertEqual(self.game.players_alive()[0], self.game._players['player0'])
        self.assertFalse(self.game.ongoing)

    # def test_game_over_one_player_left(self):
    #     pass
    #
    # def test_game_over_tied_game(self):
    #     pass
    #
    # def test_dead_player_cant_hit(self):
    #     pass
    #
    # def test_dead_player_cant_click(self):
    #     pass


def create_players(game, nb_players):
    for i in range(nb_players):
        player = game.create_player(f"player{i}")
        game.add_player(player)


def all_items_arent_bought(player):
    income_items = list(player.upgrades['Income'].values())
    click_items = list(player.upgrades['Click'].values())
    items = income_items + click_items
    return all(True if item.bought is False else False for item in items)


if __name__ == '__main__':
    unittest.main()
