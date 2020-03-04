import unittest
from src.game.room import *


class TestRoom(unittest.TestCase):
    def setUp(self) -> None:
        # create a game and get a room
        pass

    def test_bonus_correctly_applied_to_player_inside_room(self):
        pass

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
