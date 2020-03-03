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
            raise EmptyGameException("Not enough players in the lobby.")
        self.time = 0
        self.reset_players()
        self.ongoing = True

    def start_game(self):
        self._pregame_setup()

    def single_tick(self):
        self.time += 1
        self.income_tick()
        self.bleed_players()
        self.log()

        if self.is_over() and not self.players_alive():
            self.tied_game()
        elif self.is_over():
            self.game_won()

        return not self.is_over()

    def is_over(self):
        return len(self.players_alive()) <= 1

    def hit(self, from_user, to_user, action):
        self._players[to_user].get_hit(action['damage'])
        self._players[from_user].hits(action['damage'])
        self.action_log()

    def action_log(self):
        pass

    def players_alive(self):
        return list(filter(lambda player: player.is_alive(), self._players.values()))

    def log(self):
        print(f"{self.time}: {[(player.name, player.coins, player.get_income(), player.hp) for username, player in self._players.items()]}")

    def get_game_state(self):
        game_state = {
            'gameStatus': self.ongoing
        }
        return json.dumps(game_state)

    def bleed_players(self):
        for player in self.players_alive():
            player.bleed()

    def reset_players(self):
        for player in self._players.values():
            player.reset()

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
        for player in self.players_alive():
            player.income_tick()


class EmptyGameException(Exception):
    pass


class NonExistentUserException(Exception):
    pass


if __name__ == '__main__':
    pass
