from typing import List, Optional, Tuple

import pygame

from dooders.charts.grid import GridViz

Position = Tuple[int, int]

POSITION_MAP = {
    '0': (0, 0),
    '1': (1, 0),
    '2': (2, 0),
    '3': (0, 1),
    '4': (1, 1),
    '5': (2, 1),
    '6': (0, 2),
    '7': (1, 2),
    '8': (2, 2)
}


def validate_position(position: str) -> Position:
    """
    Validate the position and return the mapped value.

    Parameters
    ----------
    position : str
        Position to be validated and mapped.

    Returns
    -------
    Tuple[int, int]
        The mapped position as a tuple.
    """
    if position not in POSITION_MAP:
        raise ValueError(
            f'Invalid position value: {position}. Must be between 0 and 8.')
    return POSITION_MAP[position]


def visualize_perception_state(cycle_count: int,
                               filename: str = 'perception_state_grid',
                               energy_positions: List[str] = [],
                               decision: Optional[str] = None,
                               draw_agent: bool = True
                               ) -> None:
    """ 
    Creates a grid visualization of the agent's perception state.

    Parameters
    ----------
    cycle_count : int
        The current cycle count of the agent.
    filename : str, optional
        The filename of the image to be saved. The default is 'perception_state_grid'.
    energy_positions : list of str, optional
        A list of positions of energy in the grid. The default is [].
        For example, ['1', '3', '7'].
    decision : str, optional
        The decision made by the agent. The default is None. This will be
        highlighted red if the decision is to move to a position without energy,
        and green if the decision is to move to a position with energy.
    """
    grid = GridViz(3, 3)
    grid.setup()
    grid.screen.fill((255, 255, 255))
    grid.draw_grid()

    if decision:
        decision_position = validate_position(decision)
        decision_color = (
            0, 255, 0) if decision in energy_positions else (255, 0, 0)
        grid.fill_space(decision_position, decision_color)

    if energy_positions:
        for position in energy_positions:
            energy_position = validate_position(position)
            grid.draw_energy(energy_position)

    if draw_agent:
        grid.draw_agent((1, 1))

    grid.draw_cycle_counter(cycle_count + 1)
    pygame.display.flip()
    pygame.image.save(grid.screen, f'{filename}.png')
    pygame.quit()
