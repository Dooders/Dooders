import random


class Target:
    def __init__(self):
        self.current = None

    def update(self, game, agent):
        """
        Update the target state.

        Parameters
        ----------
        game : Game
            Game object
        agent : Agent
            Agent object
        """
        self.current = self.search(game, agent)

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
        neighbor_spaces = game.graph.nearby_spaces(agent.position)
        pellets = [
            space for space in neighbor_spaces if space.has(["Pellet", "PowerPellet"])
        ]

        if len(pellets) >= 1:
            target = random.choice(pellets).coordinates

        else:
            target = game.search_pellet(agent.position).coordinates

        return target
