import random

from src.game.room import Room


class Map:
    def __init__(self, players, rooms_per_player=3, room_connections=2):
        self.rooms_per_player = rooms_per_player
        self.nb_generate_room_connections = room_connections
        self.rooms = self.generate_rooms(players)
        self.connect_rooms()

    # Ugly code
    # Add tests
    def generate_rooms(self, players):
        nb_players = len(players)
        nb_starting_area_rooms = nb_players
        nb_other_rooms = self.rooms_per_player * nb_players - nb_players
        rooms = []

        for i in range(nb_starting_area_rooms):
            room_difficulty = 'starting_area'
            room = Room(room_difficulty)
            room.add_player(players[i])
            rooms.append(room)

        for i in range(nb_other_rooms):
            room_difficulty = random.choice(['medium_area', 'hard_area'])
            rooms.append(Room(room_difficulty))

        return rooms

    # Duplicate code
    # Add tests
    def connect_rooms(self):
        other_rooms = list(filter(lambda room: room.type != 'starting_area', self.rooms))
        for room in self.rooms:
            if room.type == 'starting_area':
                connections = random.sample(other_rooms, self.nb_generate_room_connections)
                for other_room in connections:
                    room.add_neighboring_room(other_room)

            else:
                connections = random.sample(self.rooms, self.nb_generate_room_connections)
                for other_room in connections:
                    room.add_neighboring_room(other_room)

