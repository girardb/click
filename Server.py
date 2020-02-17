from collections import deque
from Game import Game
from Player import Player

import socket
import _thread
import time
import threading

# TODO: Use json to communicate
# TODO: refactor en général parce que jesus christ


class Server:
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

        self.queue = deque()
        self.server_on = True
        self.listening_to_client = True

        self.game = Game(log_path)

    def on_new_client(self, client_socket, addr):
        #TODO: fix/connection ends right as the game ends
        while self.listening_to_client:
            data = client_socket.recv(1024) # might get stuck here and will never close its socket
            actions = Server.decode_actions(data)
            print(actions)
            if not self.game.ongoing:
                if actions == b"login":
                    #hardcoded for now
                    player = Player(f"player{len(self.game._players)}")
                    self.game.add_player(player)
                    print('new played logging in')
                elif actions == b"start":
                    print('starting game')
                    self.game.start_game()

            else:
                print(actions)
                # TODO: do something with actions

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

    # TODO: trouver une manière de ender ça à la fin
    def serve_actions(self):
        self.action_socket.listen(5)

        while True:
            c, addr = self.action_socket.accept()
            _thread.start_new_thread(self.on_new_client, (c, addr))
        self.action_socket.close()

    def serve_game_state_updates(self):
        while not self.game.ongoing:
            pass

        while self.game.ongoing:
            message = self.game.get_game_state().encode()
            self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))
            time.sleep(0.5)
        message = b"gameover"
        self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))
        self.game_state_socket.close()
        self.listening_to_client = False


if __name__ == '__main__':
    server = Server('log.txt')
    server.start()

