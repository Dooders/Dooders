from typing import List, Tuple

import imageio

from dooders.charts.grid import Grid


def convert_to_positions(move_history: List[int], grid_size: int) -> List[Tuple[int, int]]:
    """ 
    Converts a list of moves to a list of positions.

    Parameters
    ----------
    move_history : List[int]
        The list of moves.

    Returns
    -------
    List[Tuple[int, int]]
        The list of positions.
    """
    positions = []
    for move in move_history:
        row = move // grid_size
        col = move % grid_size
        positions.append((row, col))

    return positions


def get_opacity(count: int) -> float:
    """ 
    Returns the opacity of the cell based on the number of times it has been visited.

    Parameters
    ----------
    count : int
        The number of times the cell has been visited.

    Returns
    -------
    float
        The opacity of the cell.
    """
    opacity_map = {
        1: 0.2,
        2: 0.3,
        3: 0.4,
        4: 0.5,
        5: 0.6,
        6: 0.7
    }

    return opacity_map.get(count, 0.8)


def animate_move_history(positions: List[Tuple[int, int]],
                         filename: str = 'move_history.gif',
                         fps: int = 5) -> None:
    """ 
    Creates an animated gif of the move history.

    Parameters
    ----------
    positions : List[Tuple[int, int]]
        The list of positions that the dooder has visited.
    filename : str
        The name of the file to save the gif to.
    fps : int
        The number of frames per second.
    """

    grid = Grid(grid_size=5)
    image = grid.image

    image_list = []
    position_history = {position: 0 for position in positions}

    for i in range(len(positions)):

        position_history[positions[i]] += 1
        position_count = position_history.get(positions[i])
        opacity = get_opacity(position_count)
        if i > 0:
            image = grid.shade_cell(
                image, positions[i-1], opacity=opacity, color='black')
        new_image = grid.shade_cell(
            image, positions[i], opacity=1.0, color='green')
        new_image = grid.add_text(new_image, f"Cycle #{i}")
        image_list.append(new_image.copy())

    imageio.mimsave(filename, image_list, fps=fps)
