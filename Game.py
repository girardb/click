import threading
import time

# TODO: I'll want game logs -> While it's ongoing and at the end
# TODO: SCORE SYSTEM FOR RANKINGS
# TODO: Fix: la clock pour gagner la game va à la même vitesse que la clock de l'income
# TODO: demande au user de starter la game
# TODO: fini la game doucement
# TODO: mini interface pour cliquer
# TODO: mini interface pour buy des trucs


class Game:
    def __init__(self, log_file_path):
        self._players = []
        self.time = 0
        self.ongoing = False
        self.logfile = log_file_path

        self.server = None

    def add_player(self, player):
        if player not in self._players:
            self._players.append(player)
            return True
        return False

    def add_server(self, server):
        self.server = server

    def start_game(self):
        self.time = 0
        self.ongoing = True
        self.reset_players()
        time.sleep(5)
        self._tick()

    def _tick(self):
        players_alive = self.players_alive()
        self.time += 1
        self.income_tick(players_alive)
        self.bleed_players(players_alive)
        self.log()
        if len(players_alive) >= 1: # Actual line -> len(players_alive > 1)
            tick = threading.Timer(1.0, self._tick)
            tick.start()
        elif not players_alive:
            self.tied_game()
        #else:
        #    self.game_won()

    def players_alive(self):
        return list(filter(lambda player: player.is_alive(), self._players))

    def log(self):
        print(f"{self.time}: {[(player.name, player.cookies, player.income, player.hp) for player in self._players]}")

    def get_game_state(self):
        # Temporary
        return str([(player.name, player.cookies, player.income, player.hp) for player in self._players])

    def bleed_players(self, players):
        for player in players:
            player.bleed()

    def reset_players(self):
        pass

    def game_won(self):
        pass

    def tied_game(self):
        print('everyone is a loser :(')
        self.ongoing = False

    def income_tick(self, players):
        for player in players:
            player.income_tick()


if __name__ == '__main__':
    pass
