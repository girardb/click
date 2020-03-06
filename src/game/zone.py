class Zone:
    class Node:
        def __init__(self, room, distance):
            self.room = room
            self.distance = distance

    def __init__(self, final_room, distance_to_be_affected=10, cycle_time=60, damage=10):
        self.final_room = final_room
        self.distance_to_be_affected = distance_to_be_affected
        self.cycle_time = cycle_time  # ##
        self.damage = damage

    def get_affected_rooms(self):
        queue = [self.Node(self.final_room, 0)]
        visited_rooms = set()
        visited_rooms.add(self.final_room)
        affected_rooms = []

        while queue:
            node = queue.pop()
            for neighbor in node.room.neighboring_rooms:
                if neighbor not in visited_rooms:
                    queue.append(self.Node(neighbor, node.distance+1))
                    visited_rooms.add(neighbor)
            if node.distance >= self.distance_to_be_affected:
                affected_rooms.append(node.room)

        return affected_rooms

    def affect_rooms(self):
        for room in self.get_affected_rooms():
            room.damage = self.damage

    def update_zone(self, time):
        if time % 60 == 0 and self.distance_to_be_affected > 0:
            self.distance_to_be_affected -= 1
        self.affect_rooms()

# Add driver test to check if the zone shrinks over time
# Every time the zone shrinks I could pick a new final_room from the unaffected rooms
# Need to be able to show the current affected rooms
# Need to be able to show the rooms that are going to be affected in the next cycle so the players can react.

