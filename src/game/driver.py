import threading


class Driver:
    def __init__(self, game):
        self.game = game

    def start_game(self):
        self.game.start_game()
        self._tick()

    def re_tick(self):
        raise NotImplementedError()

    def _tick(self):
        if not self.game.is_over():
            self.game.single_tick()
            self.re_tick()
        elif self.game.is_over() and not self.game.players_alive():
            self.game.tied_game()
        else:
            self.game.game_won()


class ProdDriver(Driver):
    """
    Runs 'real' games
    """
    def re_tick(self):
        tick = threading.Timer(1.0, self._tick)
        tick.start()


class TestDriver(Driver):
    """
    Runs game for tests
    """
    def re_tick(self):
        self._tick()


class PlaybackDriver:
    """
    Runs game from logs
    """
    pass
