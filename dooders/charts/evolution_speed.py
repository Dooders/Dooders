import math
from typing import List

import pandas as pd
import plotly.graph_objects as go


def euclidean_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)


def generational_distance(df: pd.DataFrame) -> List[float]:
    """ 
    Calculates the distance between each generation (X, Y) and the previous
    generation.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of the embeddings for a given layer and recombination type.

    Returns
    -------
    List[float]
        The distance between each generation (X, Y) and the other.
    """

    # Calculate the distance between each generation (X, Y) and the other
    distances = []
    for i in range(len(df) - 1):
        current_coords = (df['X'][i], df['Y'][i])
        next_coords = (df['X'][i + 1], df['Y'][i + 1])
        distance = euclidean_distance(current_coords, next_coords)
        distances.append(distance)

    return distances


def evolution_speed(df: pd.DataFrame, 
                    save_path: str = None, 
                    layer: str = None) -> None:
    """ 
    Calculates the spread of a dataframe of centroids.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of the centroids for a given layer and recombination type.
    save_path : str, optional
        The path to save the chart to. If None, the chart is not saved.
    layer : str, optional
        The layer to get the embeddings for. Static or Dynamic.
    """
    df['generation'] = df['generation'].astype('int')
    df = df.sort_values('generation')
    df = df.reset_index()
    data = generational_distance(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(data))), y=list(
        data), mode='lines+markers'))
    fig.update_layout(title='Evolution Speed',
                      xaxis_title='Generation', yaxis_title='Distance')
    
    if save_path:
        fig.write_image(f'{save_path}_{layer}_evolution_speed.png',
                        format='png',
                        scale=2,
                        engine='orca')

    fig.show()
