import threading
import time


class Driver:
    def __init__(self, game):
        self.game = game

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
        while self.game.single_tick():
            time.sleep(1)


class PlaybackDriver:
    """
    Runs game from logs
    """
    pass
