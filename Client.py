import socket
import threading
import time


class Client:
    def __init__(self):
        self.game_state = {}
        self.ongoing_game = False
        self.start = False

        self.game_state_port = 12000
        self.game_state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.game_state_socket.bind(("", self.game_state_port))

        self.action_port = 50000
        self.action_socket = socket.socket()
        self.action_host = socket.gethostname()
        self.action_socket.connect((self.action_host, self.action_port))

    def send_login(self):
        print('logging in')
        login_message = b"login"
        self.action_socket.send(login_message)
        time.sleep(2)

    def start_game(self):
        self.send_start_game()
        self.start = True
        self.ongoing_game = True

    def send_start_game(self):
        print('starting game')
        start_message = b"start"
        self.action_socket.send(start_message)
        time.sleep(2)

    def start_sockets(self):
        t1 = threading.Thread(target=self.start_game_updates_socket)
        t1.start()

        t2 = threading.Thread(target=self.start_actions_socket)
        t2.start()

    def wait_for_game_start(self):
        while not self.start:
            pass

    def start_game_updates_socket(self):
        self.wait_for_game_start()
        while self.ongoing_game:
            data, addr = self.game_state_socket.recvfrom(1024)
            game_state = self.decode_data(data)
            if game_state == b"gameover":
                self.ongoing_game = False
                print('game over')
            else:
                print(data)
                # update things
        self.game_state_socket.close()

    def start_actions_socket(self):
        self.wait_for_game_start()
        while self.ongoing_game:
            #msg = b"actions"
            #self.action_socket.send(msg)
            time.sleep(1)
        self.action_socket.close()


    @staticmethod
    def decode_data(data):
        game_state = data
        return game_state


if __name__ == '__main__':
    client = Client()
    client.start_sockets()
    client.send_login()
    client.start_game()

