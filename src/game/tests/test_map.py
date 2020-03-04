import unittest
from src.game.game import *
from src.game.map import *
from src.game.tests.test_game import create_players


class TestMap(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        create_players(self.game, 3)
        self.game.start_game()

    def test_at_game_start_every_player_is_placed_in_a_room_and_is_alone(self):
        for room in self.game.map.rooms:
            self.assertTrue(len(room.get_players()) <= 1)

        for player in self.game._players:
            self.assertTrue(player.room is not None)

    def test_every_starting_area_is_not_connected_to_another_starting_area(self):
        pass

    def test_number_of_rooms_is_appropriate_for_number_of_players(self):
        pass

    def test_every_starting_area_is_the_same(self):
        pass

    def test_all_rooms_are_reachable(self):
        pass


if __name__ == '__main__':
    unittest.main()
