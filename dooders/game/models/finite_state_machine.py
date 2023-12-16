import random


class FiniteStateMachine:
    def __init__(self):
        self.state = "Search"
        self.environment = None

    def update(self, game, agent):
        """
        While in the seek pellets state, Ms Pac-Man moves randomly up until it
        detects a pellet and then follows a pathfinding algorithm to eat as many
        pellets as possible and as soon as possible.

        If a power pill is eaten, then Ms PacMan moves to the chase ghosts state
        in which it can use any tree-search algorithm to chase the blue ghosts.

        When the ghosts start flashing, Ms Pac-Man moves to the evade ghosts
        state in which it uses tree search to evade ghosts so that none is
        visible within a distance; when that happens Ms Pac-Man moves back to
        the seek pellets state.

        States
        -------
        """
        # self.update_state(game, agent)
        next_position = self.update_direction(game, agent)

        return next_position

    def update_state(self, game, agent) -> None:
        """
        Update the PacMan's state based on the current game environment.

        The PacMan's state is updated based on the following rules:
        1. If the PacMan is in the search state and a power pellet is nearby,
            then the PacMan moves to the chase state.
        2. If the PacMan is in the search state and a non-vulnerable ghost is
            nearby, then the PacMan moves to the evade state.
        3. If the PacMan is in the chase state and a power pellet is eaten and
            a vulnerable ghost is nearby, then the PacMan moves to the attack
            state.
        4. If the PacMan is in the chase state and a non-vulnerable ghost is
            nearby, then the PacMan moves to the evade state.
        5. If the PacMan is in the attack state and no vulnerable ghosts are
            nearby or a vulnerable ghost is eaten, then the PacMan moves to
            the search state.
        6. If the PacMan is in the evade state and no non-vulnerable ghosts are
            nearby, then the PacMan moves to the search state.
        7. If the PacMan is in the evade state and a power pellet is nearby, then
            the PacMan moves to the chase state.
        """

        if self.state == "Search":
            if self.power_pellet_nearby(game, agent):
                self.state = "Chase"
            elif self.non_vulnerable_ghost_nearby(game, agent):
                self.state = "Evade"

        elif self.state == "Chase":
            if self.ate_power_pellet(game, agent) and self.vulnerable_ghost_nearby(
                game, agent
            ):
                self.state = "Attack"
            elif self.non_vulnerable_ghost_nearby(game, agent):
                self.state = "Evade"

        elif self.state == "Attack":
            if not self.vulnerable_ghost_nearby(
                game, agent
            ) or self.ate_vulnerable_ghost(game, agent):
                self.state = "Search"

        elif self.state == "Evade":
            if not self.non_vulnerable_ghost_nearby(game, agent):
                self.state = "Search"
            elif self.power_pellet_nearby(game, agent):
                self.state = "Chase"

    def update_direction(self, game, agent):
        if self.state == "Search":
            next_position = self.search(game, agent)
        elif self.state == "Chase":
            pass
        elif self.state == "Attack":
            pass
        elif self.state == "Evade":
            pass

        return next_position

    def search(self, game, agent):
        """
        Get the next direction to move in the search state.

        If no pellets are nearby, then move randomly.
        If a pellet is nearby, then move towards it.
        """
        #! remove Pellet from space after eaten (or set as eaten)
        neighbor_spaces = game.graph.get_neighbor_spaces(
            agent.position
        )  #! remove get from method name
        pellets = [
            space
            for space in neighbor_spaces
            if space.has("Pellet")
            or space.has("PowerPellet")  #! allow to take list of objects
        ]

        # eligible_neighbors = [
        #     space
        #     for space in neighbor_spaces
        #     if space.playable and space not in pellets
        # ]

        if len(pellets) >= 1:
            target = random.choice(pellets).coordinates

        else:
            target = game.search_pellet(agent.position).coordinates

        return target

    def pellet_nearby(self):
        """
        Checks the direct up, down, left, and right cells for power pellets.

        Parameters
        ----------
        environment : dict
            The game environment

        Returns
        -------
        bool
            True if a power pellet is found, False otherwise
        """
        pacman_x, pacman_y = self.position

    def power_pellet_nearby(self, pacman_position, game_board, threshold_distance=3):
        """
        Check if a power pellet is nearby Pac-Man.

        It is considered nearby if it is within a Manhattan distance of
        threshold_distance.

        Manhattan distance is the distance between two points measured along
        the path and not the straight line distance.

        Parameters
        ----------
        pacman_position : tuple

        """
        pacman_x, pacman_y = pacman_position

        # Iterate over the game board
        for y in range(len(game_board)):
            for x in range(len(game_board[y])):
                # Check if the current cell contains a power pellet
                if game_board[y][x] == "PowerPellet":
                    # Calculate the Manhattan distance between Pac-Man and the power pellet
                    distance = abs(pacman_x - x) + abs(pacman_y - y)
                    if distance <= threshold_distance:
                        return True

        return False

    def non_vulnerable_ghost_nearby(self, environment):
        return False

    def vulnerable_ghost_nearby(self, environment):
        return False

    def ate_power_pellet(self, environment):
        return False

    def ate_vulnerable_ghost(self, environment):
        return False

    def move_towards_nearest_pellet(self, environment):
        # Search algo for nearest pellet in 4 directions (up, down, left, right)
        # stops when it hits a wall or a pellet, returns distance, shortest distance is chosen
        # get the N spaces in a provided direction
        return None

    def move_towards_power_pellet(self):
        return None

    def move_towards_vulnerable_ghost(self):
        return None

    def move_away_from_ghost(self):
        return None
