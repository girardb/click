from Server import Server
from Game import Game
from Player import Player

if __name__ == '__main__':
    game = Game('log.txt')
    server = Server(game)
    player = Player('player1')
    game.join_game(player) # devrait être l'inverse lol
    server.start()
    game.start_game()

