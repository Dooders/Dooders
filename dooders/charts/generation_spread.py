from typing import Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def avg_dist_to_centroid(df: pd.DataFrame) -> float:
    """ 
    Calculates the average distance from each point to the centroid of a
    dataframe of centroids.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of the centroids for a given layer and recombination type.

    Returns
    -------
    float
        The average distance from each point to the centroid of a 
        dataframe of centroids.
    """
    centroid = df[['X', 'Y', 'Z']].mean().values

    # Calculate the distance from each point to the centroid
    distances = np.sqrt(
        ((df[['X', 'Y', 'Z']] - centroid) ** 2).sum(axis=1))

    return distances.mean()


def generation_spread(df: pd.DataFrame,
                      save_path: Union[str, None] = None,
                      layer: str = '') -> None:
    """ 
    Calculates the spread of a dataframe of centroids.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of the centroids for a given layer and recombination type.
    save_path : Union[str, None], optional
        The path to save the chart to. If None, the chart is not saved
        (the default is None).
    layer : str, optional
        The layer to display the results for. Static or Dynamic.
    """
    df['generation'] = df['generation'].astype('int')
    grouped_df = df.groupby('generation')
    data = grouped_df.apply(avg_dist_to_centroid).to_dict()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(data.keys()), y=list(
        data.values()), mode='lines+markers'))
    fig.update_layout(title='Average Distance from Centroid (Generation Spread)',
                      xaxis_title='Generation', yaxis_title='Average Distance')

    if save_path:
        fig.write_image(f'{save_path}_{layer}_generation_spread.png',
                        format='png',
                        scale=2,
                        engine='orca')

    fig.show()
