import unittest

from src.game.game import *


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

        name0 = "Player0"
        name1 = "Player1"
        self.player = Player(name0)
        self.player1 = Player(name1)

        self.game.add_player(self.player)
        self.game.add_player(self.player1)
        self.game.start_game()
        self.player1.enter_room(self.player.current_room)

    def test_init(self):
        self.assertEqual(self.player.name, "Player0")
        self.assertEqual(self.player.hp, 100)
        self.assertEqual(self.player.base_income, 1)
        self.assertEqual(self.player.coins, 0)
        self.assertEqual(self.player.base_click_value, 1)
        self.assertEqual(self.player.bleed_amount, 0)
        self.assertEqual(self.player.total_damage_dealt, 0)

    def test_reset(self):
        self.player.bleed()
        self.player.click()
        self.player.income_tick()
        self.player.get_hit(10)
        self.player.hits(self.player1, 10)

        self.player.reset()

        self.test_init()

    def test_income_tick(self):
        self.player.income_tick()

        self.assertEqual(self.player.coins, 1 + self.player.current_room.income_bonus)

    def test_bleed_damage_tick(self):
        self.player.bleed_amount = 10
        self.player.current_room.damage = 0
        self.player.bleed()

        self.assertEqual(self.player.hp, 90)

    def test_bleed_zone_tick(self):
        self.player.bleed_amount = 0
        self.player.current_room.damage = 20
        self.player.bleed()

        self.assertEqual(self.player.hp, 80)

    def test_bleed_zone_and_damage_tick(self):
        self.player.bleed_amount = 10
        self.player.current_room.damage = 20
        self.player.bleed()

        self.assertEqual(self.player.hp, 70)

    def test_click(self):
        self.player.click()

        self.assertEqual(self.player.coins, 1 + self.player.current_room.click_bonus)

    def test_dealt_damage(self):
        self.player.get_hit(10)

        self.assertEqual(self.player.hp, 90)

    def test_deals_damage(self):
        self.player.hits(self.player1, 10)

        self.assertEqual(self.player.total_damage_dealt, 10)

    def test_is_dead(self):
        self.player.get_hit(100)

        self.assertFalse(self.player.is_alive())

    def test_is_alive(self):
        self.assertTrue(self.player.is_alive())

    def test_player_knows_which_room_he_is_in(self):
        self.assertNotEqual(self.player.current_room, None)

    def test_player_knows_which_rooms_he_has_visited(self):
        visited_rooms = set()
        visited_rooms.add(self.player.current_room)

        for i in range(10):
            random_neighbor_room = random.sample(self.player.current_room.neighboring_rooms, 1)[0]
            self.player.enter_room(random_neighbor_room)
            visited_rooms.add(random_neighbor_room)

        self.assertEqual(self.player.visited_rooms, visited_rooms)

    def test_player_enters_room(self):
        old_room = self.player.current_room

        neighboring_room = [room for room in self.player.current_room.neighboring_rooms][0]

        self.player.enter_room(neighboring_room)

        self.assertEqual(self.player.current_room, neighboring_room)
        self.assertNotEqual(self.player.current_room, old_room)


if __name__ == '__main__':
    unittest.main()
