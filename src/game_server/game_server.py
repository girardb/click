from src.game.game import Game
from src.game.driver import ProdDriver


import socket
import _thread
import time
import threading
import json
import collections

# TODO: refactor execute + actions decoding + management into its own class


class EndGameErrorException(Exception):
    pass


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
        self.game_state_socket.settimeout(0.1)

        self.driver = None
        self.log_path = log_path

        self.action_queue = collections.deque()

    def create_game(self, log_path):
        game = Game(log_path)
        self.driver = ProdDriver(game)

    def execute_actions(self):
        while self.driver.game.ongoing:
            if self.action_queue:
                action = self.action_queue.pop()
                self.execute(action)

    def listen_before_game_actions(self, client_socket):
        while not self.driver.game.ongoing:
            data = client_socket.recv(1024)
            data = self.decode_data(data)
            if data['type'] == "login":
                # hardcoded for now
                username = f"player{len(self.driver.game._players)}"
                player = self.driver.game.create_player(username)
                self.driver.game.add_player(player)
                print('new played logging in')

            elif data['type'] == "start":
                print('starting game')
                t = threading.Thread(target=self.driver.start_game)
                t.start()

                action_queue_thread = threading.Thread(target=self.execute_actions)
                action_queue_thread.start()


    @staticmethod
    def decode_data(data):
        if data == b'':
            raise EndGameErrorException()
        return json.loads(data.decode())

    # TODO: checker si architecturellement ca fait du sens de faire cette logique là ici
    # changer le nom de 'content' à de quoi de plus représentatif
    def execute(self, action):
        username = action['user']
        player = self.driver.game._players[username]

        if action['content'] == 'click':
            self.driver.game.click(username)

        elif action['content'] == 'hits':
            target_username = action['target']
            target = self.driver.game._players[target_username] ###
            player.hits(target)

        elif action['content'] == 'buy':
            item_type = action['item_type']
            item_effect = action['item_effect']
            item = player.consumables[item_type][item_effect]
            player.buy_item(item)

        elif action['content'] == 'upgrade':
            upgrade_type = action['upgrade_type']
            upgrade_level = action['upgrade_level']
            upgrade = player.upgrades[upgrade_type][upgrade_level]
            player.upgrade(upgrade)

        elif action['content'] == 'use_item':
            target_username = action['target']
            item_type = action['item_type']
            item_effect = action['item_effect']
            item = player.consumables[item_type][item_effect]
            player.use_item(item, target_username)

        elif action['content'] == 'enter_room':
            room_index = action['room_index'] # eventually change to room_name
            room = self.driver.game.map.rooms[room_index]
            player.enter_room(room)

    def listen_for_actions(self, client_socket):
        while self.driver.game.ongoing:
            try:
                data = client_socket.recv(1024)
                action = GameServer.decode_data(data)
                self.action_queue.appendleft(action)
            except EndGameErrorException: # TODO: FIX
                break

    def serve_actions(self, client_socket, addr):
        # TODO: connection ends right as the game ends
        self.listen_before_game_actions(client_socket)
        self.listen_for_actions(client_socket)
        client_socket.close()

    def start(self):
        if self.driver is None:
            self.create_game(self.log_path)

        t1 = threading.Thread(target=self.serve_game_state_updates)
        t1.start()

        t2 = threading.Thread(target=self.create_action_socket_threads)
        t2.start()

    def create_action_socket_threads(self):
        self.action_socket.listen(5)

        while not self.driver.game.ongoing:
            c, addr = self.action_socket.accept()
            _thread.start_new_thread(self.serve_actions, (c, addr))
        self.action_socket.close()

    def wait_for_game_start(self):
        while not self.driver.game.ongoing:
            pass

    def send_game_state(self):
        message = self.driver.game.get_game_state().encode()
        self.game_state_socket.sendto(message, (self.game_state_host, self.game_state_port))
        time.sleep(0.5)

    def send_game_over(self):
        message = {
            'gameStatus': False
        }
        self.game_state_socket.sendto(json.dumps(message).encode(), (self.game_state_host, self.game_state_port))

    def serve_game_state_updates(self):
        self.wait_for_game_start()

        while self.driver.game.ongoing:
            self.send_game_state()

        self.send_game_over()
        self.game_state_socket.close()


if __name__ == '__main__':
    server = GameServer('log.txt')
    server.start()

