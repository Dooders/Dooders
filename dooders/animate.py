""" 
Class to create and return a default pygame rendered grid of LxW dimensions

#! Is this class still needed?
"""

import math
import sys

import imageio
import pygame
from pydantic import BaseModel


class DefaultSettings(BaseModel):
    Length: int = 10
    Width: int = 10
    CellSize: int = 50
    CellPadding: int = 5
    Padding: int = 20
    CounterPadding: int = 30
    FontColor: tuple = (255, 255, 255)
    BackgroundColor: tuple = (211, 211, 211)
    AgentColor: tuple = (29, 48, 36)
    EnergyColor: tuple = (0, 0, 139)
    TrailColor: tuple = (132, 150, 139)
    ChosenColor: tuple = (0, 255, 0)
    ChosenAlpha: int = 128


class Grid:
    """ 
    Class to create and return a default pygame rendered grid of LxW dimensions

    Parameters
    ----------
    L : int
        Length of the grid
    W : int
        Width of the grid
    caption : str
        Caption of the pygame window

    Attributes
    ----------
    L : int
        Length of the grid
    W : int
        Width of the grid
    grid_size : int
        Length of the grid
    cell_size : int
        Size of each cell in the grid
    cell_padding : int
        Padding between each cell in the grid
    padding : int
        Padding of the grid
    counter_padding : int
        Padding of the counter
    caption : str
        Caption of the pygame window
    screen_width : int
        Width of the pygame window
    screen_height : int
        Height of the pygame window
    screen : pygame.Surface
        Pygame surface of the pygame window
    clock : pygame.time.Clock
        Pygame clock
    clockfont : pygame.font.Font
        Pygame font
    font : pygame.font.Font
        Pygame font

    Methods
    -------
    draw_grid()
        Draws the grid
    draw_agent(pos, color, text_color=(255, 255, 255), text=None)
        Draws an agent in the grid
    draw_counter(counter)
        Draws the counter
    draw()
        Draws the grid and the counter
    save_image(filename)
        Saves the current state of the grid as an image
    save_gif(filename, fps=10)
        Saves the current state of the grid as a gif
    """

    def __init__(self, L: int, W: int, caption: str = "Grid Animation",
                 save: bool = False, trail: bool = False,
                 settings: DefaultSettings = None) -> None:
        self.settings = settings or DefaultSettings()
        self._initialize_default_settings()
        self.L = L
        self.W = W
        self.grid_size = L
        self.save = save
        self.trail = trail
        self.caption = caption
        self.screen_width = self.grid_size * self.cell_size + \
            self.cell_padding * (self.grid_size - 1) + 2 * self.padding
        self.screen_height = self.grid_size * self.cell_size + self.cell_padding * \
            (self.grid_size - 1) + 2 * self.padding + self.counter_padding

    def _initialize_default_settings(self):
        self.cell_size = self.settings.CellSize
        self.cell_padding = self.settings.CellPadding
        self.padding = self.settings.Padding
        self.counter_padding = self.settings.CounterPadding
        self.agent_color = self.settings.AgentColor
        self.energy_color = self.settings.EnergyColor
        self.trail_color = self.settings.TrailColor
        self.chosen_color = self.settings.ChosenColor
        self.chosen_alpha = self.settings.ChosenAlpha

    def setup(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption(self.caption)

        self.clock = pygame.time.Clock()
        self.clockfont = pygame.font.Font(None, 24)

    def draw_border(self, color: tuple = (0, 0, 0), thickness: int = 2) -> None:
        """
        Draws a border around the grid

        Parameters
        ----------
        color : tuple
            Color of the border
        thickness : int
            Thickness of the border
        """
        border_rect = pygame.Rect(
            self.padding - thickness,
            self.padding + self.counter_padding - thickness,
            self.grid_size * self.cell_size + self.cell_padding *
            (self.grid_size - 1) + 2 * thickness,
            self.grid_size * self.cell_size + self.cell_padding *
            (self.grid_size - 1) + 2 * thickness,
        )
        pygame.draw.rect(self.screen, color, border_rect, thickness)

    def draw_grid(self) -> None:
        """ 
        Draws the grid
        """
        font = pygame.font.Font(None, 16)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                cell_number = y * self.grid_size + x
                cell_number_text = font.render(
                    str(cell_number + 1), True, self.settings.FontColor)

                rect = pygame.Rect(
                    self.padding + x * (self.cell_size + self.cell_padding),
                    self.padding + self.counter_padding + y *
                    (self.cell_size + self.cell_padding),
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, self.settings.BackgroundColor,
                                 rect, border_radius=5)

                # Add cell number to the top left of the cell
                cell_number_position = (
                    self.padding + x * (self.cell_size +
                                        self.cell_padding) + 5,
                    self.padding + self.counter_padding + y *
                    (self.cell_size + self.cell_padding) + 5
                )
                self.screen.blit(cell_number_text, cell_number_position)

                # self.draw_border()

    def draw_agent(self,
                   pos: tuple,
                   color: tuple = None,
                   text_color: tuple = None,
                   text: str = None
                   ) -> None:
        """ 
        Draws an agent in the grid

        Parameters
        ----------
        pos : tuple
            Position of the agent
        color : tuple
            Color of the agent
        text_color : tuple
            Color of the text
        text : str
            Text to be displayed
        """
        color = color or self.agent_color
        text_color = text_color or self.settings.FontColor
        x, y = pos
        rect = pygame.Rect(
            self.padding + x * (self.cell_size +
                                self.cell_padding) + self.cell_padding // 2,
            self.padding + self.counter_padding + y *
            (self.cell_size + self.cell_padding) + self.cell_padding // 2,
            self.cell_size - self.cell_padding,
            self.cell_size - self.cell_padding,
        )
        pygame.draw.rect(self.screen, color, rect, border_radius=5)

        if text is not None:
            self.font = pygame.font.Font("Roboto-Bold.ttf", 24)
            self.letter = self.font.render(text, True, text_color)
            self.letter_rect = self.letter.get_rect(center=rect.center)
            self.screen.blit(self.letter, self.letter_rect)

    def draw_cycle_counter(self, cycles: int) -> None:
        """ 
        Draws the counter

        Parameters
        ----------
        counter : int
            Counter to be displayed
        """
        text = self.font.render(f"Step: {cycles}", True, (51, 51, 51))
        self.screen.blit(text, (self.padding, self.padding))

    def draw_trail(self, visited_positions: list) -> None:
        """ 
        Draws the trail of visited cells in green

        Parameters
        ----------
        visited_positions : list
            List of visited positions
        """
        for pos in visited_positions:
            self.draw_agent(pos, (132, 150, 139))

    def draw_energy(self, pos: tuple, color: tuple = None) -> None:
        """ 
        Draws energy as a dark blue circle within the cell

        Parameters
        ----------
        pos : tuple
            Position on the grid
        energy : int
            Energy value
        color : tuple
            Color of the energy circle
        """
        color = color or self.energy_color
        x, y = pos
        circle_center = (
            self.padding + x * (self.cell_size +
                                self.cell_padding) + self.cell_size // 2,
            self.padding + self.counter_padding + y *
            (self.cell_size + self.cell_padding) + self.cell_size // 2,
        )
        radius = self.cell_size // 5
        pygame.draw.circle(self.screen, color, circle_center, radius)

    def draw_chosen_space(self, pos: tuple, color: tuple = None,
                          alpha: int = None) -> None:
        """ 
        Makes the chosen cell semi-transparent green

        Parameters
        ----------
        pos : tuple
            Position on the grid
        color : tuple
            Color of the semi-transparent cell
        alpha : int
            Transparency value (0 to 255)
        """
        color = color or self.chosen_color
        alpha = alpha or self.chosen_alpha
        x, y = pos
        rect = pygame.Rect(
            self.padding + x * (self.cell_size + self.cell_padding),
            self.padding + self.counter_padding + y *
            (self.cell_size + self.cell_padding),
            self.cell_size,
            self.cell_size,
        )
        green_surface = pygame.Surface(
            (self.cell_size, self.cell_size), pygame.SRCALPHA)
        green_surface.fill((*color, alpha))
        self.screen.blit(green_surface, rect.topleft)

    def animate(self, player_positions: list, energy_data: list,
            chosen_positions: list) -> None:
        """ 
        Animates the agent moving through the grid, displays energy information, and indicates the chosen space

        Parameters
        ----------
        player_positions : list
            List of positions of the agent
        energy_data : list
            List of dictionaries containing energy information for each turn
        chosen_positions : list
            List of tuples containing the chosen positions for each turn
        """

        self.setup()

        current_position = 0
        num_scenes = len(player_positions)

        frames = []

        for scene_idx in range(num_scenes):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))
            self.draw_grid()

            if self.trail:
                # Draw the trail of visited cells in green
                visited_positions = player_positions[:current_position]
                self.draw_trail(visited_positions)

            # Draw energy circles
            energy_positions = energy_data[scene_idx]
            for energy_pos in energy_positions:
                self.draw_energy(energy_pos, (0, 0, 139))

            chosen_color = self.chosen_color

            if energy_positions:  # If there are energy objects on the grid
                if chosen_positions[current_position] in energy_positions:
                    chosen_color = self.chosen_color  # Green for energy object
                else:
                    chosen_color = (255, 0, 0)  # Red for no energy object

            self.draw_chosen_space(chosen_positions[current_position], color=chosen_color)

            self.draw_agent(
                player_positions[current_position], (29, 48, 36), text="D")
            current_position += 1

            self.draw_cycle_counter(current_position)

            if self.save:
                # Capture the current frame and add it to the list of frames
                frame = pygame.surfarray.array3d(self.screen)
                frames.append(frame.swapaxes(0, 1))

            pygame.display.flip()
            self.clock.tick(3)

        # Save the frames as an animated GIF
        if self.save:
            imageio.mimsave(f"{self.caption}.gif", frames, fps=3)

        pygame.quit()

    def collage(self, player_positions: list, energy_data: list,
            chosen_positions: list, filename: str = "collage.png") -> None:
        """ 
        Creates a collage of scenes

        Parameters
        ----------
        player_positions : list
            List of positions of the agent
        energy_data : list
            List of lists containing tuples of energy positions for each turn
        chosen_positions : list
            List of tuples containing the chosen positions for each turn
        filename : str
            Output filename for the collage
        """
        self.setup()

        num_scenes = len(player_positions)
        collage_side = math.ceil(math.sqrt(num_scenes))

        actual_rows = math.ceil(num_scenes / collage_side)

        collage_width = collage_side * self.screen_width
        collage_height = actual_rows * self.screen_height

        collage_surface = pygame.Surface((collage_width, collage_height))
        collage_surface.fill((255, 255, 255))

        for scene_idx in range(num_scenes):
            self.screen.fill((255, 255, 255))
            self.draw_grid()

            # Check if the grid has any energy objects
            has_energy_objects = any(energy_data[scene_idx])

            # Draw chosen_positions
            if not has_energy_objects or chosen_positions[scene_idx] in energy_data[scene_idx]:
                self.draw_chosen_space(chosen_positions[scene_idx], color=(0, 255, 0), alpha=self.chosen_alpha)
            else:
                self.draw_chosen_space(chosen_positions[scene_idx], color=(255, 0, 0), alpha=self.chosen_alpha)

            # Draw energy circles
            energy_positions_real = energy_data[scene_idx]
            for energy_pos in energy_positions_real:
                self.draw_energy(energy_pos, (0, 0, 139))

            if self.trail:
                # Draw the trail of visited cells in green
                visited_positions = player_positions[:scene_idx]
                self.draw_trail(visited_positions)

            self.draw_agent(
                player_positions[scene_idx], (29, 48, 36), text="D")

            self.draw_cycle_counter(scene_idx + 1)

            row = scene_idx // collage_side
            col = scene_idx % collage_side
            collage_surface.blit(
                self.screen, (col * self.screen_width, row * self.screen_height))

        pygame.image.save(collage_surface, filename)
        pygame.quit()

    def render_map(self, filename: str = "map.png") -> None:
        """ 
        Renders the map

        Parameters
        ----------
        filename : str
            Output filename for the map
        """
        self.setup()

        self.screen.fill((255, 255, 255))
        self.draw_grid()

        pygame.image.save(self.screen, filename)
        pygame.quit()
        