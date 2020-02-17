import socket
import threading
import time


class Client:
    def __init__(self):
        self.game_state = {}
        self.game_state_port = 12000
        self.game_state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.action_port = 50000
        self.action_socket = socket.socket()
        self.action_host = socket.gethostname()

    def start(self):
        t1 = threading.Thread(target=self.start_game_updates_socket)
        t1.start()

        t2 = threading.Thread(target=self.start_actions_socket)
        t2.start()

    def start_game_updates_socket(self):
        self.game_state_socket.bind(("", self.game_state_port))
        while True:
            data, addr = self.game_state_socket.recvfrom(1024)
            self.game_state = self.decode_game_state(data)
            print(data)

    def start_actions_socket(self):
        self.action_socket.connect((self.action_host, self.action_port))
        while True:
            #msg = b"actions"
            #self.action_socket.send(msg)
            time.sleep(1)


    @staticmethod
    def decode_game_state(data):
        game_state = data
        return game_state

if __name__ == '__main__':
    client = Client()
    client.start()