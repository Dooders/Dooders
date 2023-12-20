from dooders.games.pacman.game import Game

game = Game()
game.load_game()
while True:
    game.update()
