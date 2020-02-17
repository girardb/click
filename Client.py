import socket


class Client:
    def __init__(self):
        self.game_state = {}
        self.game_state_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.game_state_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.game_state_socket.bind(("", 12000))
        while True:
            data, addr = self.game_state_socket.recvfrom(1024)
            self.game_state = self.decode_game_state(data)
            print(data)

    @staticmethod
    def decode_game_state(data):
        game_state = data
        return game_state


if __name__ == '__main__':
    client = Client()
    client.start()
