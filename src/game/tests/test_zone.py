import unittest


class TestZone(unittest.TestCase):
    def test_all_but_final_room_are_affected(self):
        self.assertEqual(True, False)

    def test_all_rooms_are_affected(self):
        pass

    # Unless the map is really big
    def test_no_room_is_affected(self):
        pass

    def test_verify_bfs_distance1(self):
        # test for multiple distances -> for i in range(20)
        pass


if __name__ == '__main__':
    unittest.main()
