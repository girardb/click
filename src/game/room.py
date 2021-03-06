import random


class Room:
    def __init__(self, room_difficulty):
        self.room_difficulty = room_difficulty
        self.click_bonus, self.income_bonus, self.room_size = self.get_room_data_from_difficulty(room_difficulty)

        self.players = set()
        self.neighboring_rooms = set()
        self.discovered = False
        self.damage = 0

    def _add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.remove(player)

    def connect_with(self, other_room):
        self.neighboring_rooms.add(other_room)
        other_room.neighboring_rooms.add(self)

    # Add multiple tests
    @staticmethod
    def get_room_data_from_difficulty(room_difficulty):
        if room_difficulty == 'starting_area':
            click_bonus = 1
            income_bonus = 1
            room_size = 5

        elif room_difficulty == 'medium_area':
            click_bonus = 1
            income_bonus = 1
            room_size = 5

        elif room_difficulty == 'hard_area':
            click_bonus = 1
            income_bonus = 1
            room_size = 5

        else:
            raise Exception("Invalid Room Type")

        return click_bonus, income_bonus, room_size

