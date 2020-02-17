from collections import deque
import socket
import _thread
import time
import threading


class Server:
    def __init__(self, game):
        self.action_port = 50000
        self.action_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.action_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.action_host = socket.gethostname()

        self.game_state_port = 12000
        self.game_state_host = "<broadcast>"
        self.game_state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.game_state_socket.settimeout(0.2)

        self.queue = deque()
        self.server_on = True

        self.game = game

    @staticmethod
    def on_new_client(client_socket, addr):
        #TODO: break out de ça
        while True:
            data = client_socket.recv(1024)
            actions = Server.decode_actions(data)
            print(actions)
            # TODO: do something with actions

        clientsocket.close()

    @staticmethod
    def decode_actions(data):
        actions = data
        return actions

    def start(self):
        t1 = threading.Thread(target=self.serve_game_state_updates)
        t1.start()

        t2 = threading.Thread(target=self.serve_actions)
        t2.start()

    def __start(self):
        while self.server_on:
            if self.queue:
                action = self.queue.pop()
                action.execute()

    def add_action(self, action):
        self.queue.appendleft(action)

    def serve_actions(self):
        self.action_socket.bind((self.action_host, self.action_port))
        self.action_socket.listen(5)

        #TODO: break out de ça
        while True:
            c, addr = self.action_socket.accept()
            _thread.start_new_thread(self.on_new_client, (c, addr))
        self.action_socket.close()

    def serve_game_state_updates(self):
        while True:
            #message = bytes(self.game.get_game_state())
            message = self.game.get_game_state().encode()
            self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))
            time.sleep(0.5)

