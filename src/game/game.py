import threading
import time
import json

from src.game.player import Player

# TODO: I'll want game logs -> While it's ongoing and at the end
# TODO: SCORE SYSTEM FOR RANKINGS


class Game:
    def __init__(self, log_file_path='log.txt'):
        self._players = {}
        self.time = 0
        self.ongoing = False
        self.log_file_path = log_file_path

        self.server = None

    @staticmethod
    def create_player(username):
        return Player(username)

    def add_player(self, player):
        if player.name not in self._players:
            self._players[player.name] = player
            return True
        return False

    def add_server(self, server):
        self.server = server

    def _pregame_setup(self):
        if len(self._players) < 2:
            raise EmptyGameException("The game lobby is too empty.")
        self.time = 0
        self.ongoing = True
        self.reset_players()

    def start_game(self):
        self._pregame_setup()

    def single_tick(self):
        self.time += 1
        self.income_tick()
        self.bleed_players()
        self.log()

    def is_over(self):
        return len(self.players_alive()) <= 1 and self.ongoing

    def hit(self, from_user, to_user, action):
        self._players[to_user].get_hit(action['damage'])
        self._players[from_user].hits(action['damage'])
        self.action_log()

    def action_log(self):
        pass

    def players_alive(self):
        return list(filter(lambda username: self._players[username].is_alive(), self._players))

    def log(self):
        print(f"{self.time}: {[(player.name, player.cookies, player.income, player.hp) for username, player in self._players.items()]}")

    def get_game_state(self):
        game_state = {
            'gameStatus': self.ongoing
        }
        return json.dumps(game_state)

    def bleed_players(self):
        for player in self._players.values():
            player.bleed()

    def reset_players(self):
        pass

    def game_won(self):
        print(f'{self.players_alive()[0]} won! :O')
        self.ongoing = False

    def click(self, username):
        if username not in self._players:
            raise NonExistentUserException("This user is not in the current game.")
        self._players[username].click()

    def tied_game(self):
        print('everyone is a loser :(')
        self.ongoing = False

    def income_tick(self):
        for player in self._players.values():
            player.income_tick()


class EmptyGameException(Exception):
    pass


class NonExistentUserException(Exception):
    pass


if __name__ == '__main__':
    pass
