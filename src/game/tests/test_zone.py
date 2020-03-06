import unittest
from src.game.game import *


class TestZone(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.player0 = self.game.create_player('player0')
        self.player1 = self.game.create_player('player1')
        self.game.add_player(self.player0)
        self.game.add_player(self.player1)
        self.game.start_game()

    def test_all_but_final_room_are_affected(self):
        self.game.map.zone.distance_to_be_affected = 1
        self.game.map.zone.affect_rooms()

        for room in self.game.map.rooms:
            if room == self.game.map.zone.final_room:
                self.assertFalse(room.isInZone)
            else:
                self.assertTrue(room.isInZone)

    def test_all_rooms_are_affected(self):
        self.game.map.zone.distance_to_be_affected = 0
        self.game.map.zone.affect_rooms()

        for room in self.game.map.rooms:
            self.assertTrue(room.isInZone)

    # Unless the map is really big
    def test_no_room_is_affected(self):
        self.game.map.zone.distance_to_be_affected = float('inf')
        self.game.map.zone.affect_rooms()

        for room in self.game.map.rooms:
            self.assertFalse(room.isInZone)

    # # Create a dummy map and test the distances on it
    # def test_verify_bfs_distance(self):
    #     # test for multiple distances -> for i in range(20)
    #     pass


if __name__ == '__main__':
    unittest.main()
