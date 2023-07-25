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

    grouped_df = df.groupby('generation')

    centroid = grouped_df[['X', 'Y', 'Z']].mean().values

    # Calculate the distance from each point to the centroid
    distances = np.sqrt(
        ((grouped_df[['X', 'Y', 'Z']] - centroid) ** 2).sum(axis=1))

    return distances.mean()


def generation_spread(df: pd.DataFrame):
    """ 
    Calculates the spread of a dataframe of centroids.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of the centroids for a given layer and recombination type.
    """

    data = df.apply(avg_dist_to_centroid).to_dict()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(data.keys()), y=list(
        data.values()), mode='lines+markers'))
    fig.update_layout(title='Average Distance from Centroid (Generation Spread)',
                      xaxis_title='Generation', yaxis_title='Average Distance')

    fig.show()
