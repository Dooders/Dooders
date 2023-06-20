from collections import Counter
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pygame

from dooders.charts.grid import GridViz


def perception_state_grid(cycle_count: int,
                          filename: str = 'perception_state_grid',
                          energy_positions: list = [],
                          decision: Union[str, None] = None
                          ) -> None:
    """ 
    Creates a grid visualization of the perception state of the agent.

    Parameters
    ----------
    cycle_count : int
        The current cycle count of the agent.
    filename : str, optional
        The filename of the image to be saved. The default is 'perception_state_grid'.
    energy_positions : list, optional
        A list of positions of energy in the grid. The default is [].
        For example, ['1', '3', '7'].
    decision : str, optional
        The decision made by the agent. The default is None. This will be
        highlighted red if the decision is to move to a position without energy,
        and green if the decision is to move to a position with energy.
    """

    mapping = {'0': (0, 0),
               '1': (1, 0),
               '2': (2, 0),
               '3': (0, 1),
               '4': (1, 1),
               '5': (2, 1),
               '6': (0, 2),
               '7': (1, 2),
               '8': (2, 2)}

    g = GridViz(3, 3)
    g.setup()
    g.screen.fill((255, 255, 255))
    g.draw_grid()

    if decision:
        if decision in energy_positions:
            space_color = (0, 255, 0)
        else:
            space_color = (255, 0, 0)

        pos = mapping.get(decision, (None, None))
        if None in pos:
            raise ValueError(
                f'Invalid decision value: {decision}. Must be between 0 and 8.')
        else:
            g.fill_space(pos, space_color)

    if energy_positions:
        for position in energy_positions:
            final_position = mapping.get(position)
            g.draw_energy(final_position)

    g.draw_agent((1, 1))

    g.draw_cycle_counter(int(cycle_count) + 1)
    pygame.display.flip()
    pygame.image.save(g.screen, f'{filename}.png')
    pygame.quit()


def make_decision_value_list(inference_record: dict):
    decision_list = []

    for data in inference_record.values():
        decision_list.append(data['decision'])

    return decision_list


def make_reality_value_list(inference_record: dict):
    reality_list = []

    for data in inference_record.values():
        reality_list.append(data['reality'])

    return [element for sublist in reality_list for element in sublist]


def make_counter(decision_value_list):
    decision_counts = Counter(decision_value_list)
    sorted_decision_counts = {
        str(i): decision_counts.get(str(i), 0) for i in range(9)}

    return sorted_decision_counts


def create_color_range(int_values):
    # normalize the values to range between 0 and 1
    normalized_values = (int_values - np.min(int_values)) / np.ptp(int_values)

    # get the colormap
    cmap = plt.get_cmap('viridis')

    # map normalized values to colors
    color_range = cmap(normalized_values)

    return [tuple(color[:3]) for color in color_range]


def decision_map(decision_value_list: list = [], filename: str = 'decision_map') -> None:
    """ 
    """

    mapping = {'0': (0, 0),
               '1': (1, 0),
               '2': (2, 0),
               '3': (0, 1),
               '4': (1, 1),
               '5': (2, 1),
               '6': (0, 2),
               '7': (1, 2),
               '8': (2, 2)}

    g = GridViz(3, 3)
    g.setup()
    g.screen.fill((255, 255, 255))
    g.draw_grid()

    decision_counts = make_counter(decision_value_list)
    print(decision_counts)
    int_values = list(decision_counts.values())
    colors = create_color_range(int_values)

    for i, color in enumerate(colors):
        g.fill_space(mapping.get(str(i)), color=color)
        g.draw_text(mapping.get(str(i)), str(decision_counts.get(str(i))))

    pygame.display.flip()
    pygame.image.save(g.screen, f'{filename}.png')
    pygame.quit()


def reality_map(reality_value_list: list = [], filename: str = 'reality_map') -> None:
    """ 
    """

    mapping = {'0': (0, 0),
               '1': (1, 0),
               '2': (2, 0),
               '3': (0, 1),
               '4': (1, 1),
               '5': (2, 1),
               '6': (0, 2),
               '7': (1, 2),
               '8': (2, 2)}

    g = GridViz(3, 3)
    g.setup()
    g.screen.fill((255, 255, 255))
    g.draw_grid()

    reality_counts = make_counter(reality_value_list)
    print(reality_counts)
    int_values = list(reality_counts.values())
    colors = create_color_range(int_values)

    for i, color in enumerate(colors):
        g.fill_space(mapping.get(str(i)), color=color)
        g.draw_text(mapping.get(str(i)), str(reality_counts.get(str(i))))

    pygame.display.flip()
    pygame.image.save(g.screen, f'{filename}.png')
    pygame.quit()


def accuracy_map(accuracy_list: list = [], filename: str = 'accuracy_map') -> None:
    """ 
    """

    mapping = {'0': (0, 0),
               '1': (1, 0),
               '2': (2, 0),
               '3': (0, 1),
               '4': (1, 1),
               '5': (2, 1),
               '6': (0, 2),
               '7': (1, 2),
               '8': (2, 2)}

    g = GridViz(3, 3)
    g.setup()
    g.screen.fill((255, 255, 255))
    g.draw_grid()

    colors = create_color_range(accuracy_list)

    for i, color in enumerate(colors):
        g.fill_space(mapping.get(str(i)), color=color)
        g.draw_text(mapping.get(str(i)), str(accuracy_list[i]))

    pygame.display.flip()
    pygame.image.save(g.screen, f'{filename}.png')
    pygame.quit()
