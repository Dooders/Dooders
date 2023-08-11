import io
from typing import Union

import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import LANCZOS

embedding_map = {0: 'EmbeddingA', 1: 'EmbeddingB', 2: 'EmbeddingC'}


def gene_embedding(dooder_df,
                   color_by: str = 'cycle',
                   show_cbar: bool = True,
                   title: str = 'Gene Embedding',
                   save_path: Union[str, None] = None,
                   layer: Union[str, None] = None) -> px.scatter:
    """ 
    Create a scatter plot of the gene embeddings.

    Parameters
    ----------
    dooder_df : pd.DataFrame
        The dooder dataframe.
    color_by : str
        The column to color by.
    show_cbar : bool
        Whether to show the colorbar.
    title : str
        The title of the plot.
    save_path : Union[str, None]
        The path to save the plot to. If None, the plot is not saved.
    layer : Union[str, None]
        The layer the embeddings are from.

    Returns
    -------
    fig : px.scatter
        The scatter plot of a 2D embedding.
    """

    # If the dooder_df does not have X and Y columns, create them
    if 'X' not in dooder_df.columns:
        temp_df = dooder_df.copy()[['last_encoding', color_by]]
        temp_df['X'] = temp_df['last_encoding'].apply(lambda x: x[0])
        temp_df['Y'] = temp_df['last_encoding'].apply(lambda x: x[1])
    else:
        temp_df = dooder_df.copy()[['X', 'Y', color_by]]

    # Create the scatter plot
    fig = px.scatter(temp_df,
                     x="X",
                     y="Y",
                     color=color_by,
                     title=title,
                     color_continuous_scale="Viridis")

    # Remove axis titles
    fig.update_xaxes(title='Feature-A')
    fig.update_yaxes(title='Feature-B')

    # Remove tick labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    # Remove the color legend
    fig.update_layout(showlegend=False)

    if show_cbar:
        fig.update_layout(coloraxis_colorbar=dict(
            title=color_by))

    if save_path is not None:
        if 'Centroid' in title:
            final_save_path = f'{save_path}_{layer}_centroid_embedding.png'
        else:
            final_save_path = f'{save_path}_{layer}_gene_embedding.png'

        fig.write_image(final_save_path,
                        format='png',
                        scale=2,
                        engine='orca')

    fig.show()


def gene_embedding_1d(values: list, component: int = 0, padding: float = 0.02) -> go.Figure:
    """ 
    Create a 1D scatter plot of the gene embeddings.

    Parameters
    ----------
    values : list
        A list of gene embeddings.
    component : int
        The component to plot.
    padding : float
        The padding to add to the plot.

    Returns
    -------
    fig : go.Figure
        The 1D scatter plot.
    """
    x_data = [x[component] for x in values]
    x_min = min(x_data)
    x_max = max(x_data)
    x_padding = padding * (x_max - x_min)

    trace = go.Scatter(
        y=[0] * len(values),
        x=x_data,
        mode='markers',
        marker=dict(
            size=10,
            color=list(range(len(values))),
            colorscale='Viridis',
            showscale=False
        )
    )

    layout = go.Layout(
        plot_bgcolor='rgba(218, 218, 218, 10)',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[x_min - x_padding, x_max + x_padding],
            gridcolor='rgba(218, 218, 218, 10)'
        ),
        yaxis=dict(showgrid=False, showticklabels=False,
                   gridcolor='rgba(218, 218, 218, 10)'),
        width=1000,
        height=100,
        margin=dict(l=2, r=0, t=0, b=0)
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def compose_images(figures: list,
                   filenames: list,
                   padding_right: int = 20,
                   label_padding_x: int = 10,
                   label_padding_y: int = 10,
                   font_size: int = 18) -> Image:
    """ 
    Compose a list of images into a single image.

    Parameters
    ----------
    figures : list
        A list of Plotly figures.
    filenames : list
        A list of filenames.
    padding_right : int
        The padding to add to the right of the image.
    label_padding_x : int
        The padding to add to the x-coordinate of the label.
    label_padding_y : int
        The padding to add to the y-coordinate of the label.
    font_size : int
        The font size of the label.

    Returns
    -------
    composed_image : Image
    """
    images = []
    max_width = 0
    total_height = 0

    # Generate the images from the Plotly figures and calculate dimensions
    for fig in figures:
        image_bytes = fig.to_image(format="png", engine="orca")
        image = Image.open(io.BytesIO(image_bytes))
        images.append(image)
        max_width = max(max_width, image.width)
        total_height += image.height

    # Calculate the total width for the composed image with padding
    total_width = max_width + padding_right

    # Create a blank canvas for the composed image with padding
    composed_image = Image.new(
        'RGB', (total_width, total_height - 35), color=(218, 218, 218))

    # Create a font object for the labels
    font = ImageFont.truetype("Roboto-Bold.ttf", font_size)

    # Create a new drawing object for the composed image
    draw = ImageDraw.Draw(composed_image)

    # Calculate the maximum label width
    max_label_width = max(draw.textbbox((0, 0), filename, font=font)[
                          2] for filename in filenames)

    # Add each image and label to the composed image
    label_y = 0
    for image, filename in zip(images, filenames):
        # Calculate the x-coordinate for centering the label horizontally
        label_x = label_padding_x

        # Calculate the y-coordinate for centering the label vertically
        label_center_y = label_y + (image.height - font.size) // 2

        # Add the label
        draw.text((label_x, label_center_y - label_padding_y),
                  filename, font=font, fill='black')

        # Resize the image while maintaining aspect ratio
        image.thumbnail((max_width - max_label_width -
                        label_padding_x * 2, image.height), LANCZOS)

        # Add the image
        composed_image.paste(
            image, (max_label_width + label_padding_x * 2, label_y))

        # Update the position variables for the next iteration
        label_y += image.height

    return composed_image
