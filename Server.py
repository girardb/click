from collections import deque
import socket
import _thread
import time


class Server:
    def __init__(self, Game):
        self.Game = Game

        self.action_port = 5000
        self.action_socket = socket.socket()
        self.action_host = socket.gethostname()

        self.game_state_port = 12000
        self.game_state_host = "<broadcast>"
        self.game_state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.game_state_socket.settimeout(0.2)

        self.queue = deque()
        self.server_on = True

    @staticmethod
    def on_new_client(client_socket, addr):
        #TODO: break out de ça
        while True:
            msg = client_socket.recv(1024)

            msg = ""
            client_socket.send(msg)
        clientsocket.close()

    def start(self):
        pass

    def __start(self):
        while self.server_on:
            if self.queue:
                action = self.queue.pop()
                action.execute()

    def add_action(self, action):
        self.queue.appendleft(action)

    def serve_actions(self):
        self.action_socket.bind((self.host, self.port))
        self.action_socket.listen(5)

        #TODO: break out de ça
        while True:
            c, addr = self.action_socket.accept()
            _thread.start_new_thread(self.on_new_client, (c, addr))
        self.action_socket.close()

    def serve_game_state_updates(self):
        while True:
            message = b"hello\n"
            self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))
            time.sleep(0.5)


if __name__ == '__main__':
    server = Server('')
    server.serve_game_state_updates()
