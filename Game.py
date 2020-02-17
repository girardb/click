import threading

# TODO: I'll want game logs -> While it's ongoing and at the end
# TODO: SCORE SYSTEM FOR RANKINGS


class Game:
    def __init__(self, logfile):
        self._players = []
        self.timer = 0
        self.logfile = logfile

    def join_game(self, player):
        if player not in self._players:
            self._players.append(player)
            return True
        return False

    def start_game(self):
        self.timer = 0
        self.reset_players()
        self._tick()

    def _tick(self):
        players_alive = self.players_alive()
        if len(players_alive) > 1:
            self.timer += 1
            self.income_tick()
            tick = threading.Timer(1.0, self._tick)
            tick.start()
        elif not players_alive:
            self.tied_game()
        else:
            self.game_won()

    def players_alive(self):
        return list(filter(lambda player: player.is_alive(), self._players))

    def reset_players(self):
        pass

    def game_won(self):
        pass

    def tied_game(self):
        pass

    def income_tick(self):
        for player in filter(lambda _player: _player.is_alive(), self._players):
            player.income_tick()


if __name__ == '__main__':
    pass
