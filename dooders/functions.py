import pygame

from dooders.grid_viz import GridViz


def perception_state_grid(cycle_count: int,
                          filename: str = 'perception_state_grid',
                          energy_positions: list = [],
                          decision: str = None
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
               '5': (1, 2),
               '6': (2, 0),
               '7': (2, 1),
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

        g.fill_space(mapping.get(decision), space_color)

    if energy_positions:
        for position in energy_positions:
            final_position = mapping.get(position)
            g.draw_energy(final_position)

    g.draw_agent((1, 1))

    g.draw_cycle_counter(int(cycle_count) + 1)
    pygame.display.flip()
    pygame.image.save(g.screen, f'{filename}.png')
    pygame.quit()
