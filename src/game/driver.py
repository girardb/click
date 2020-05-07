import time


class Driver:
    def __init__(self, game):
        self.game = game
        self.ticks_per_second = 1

    def start_game(self):
        self.game.start_game()
        self._play_game()

    def _play_game(self):
        raise NotImplementedError()


class ProdDriver(Driver):
    """
    Runs 'real' games
    """
    def _play_game(self):
        next_tick = self.ticks_per_second
        while True:
            time_before_tick = time.time()
            ongoing_game = self.game.custom_tick(next_tick)
            if not ongoing_game:
                break
            next_tick = (time.time() - time_before_tick) * self.ticks_per_second


class PlaybackDriver:
    """
    Runs game from logs
    """
    pass
