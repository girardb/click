from collections import deque


class ActionServer:
    def __init__(self):
        self.queue = deque()
        self.server_on = True

    def start(self):
        while self.server_on:
            if self.queue:
                action = self.queue.pop()
                action.execute()

    def add_action(self, action):
        self.queue.appendleft(action)

