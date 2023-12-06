from dooders.game.main import GameController

game = GameController()
game.load_game()
while True:
    game.update()
