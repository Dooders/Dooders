from typing import Any, List

from PIL import Image, ImageColor, ImageDraw, ImageFont
from pydantic import BaseModel

# Define the dimensions of the grid and cells
grid_size = 3
cell_size = 200  # Increased cell size
padding = 20  # Increased padding
cell_radius = 20  # Adjusted cell radius


class ImageObject(BaseModel):
    grid_size: int = 3
    cell_size: int = 200
    padding: int = 20
    cell_radius: int = 20
    image: Any


def base_grid(grid_size: int = grid_size,
              cell_size: int = cell_size,
              padding: int = padding,
              cell_radius: int = cell_radius) -> Image:
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

    return ImageObject(image=image, grid_size=grid_size, cell_size=cell_size, padding=padding, cell_radius=cell_radius)


def add_mask_to_cells(base_image: ImageObject,
                      mask_positions: list,
                      mask_color_name: str = 'black') -> Image.Image:
    """
    Add semi-transparent black mask to specific grid cells.

    Parameters
    ----------
    base_image : Image
        The base grid image.
    mask_positions : list
        List of positions (integers) of cells to be masked.
    mask_color_name : str
        The color name of the mask.

    Returns
    -------
    Image
        The image with the black mask added to the specified cells.
    """
    # Create a copy of the base image to avoid modifying the original image
    # image = base_image.image.copy()
    draw = ImageDraw.Draw(base_image.image)

    # Define the mask color with transparency (semi-transparent black)
    mask_color = ImageColor.getrgb(mask_color_name) + (128,)

    # Draw the mask on the specified cells
    for position in mask_positions:
        if position < 1 or position > base_image.grid_size**2:
            continue

        # Calculate the row and column based on the position
        row = (position - 1) // base_image.grid_size
        col = (position - 1) % base_image.grid_size

        # Calculate the top-left and bottom-right coordinates of the cell
        x1 = base_image.padding + col * \
            (base_image.cell_size + base_image.padding)
        y1 = base_image.padding + row * \
            (base_image.cell_size + base_image.padding)
        x2 = x1 + base_image.cell_size
        y2 = y1 + base_image.cell_size

        # Draw the rounded rectangle with the mask color
        draw.rounded_rectangle(
            [(x1, y1), (x2, y2)], fill=mask_color, outline=None, radius=base_image.cell_radius)

    return base_image


def add_text(image, title: str):
    """
    Add a title above the image.

    Parameters
    ----------
    image : ImageObject
        The base image object.
    title : str
        The title to be added above the image.

    Returns
    -------
    ImageObject
        The image object with the title added above.
    """
    # Create a copy of the original image object
    new_image = image.image.copy()

    # Set the font size and font type
    font_size = 75
    font = ImageFont.truetype('Roboto-Bold.ttf', font_size)

    # Calculate the required width and height for the new image
    text_width, text_height = font.getsize(title)
    new_width = max(new_image.width, text_width)
    new_height = new_image.height + text_height

    # Create a new image with the updated size
    combined_image = Image.new('RGB', (new_width, new_height), color='white')

    # Paste the original image below the title
    combined_image.paste(new_image, (0, text_height))

    # Draw the text on the combined image with an offset
    draw = ImageDraw.Draw(combined_image)
    title_offset = 20  # Specify the desired offset in pixels
    draw.text((title_offset, 0), title, fill='black', font=font)

    return combined_image


def horizontal_composition(image_list: List[ImageObject]) -> Image.Image:
    """  
    Compose all the images in a list horizontally into a single image

    Parameters
    ----------
    image_list : List[Image]
        List of images to be composed horizontally

    Returns
    -------
    Image
        The composed image
    """

    # Get the width and height of the images
    widths, heights = zip(*(image.size for image in image_list))

    # Create a new image with the width of all the images and the height of the tallest image
    new_image = Image.new('RGB', (sum(widths), max(heights)))

    # Paste each image into the new image
    x_offset = 0
    for image in image_list:
        new_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]

    return new_image