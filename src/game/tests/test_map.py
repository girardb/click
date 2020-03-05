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
            self.assertTrue(len(room.players) <= 1)

        for player in self.game._players.values():
            self.assertTrue(player.current_room is not None)

    def test_every_starting_area_is_not_connected_to_another_starting_area1(self):
        for room in self.game.map.rooms:
            if room.room_difficulty == 'starting_area':
                for connected_room in room.neighboring_rooms:
                    self.assertNotEqual(connected_room.room_difficulty, 'starting_area')

    def test_every_starting_area_is_not_connected_to_another_starting_area2(self):
        for room in self.game.map.rooms:
            if room.players:
                for connected_room in room.neighboring_rooms:
                    self.assertEqual(connected_room.players, set())

    def test_at_game_start_all_players_are_placed_in_starting_areas(self):
        for player in self.game._players.values():
            self.assertEqual(player.current_room.room_difficulty, 'starting_area')

    def test_no_isolated_rooms(self):
        queue = [self.game.map.rooms[0]]
        visited_rooms = set()
        while queue:
            room = queue.pop()
            visited_rooms.add(room)
            for connected_room in room.neighboring_rooms:
                if connected_room not in visited_rooms:
                    queue.append(connected_room)

        self.assertEqual(len(visited_rooms), len(self.game.map.rooms))

    def test_every_starting_area_is_the_same(self):
        starting_areas = list(filter(lambda room: room.room_difficulty == 'starting_area', self.game.map.rooms))

        nb_players = [len(room.players) for room in starting_areas]
        self.assertTrue(len(set(nb_players)) == 1)

        click_bonuses = [room.click_bonus for room in starting_areas]
        self.assertTrue(len(set(click_bonuses)) == 1)

        income_bonuses = [room.income_bonus for room in starting_areas]
        self.assertTrue(len(set(income_bonuses)) == 1)

        room_sizes = [room.room_size for room in starting_areas]
        self.assertTrue(len(set(room_sizes)) == 1)


if __name__ == '__main__':
    unittest.main()
