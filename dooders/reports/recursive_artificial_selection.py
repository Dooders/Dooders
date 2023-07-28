import math
import statistics
from typing import Any, Dict

import pandas as pd
from IPython.display import Markdown, display

from dooders.charts.evolution_speed import evolution_speed
from dooders.charts.fit_count_and_accuracy import fit_count_and_accuracy
from dooders.charts.gene_embedding import gene_embedding
from dooders.charts.generation_spread import generation_spread

recombination_types = ['crossover', 'average', 'random', 'range', 'none']


def euclidean_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)


def get_embedding_df(layer: str, results: Dict[str, Any]) -> pd.DataFrame:
    """ 
    Returns a dataframe of the embeddings for a given layer and recombination type.

    Parameters
    ----------
    layer : str
        The layer to get the embeddings for. Static or Dynamic.
    results : Dict[str, Any]
        The results of the recursive artificial selection experiment.

    Returns
    -------
    pd.DataFrame
        A dataframe of the embeddings for a given layer and recombination type.
        Columns: X, Y, Z, generation
    """

    generation_list = [[[list(v) for k, v in a.items() if k == layer]
                        for a in d] for d in results['generation_embeddings']]

    flattened_data = [(*embedding[0], generation) for generation,
                      embeddings in enumerate(generation_list) for embedding in embeddings]

    df = pd.DataFrame(flattened_data, columns=['X', 'Y', 'Z', 'generation'])
    df['generation'] = df['generation'].astype('str')

    return df


def evolution_distance(df: pd.DataFrame) -> float:
    """ 
    Calculates the distance between the first and last point in a dataframe
    of centroids.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of the centroids for a given layer and recombination type.

    Returns
    -------
    float
        The distance between the first and last point in a dataframe of centroids.
    """
    if not df.empty:
        first_x, *_, last_x = df['X'].tolist()
        first_y, *_, last_y = df['Y'].tolist()

    return euclidean_distance((first_x, first_y), (last_x, last_y))


def display_layer_results(layer: str, results: Dict[str, Any]) -> None:
    """ 
    Displays the results for a given layer.

    Including:
    - Evolution distance
    - Static layer embeddings
    - Dynamic layer embeddings
    - Generation spread
    - Evolution speed

    Parameters
    ----------
    layer : str
        The layer to display the results for. Static or Dynamic.
    results : Dict[str, Any]
        The results of the recursive artificial selection experiment.
    """
    title = layer.capitalize()
    display(Markdown('## ' + title + ' Embeddings'))
    df = get_embedding_df(layer, results)
    centroid_df = df.groupby('generation').mean().reset_index()
    centroid_distance = evolution_distance(centroid_df)
    display(Markdown(f'### Evolution distance: {centroid_distance}'))
    gene_embedding(df, color_by='generation').show()
    gene_embedding(
        centroid_df, title=f'{title} Centroid', color_by='generation').show()
    generation_spread(df)
    evolution_speed(centroid_df)


def report(recombination_type: str, results: Dict[str, Any]) -> None:
    """ 
    Generates a report for the recursive artificial selection experiment.

    Parameters
    ----------
    recombination_type : str
        The type of recombination used in the experiment. Static or Dynamic.
    results : Dict[str, Any]
        The results of the recursive artificial selection experiment.
    """

    # Display the recombination type
    display(Markdown(f'# {recombination_type.capitalize()} Recombination'))

    dooder_counts = results['fit_dooder_counts']
    average_accuracies = [statistics.mean(
        values) for values in results['accuracies']]

    # Display the fit count and accuracy plot
    fit_count_and_accuracy(dooder_counts, average_accuracies)

    # Display the static layer embeddings
    display_layer_results('static', results)

    # Display the dynamic layer embeddings
    display_layer_results('dynamic', results)
