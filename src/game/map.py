import random

from src.game.room import Room
from src.game.zone import Zone


class Map:
    def __init__(self, players, rooms_per_player=3, room_connections=2):
        self.rooms_per_player = rooms_per_player
        self.nb_generate_room_connections = room_connections
        self.rooms = self.generate_rooms(players)
        self.connect_rooms()
        self.zone = Zone(random.choice(self.rooms))

    def generate_rooms(self, players):
        nb_players = len(players)
        nb_starting_area_rooms = nb_players
        nb_other_rooms = self.rooms_per_player * nb_players - nb_players

        non_starting_area_rooms = self.create_non_starting_area_rooms(nb_other_rooms)
        starting_area_rooms = self.create_starting_area_rooms(nb_starting_area_rooms, non_starting_area_rooms, players)

        return non_starting_area_rooms + starting_area_rooms

    @staticmethod
    def create_starting_area_rooms(nb_rooms, non_starting_area_rooms, players):
        starting_area_rooms = []
        for i in range(nb_rooms):
            room_difficulty = 'starting_area'
            room = Room(room_difficulty)

            other_room = random.sample(non_starting_area_rooms, 1)[0]
            room.connect_with(other_room)

            players[i].enter_room(room)
            room._add_player(players[i])
            starting_area_rooms.append(room)
        return starting_area_rooms

    @staticmethod
    def create_non_starting_area_rooms(nb_rooms):
        non_starting_area_rooms = []
        for i in range(nb_rooms):
            room_difficulty = random.choice(['medium_area', 'hard_area'])
            room = Room(room_difficulty)

            # Make sure that it is reachable
            if i != 0:
                other_room = random.sample(non_starting_area_rooms, 1)[0]
                room.connect_with(other_room)
            non_starting_area_rooms.append(room)
        return non_starting_area_rooms

    def connect_rooms(self):
        other_rooms = list(filter(lambda room: room.room_difficulty != 'starting_area', self.rooms))
        for room in self.rooms:
            if room.room_difficulty == 'starting_area':
                connections = random.sample(other_rooms, self.nb_generate_room_connections)
                for other_room in connections:
                    room.connect_with(other_room)

            else:
                connections = random.sample(self.rooms, self.nb_generate_room_connections)
                for other_room in connections:
                    if other_room != room:
                        room.connect_with(other_room)

