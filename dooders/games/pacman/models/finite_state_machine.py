from dooders.games.pacman.settings import GhostStates
from dooders.games.pacman.targets import Target
import random


class PacManFSM:
    def __init__(self):
        self.current = None

    def run(self, game, agent):
        """
        Update the target state.

        Parameters
        ----------
        game : Game
            Game object
        agent : Agent
            Agent object
        """
        agent.target.current = self.search(game, agent)

    def search(self, game, agent):
        """
        Get the next direction to move in the search state.

        If no pellets are nearby, then move randomly.
        If a pellet is nearby, then move towards it.

        Parameters
        ----------
        game : Game
            Game object
        agent : Agent
            Agent object

        Returns
        -------
        tuple
            The coordinates of the target space
        """
        neighbor_spaces = game.map.graph.nearby_spaces(agent.position)
        pellets = [
            space for space in neighbor_spaces if space.has(["Pellet", "PowerPellet"])
        ]

        if len(pellets) >= 1:
            target = random.choice(pellets).coordinates

        else:
            target = game.search_pellet(agent.position).coordinates

        return target


class GhostFSM:
    def __init__(self):
        self.current = None

    def run(self, game, agent):
        """
        Update the target state.

        Parameters
        ----------
        game : Game
            Game object
        agent : Agent
            Agent object
        """
        agent.target.current = self.update(game, agent)

    def update(self, game, agent):
        """
        Updates the ghost's position and direction based on the current state.

        If the ghost is in the SPAWN state, then the target is the spawn point.

        If the ghost CHASE state, the target is PacMan's position.

        If the ghost is in the SCATTER state, then the target is the next waypoint.

        Parameters
        ----------
        game : GameController
            The game controller object that the ghost is in.
        """
        if agent.state.current == GhostStates.SPAWN:
            self.current = agent.spawn

        elif agent.state.current == GhostStates.CHASE:
            self.current = game.pacman.position

        elif agent.state.current == GhostStates.SCATTER:
            if agent.path == [] and agent.waypoints != []:
                self.current = agent.waypoints.pop(0)
