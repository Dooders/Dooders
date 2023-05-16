from dooders.grid_viz import GridViz
import pygame

def perception_state_grid(cycle_count: int, 
                          filename: str = 'perception_state_grid', 
                          energy_positions: list = []) -> None:
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
    """
    
    mapping = {'0': (0,0), 
               '1': (1,0), 
               '2': (2,0), 
               '3': (0,1), 
               '4': (1,1), 
               '5': (1,2), 
               '6': (2,0), 
               '7': (2,1), 
               '8': (2,2)}
    
    g = GridViz(3,3)
    g.setup()
    g.screen.fill((255, 255, 255))
    g.draw_grid()
    
    if energy_positions:
        for position in energy_positions:
            final_position = mapping.get(position)
            g.draw_energy(final_position)
            
    g.draw_agent((1,1))
            
    g.draw_cycle_counter(cycle_count)
    pygame.display.flip()
    pygame.image.save(g.screen, f'{filename}.png')
    pygame.quit()