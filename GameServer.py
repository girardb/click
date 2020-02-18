from collections import deque
from Game import Game
from Player import Player

import socket
import _thread
import time
import threading

# TODO: Use json to communicate


class GameServer:
    def __init__(self, log_path):
        self.action_port = 50000
        self.action_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.action_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.action_host = socket.gethostname()
        self.action_socket.bind((self.action_host, self.action_port))

        self.game_state_port = 12000
        self.game_state_host = "<broadcast>"
        self.game_state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.game_state_socket.settimeout(0.2)

        self.game = None

    def create_game(self, log_path):
        self.game = Game(log_path)

    def listen_before_game_actions(self, client_socket):
        while not self.game.ongoing:
            data = client_socket.recv(1024)
            if data == b"login":
                # hardcoded for now
                player = Player(f"player{len(self.game._players)}")
                self.game.add_player(player)
                print('new played logging in')
            elif data == b"start":
                print('starting game')
                self.game.start_game()

    def listen_for_actions(self, client_socket):
        while self.game.ongoing:
            data = client_socket.recv(1024)  # might get stuck here and will never close its socket
            actions = GameServer.decode_actions(data)
            print(actions)

            # TODO: do something with actions
            # self.execute_actions(actions)

    def serve_actions(self, client_socket, addr):
        # TODO: connection ends right as the game ends
        self.listen_before_game_actions(client_socket)
        self.listen_for_actions(client_socket)
        client_socket.close()

    @staticmethod
    def decode_actions(data):
        actions = data
        return actions

    def start(self):
        t1 = threading.Thread(target=self.serve_game_state_updates)
        t1.start()

        t2 = threading.Thread(target=self.serve_actions)
        t2.start()

    def create_action_socket_threads(self):
        self.action_socket.listen(5)

        while not self.game.ongoing:
            c, addr = self.action_socket.accept()
            _thread.start_new_thread(self.serve_actions, (c, addr))
        self.action_socket.close()

    def wait_for_game_start(self):
        while not self.game.ongoing:
            pass

    def send_game_state(self):
        message = self.game.get_game_state().encode()
        self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))
        time.sleep(0.5)

    def send_game_over(self):
        message = b"gameover"
        self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))

    def serve_game_state_updates(self):
        self.wait_for_game_start()

        while self.game.ongoing:
            self.send_game_state()

        self.send_game_over()
        self.game_state_socket.close()


if __name__ == '__main__':
    server = GameServer('log.txt')
    server.start()

