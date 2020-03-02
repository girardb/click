import unittest

from src.game.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        name = "Player0"
        self.player = Player(name)

    def test_init(self):
        self.assertEqual(self.player.name, "Player0")
        self.assertEqual(self.player.hp, 100)
        self.assertEqual(self.player.base_income, 1)
        self.assertEqual(self.player.cookies, 0)
        self.assertEqual(self.player.click_value, 1)
        self.assertEqual(self.player.bleed_amount, 20)
        self.assertEqual(self.player.total_damage_dealt, 0)

    def test_reset(self):
        self.player.bleed()
        self.player.click()
        self.player.income_tick()
        self.player.get_hit(10)
        self.player.hits(10)

        self.player.reset()

        self.test_init()

    def test_income_tick(self):
        self.player.income_tick()

        self.assertEqual(self.player.cookies, 1)

    def test_bleed_tick(self):
        self.player.bleed()

        self.assertEqual(self.player.hp, 80)

    def test_click(self):
        self.player.click()

        self.assertEqual(self.player.cookies, 1)

    def test_dealt_damage(self):
        self.player.get_hit(10)

        self.assertEqual(self.player.hp, 90)

    def test_deals_damage(self):
        self.player.hits(10)

        self.assertEqual(self.player.total_damage_dealt, 10)

    def test_is_dead(self):
        self.player.get_hit(100)

        self.assertFalse(self.player.is_alive())

    def test_is_alive(self):
        self.assertTrue(self.player.is_alive())


if __name__ == '__main__':
    unittest.main()
