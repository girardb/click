import random


class Room:
    def __init__(self, room_difficulty):
        self.type = type
        self.click_bonus, self.income_bonus, self.room_size = self.get_room_data_from_difficulty(room_difficulty)

        self.players = set()
        self.neighboring_rooms = set()
        self.discovered = False

    # Add test
    def add_player(self, player):
        self.players.add(player)

    # Add test
    def remove_player(self, player):
        self.players.remove(player)

    # Add test
    def add_neighboring_room(self, other_room):
        self.neighboring_rooms.add(other_room)

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

