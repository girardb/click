import unittest
from src.game.player import *
from src.game.game import *
from functools import partial


class TestRoom(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.player0 = Player('player0')
        self.player1 = Player('player1')
        self.game.add_player(self.player0)
        self.game.add_player(self.player1)
        self.game.start_game()

    # Using this method, a user is present in two rooms at once
    def test_add_player(self):
        room = self.player0.current_room
        room._add_player(self.player1)

        self.assertEqual(len(room.players), 2)
        self.assertTrue(self.player0 in room.players)
        self.assertTrue(self.player1 in room.players)

    # Using this method, a user is currently in the game but not not in a room
    def test_remove_player(self):
        room = self.player0.current_room
        room.remove_player(self.player0)

        self.assertEqual(len(room.players), 0)
        self.assertTrue(self.player0 not in room.players)

    def test_connect_two_rooms(self):
        room1 = self.player0.current_room
        room2 = self.player1.current_room

        room1.connect_with(room2)

        self.assertTrue(room1 in room2.neighboring_rooms)
        self.assertTrue(room2 in room1.neighboring_rooms)

    def test_bonus_correctly_applied_to_player_inside_room(self):
        self.assertEqual(self.player0.get_income(), self.player0.base_income + self.player0.current_room.income_bonus)
        self.assertEqual(self.player0.get_click_value(), self.player0.base_click_value + self.player0.current_room.click_bonus)

    def test_a_player_can_only_see_the_players_in_his_room(self):
        self.player1.enter_room(self.player0.current_room)

        surrounding_players = self.player0.get_surrounding_players()

        for player in surrounding_players:
            self.assertEqual(player.current_room, self.player0.current_room)

        self.assertEqual(len(self.player0.current_room.players), 2)

    def test_a_player_can_only_interact_with_the_players_in_his_room__hits_throws(self):
        self.assertRaises(PlayerNotInRoomException, partial(self.player0.hits, self.player1, 10))

    def test_a_player_can_only_interact_with_the_players_in_his_room__consumable_throws(self):
        for i in range(10):
            self.player0.click()
        self.player0.buy_item(self.player0.consumables['Potion']['Damage'])

        self.assertRaises(PlayerNotInRoomException, partial(self.player0.use_item, self.player0.consumables['Potion']['Damage'], self.player1))

    def test_a_player_can_only_interact_with_the_players_in_his_room__hits_works(self):
        self.player1.enter_room(self.player0.current_room)

        self.player0.hits(self.player1, 10)

        self.assertEqual(self.player1.hp, self.player1.max_hp - 10)

    def test_a_player_can_only_interact_with_the_players_in_his_room__consumable_works(self):
        self.player1.enter_room(self.player0.current_room)
        for i in range(10):
            self.player0.click()
        self.player0.buy_item(self.player0.consumables['Potion']['Damage'])

        self.player0.use_item(self.player0.consumables['Potion']['Damage'], self.player1)

        self.assertEqual(self.player1.hp, self.player1.max_hp + self.player0.consumables['Potion']['Damage'].effect)

    def test_player_enters_room(self):
        old_room = self.player0.current_room
        new_room = [room for room in self.player0.current_room.neighboring_rooms][0]

        self.player0.enter_room(new_room)

        self.assertEqual(self.player0.current_room, new_room)
        self.assertNotEqual(self.player0.current_room, old_room)

    # def test_discoverRoom_undiscoveredRoom_givesBonus(self):
    #     pass
    #
    # def test_discoverRoom_discoveredRoom_doesnt_give_bonus(self):
    #     pass
    #
    # def test_player_enters_full_room(self):
    #     pass
    #
    # def test_player_unfilled_room(self):
    #     pass
    #
    # def test_lock_room(self):
    #     pass
    #
    # def test_unlock_room(self):
    #     pass
    #
    # def test_place_furniture_in_an_unfilled_room(self):
    #     pass
    #
    # def test_place_furniture_in_a_filled_room_throws(self):
    #     pass
    # Should add that you need to be in an adjacent room to be able to enter it
    # Should add that you can't enter the room you're already in


if __name__ == '__main__':
    unittest.main()
