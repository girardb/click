import unittest
from src.game.room import *
from src.game.player import *
from src.game.game import *


class TestRoom(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.player0 = Player('player0')
        self.player1 = Player('player1')
        self.game.add_player(self.player0)
        self.game.add_player(self.player1)
        self.game.start_game()

    def test_bonus_correctly_applied_to_player_inside_room(self):
        self.assertEqual(self.player0.get_income(), self.player0.base_income + self.player0.current_room.income_bonus)
        self.assertEqual(self.player0.get_click_value(), self.player0.base_click_value + self.player0.current_room.click_bonus)

    def test_a_player_can_only_see_the_players_in_his_room(self):
        pass

    def test_a_player_can_only_interact_with_the_players_in_his_room(self):
        pass

    def test_discoverRoom_undiscoveredRoom_givesBonus(self):
        pass

    def test_discoverRoom_discoveredRoom_doesnt_give_bonus(self):
        pass

    def test_player_enters_full_room(self):
        pass

    def test_player_unfilled_room(self):
        pass

    def test_player_enters_room(self):
        old_room = self.player0.current_room
        new_room = [room for room in self.player0.current_room.neighboring_rooms][0]

        self.player0.enter_room(new_room)

        self.assertEqual(self.player0.current_room, new_room)
        self.assertNotEqual(self.player0.current_room, old_room)

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


if __name__ == '__main__':
    unittest.main()
