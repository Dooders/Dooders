import time

import pygame
from pygame.locals import *

from dooders.game.blinky import Blinky
from dooders.game.constants import *
from dooders.game.fruit import Fruit
from dooders.game.maze import MazeData
from dooders.game.pacman import PacMan
from dooders.game.pauser import Pause
from dooders.game.pellets import PelletGroup
from dooders.game.sprites import LifeSprites, MazeSprites
from dooders.game.text import TextGroup
from dooders.sdk.base.coordinate import Coordinate
from dooders.sdk.surfaces.graph import Graph

map_legend = {
    "playable": [".", "-", "+", "p", "P", "n", "|"],
    "non-playable": [
        "X",
        "0",
        "1",
        "8",
        "7",
        "3",
        "2",
        "9",
        "6",
        "4",
        "5",
        "=",
    ],
}


class Game:
    """
    Main game controller class.  This class is responsible for
    initializing the game, loading the data, and updating the game
    state.  It also handles the main game loop and rendering.

    Attributes
    ----------
    screen : pygame.Surface
        The main game screen
    background : pygame.Surface
        The background image
    clock : pygame.time.Clock
        The game clock
    fruit : Fruit
        The fruit object
    pause : Pause
        The pause object
    level : int
        The current game level
    lives : int
        The number of lives remaining
    score : int
        The current score
    textgroup : TextGroup
        The text group object
    lifesprites : LifeSprites
        The life sprites object
    flashBG : bool
        Whether or not the background is flashing
    flashTime : float
        The time between background flashes
    flashTimer : float
        The current time since last background flash
    fruitCaptured : list
        A list of fruit images captured
    fruitNode : Node
        The node where the fruit is located
    mazedata : MazeData
        The maze data object

    Methods
    -------
    set_background()
        Sets the background image
    load_game()
        Starts the game
    update()
        Updates the game state
    check_events()
        Checks for user input
    check_pellet_events()
        Checks for pellet events
    check_ghost_events()
        Checks for ghost events
    check_fruit_events()
        Checks for fruit events
    show_entities()
        Shows the entities
    hide_entities()
        Hides the entities
    next_level()
        Starts the next level
    reload_game()
        Restarts the game
    reset_level()
        Resets the current level
    update_score()
        Updates the score
    render()
        Renders the game
    """

    def __init__(self, render_game: bool = True) -> None:
        self.render_game = render_game
        if render_game:
            pygame.init()
        self.screen = pygame.display.set_mode(Dimensions.SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()

    def set_background(self) -> None:
        """
        Sets up the game's background, including a normal background
        and a flashing one.
        """
        self.background_norm = pygame.surface.Surface(Dimensions.SCREENSIZE).convert()
        self.background_norm.fill(Colors.BLACK.value)
        self.background_flash = pygame.surface.Surface(Dimensions.SCREENSIZE).convert()
        self.background_flash.fill(Colors.BLACK.value)
        self.background_norm = self.mazesprites.construct_background(
            self.background_norm, self.level % 5
        )
        self.background_flash = self.mazesprites.construct_background(
            self.background_flash, 5
        )
        self.flashBG = False
        self.background = self.background_norm

    def load_game(self) -> None:
        """
        Loads the maze for the current level, sets up the maze sprites, nodes,
        Pacman, pellets, and ghosts. It also configures the starting positions
        and behaviors of the ghosts.

        Order of operations:
        1. Load the maze
        2. Set up the maze sprites
        3. Set up the nodes
        4. Set up Pacman
        5. Set up the pellets
        6. Set up the ghosts
        7. Set up the ghost starting positions
        8. Set up the ghost behaviors
        9. Set up the ghost home nodes
        10. Set up the ghost home access
        11. Set up the ghost access
        """
        self.mazedata.load_maze(self.level)
        self.mazesprites = MazeSprites()
        self.graph = self.setup_graph()
        self.set_background()
        self.pacman = PacMan()
        self.blinky = Blinky()
        self.graph.add(self.pacman, self.pacman.position)
        self.pellets = PelletGroup("dooders/game/assets/maze1.txt")

        for pellet in self.pellets.pellet_List:
            self.graph.add(pellet, pellet.position)

    def setup_graph(self):
        map_data = self.mazesprites.data
        grid_height = len(map_data)
        grid_width = len(map_data[0])
        graph = Graph({"height": grid_height, "width": grid_width, "map": map_data})

        nodes_to_remove = []

        for space in graph.spaces():
            if space.tile_type in map_legend["playable"]:
                space.playable = True
            else:
                nodes_to_remove.append(space.coordinates)

        # Removing the nodes that are not playable
        for node in nodes_to_remove:
            graph._graph.remove_node(node)

        return graph

    def update(self) -> None:
        """
        Updates the game state by updating all game entities
        (like Pacman, ghosts, pellets, etc.) and checking for various game
        events (like collisions).

        Also, handles the game's rendering.

        1. Game clock is updated.
        2. Update the text group, pellets, ghosts,and fruit. If the game is not
            paused, then the ghosts and fruit are updated.
        3. If Pacman is alive and the game is not paused, Pacman is updated.
            Otherwise, Pacman is updated regardless of whether the game is paused or not.
        4. If the background is flashing, the background is updated.
        5. Pause is updated.
        6. Game checks for events and renders the game.
        """
        dt = self.clock.tick(30) / 1000.0
        self.dt = dt
        self.textgroup.update(dt)
        self.pellets.update(dt)

        # Update ghosts, fruit, and check for pellet events
        if not self.pause.paused:
            self.blinky.update(self)
            self.check_pellet_events()
            self.check_ghost_events()

        # Play when pacman is alive and not paused
        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(self)
                self.check_ghost_events()
        else:
            self.pacman.update(self)

        # Flash background
        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        # Update pause
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()

        # Finish update and render
        self.check_events()
        if self.render_game:
            self.render()

        time.sleep(0.1)

    def path_finding(self, start: "Coordinate", end: "Coordinate") -> list:
        path = self.graph.path_finding(start, end)

        return path

    def check_events(self) -> None:
        """
        Checks for user input events, like quitting the game or pausing.

        If the user presses the space bar, the game is paused.
        If the user presses the escape key, the game is exited.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.textgroup.hide_text()
                        else:
                            self.textgroup.show_text(Texts.PAUSETXT)

    def check_pellet_events(self) -> None:
        """
        Checks if Pacman has eaten any pellets and handles the consequences.

        If Pacman eats a pellet, the pellet is removed from the pellet list, the
            score is updated, and the ghost freight state is started if Pacman
            eats a power pellet.
        If Pacman eats all the pellets, the background flashes and the game is
            paused for 3 seconds before starting the next level.
        """
        pellet = self.pacman.eat_pellets(self.pellets.pellet_List)
        if pellet:
            self.graph.remove(pellet)
            self.pellets.numEaten += 1
            self.update_score(pellet.points)
            # if self.pellets.numEaten == 30:
            #     self.ghosts.inky.startNode.allow_access(RIGHT, self.ghosts.inky)
            # if self.pellets.numEaten == 70:
            #     self.ghosts.clyde.startNode.allow_access(LEFT, self.ghosts.clyde)
            self.pellets.pellet_List.remove(pellet)
            if pellet.name == "PowerPellet":
                self.blinky.start_freight()
            if self.pellets.is_empty():
                self.flashBG = True
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    def check_ghost_events(self) -> None:
        """
        Checks for collisions between Pacman and the ghosts and handles the outcomes.

        If Pacman collides with a ghost in freight state, the ghost and Pacman
            are hidden, the score is updated, and the ghost is sent back to its
            spawn node.
        If Pacman collides with a ghost in any other state, Pacman dies and the
            game is paused for 3 seconds before restarting the level.
        """

        if self.pacman.collide_check(self.blinky):
            if self.blinky.state.current is GhostStates.FREIGHT:
                self.update_score(self.blinky.points)
                self.textgroup.add_text(
                    str(self.blinky.points),
                    Colors.WHITE,
                    self.blinky.position.x,
                    self.blinky.position.y,
                    8,
                    time=1,
                )
                self.blinky.start_spawn()
                # self.ghosts.update_points()
                # self.pause.set_pause(pause_time=1, func=self.show_entities)
                # self.nodes.allow_home_access(self.ghosts)

            elif self.blinky.state.current is not GhostStates.SPAWN:
                if self.pacman.alive:
                    self.lives -= 1
                    self.lifesprites.remove_image()
                    self.pacman.die()
                    self.blinky.visible = False

                    if self.lives <= 0:
                        self.textgroup.show_text(Texts.GAMEOVERTXT)
                        self.pause.set_pause(pause_time=3, func=self.reload_game)
                    else:
                        self.pause.set_pause(pause_time=3, func=self.reset_level)

    def check_fruit_events(self) -> None:
        """
        Checks for events related to the fruit, like if Pacman has eaten it.

        If Pacman eats the fruit, the score is updated and the fruit is removed.
        If the fruit is destroyed, the fruit is removed.
        """
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20), self.level)
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.update_score(self.fruit.points)
                self.textgroup.add_text(
                    str(self.fruit.points),
                    Colors.WHITE,
                    self.fruit.position.x,
                    self.fruit.position.y,
                    8,
                    time=1,
                )
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def search_pellet(self, start: "Coordinate") -> "Coordinate":
        #! Get rid of this method
        # Use BFS to find the closest pellet
        visited = set()
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)

                # Check if the node has a pellet
                space = self.graph._graph.nodes[node].get("space")
                if space and space.has("Pellet"):
                    return space

                # Add neighbors to the queue
                for neighbor in self.graph._graph.neighbors(node):
                    if neighbor not in visited:
                        queue.append(neighbor)

        return None  # Return None if no pellet is found

    def show_entities(self) -> None:
        """
        Shows the entities, like Pacman and the ghosts.
        """
        self.pacman.visible = True
        self.blinky.visible = True

    def hide_entities(self) -> None:
        """
        Hides the entities, like Pacman and the ghosts.
        """
        self.pacman.visible = False
        self.blinky.visible = False

    def next_level(self) -> None:
        """
        Progresses the game to the next level.
        """
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.load_game()
        self.textgroup.update_level(self.level)

    def reload_game(self) -> None:
        """
        Restarts the game from the beginning.
        """
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.load_game()
        self.score = 0
        self.textgroup.update_score(self.score)
        self.textgroup.update_level(self.level)
        self.textgroup.show_text(Texts.READYTXT)
        self.lifesprites.reset_lives(self.lives)
        self.fruitCaptured = []

    def reset_level(self) -> None:
        """
        Resets the current level.
        """
        self.pause.paused = True
        self.pacman.reset()
        self.blinky.reset()
        self.fruit = None
        self.textgroup.show_text(Texts.READYTXT)

    def update_score(self, points: int) -> None:
        """
        Updates the player's score.

        Parameters
        ----------
        points : int
            The amount of points to add to the score
        """
        self.score += points
        self.textgroup.update_score(self.score)

    def render(self) -> None:
        """
        Renders all game entities and UI elements onto the screen.

        1. The background is rendered.
        2. The nodes are rendered.
        3. The pellets are rendered.
        4. The fruit is rendered.
        5. Pacman is rendered.
        6. The ghosts are rendered.
        7. The text group is rendered.
        8. The lives sprites are rendered.
        9. The fruit captured sprites are rendered.
        """
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        # if self.fruit is not None:
        #     self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.blinky.render(self.screen)
        # self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        # # Lifesprites
        # for i in range(len(self.lifesprites.images)):
        #     x = self.lifesprites.images[i].get_width() * i
        #     y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
        #     self.screen.blit(self.lifesprites.images[i], (x, y))

        # # Fruit captured
        # for i in range(len(self.fruitCaptured)):
        #     x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i + 1)
        #     y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
        #     self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()
