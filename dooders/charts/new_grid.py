from PIL import Image, ImageDraw

# Define the dimensions of the grid and cells
grid_size = 3
cell_size = 200  # Increased cell size
padding = 20  # Increased padding
cell_radius = 20  # Adjusted cell radius


def base_grid(grid_size: int, cell_size: int, padding: int, cell_radius: int) -> Image:
    """
    Base grid graphic

    Parameters
    ----------
    grid_size : int
        The number of cells in the grid.
    cell_size : int
        The size of each cell in the grid.
    padding : int
        The padding between each cell.
    cell_radius : int
        The radius of the cell's rounded corners.

    Returns
    -------
    Image
        The base grid image.
    """
    # Calculate the total size of the grid visualization
    viz_size = (cell_size * grid_size) + (padding * (grid_size + 1))

    # Create a new white image with the desired size
    image = Image.new("RGB", (viz_size, viz_size), "white")
    draw = ImageDraw.Draw(image)

    # Define the light grey background color
    bg_color = (220, 220, 220)

    # Draw the cells with rounded corners and the background color
    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate the top-left and bottom-right coordinates of the cell
            x1 = padding + col * (cell_size + padding)
            y1 = padding + row * (cell_size + padding)
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Draw the rounded rectangle with the background color
            draw.rounded_rectangle(
                [(x1, y1), (x2, y2)], fill=bg_color, outline=None, radius=cell_radius)

    return image
