import json
import math
import os
import shutil
import statistics
from typing import Any, Dict, Optional

import pandas as pd
from IPython.display import Markdown, display

from dooders.charts.evolution_speed import evolution_speed
from dooders.charts.fit_count_and_accuracy import fit_count_and_accuracy
from dooders.charts.gene_embedding import gene_embedding
from dooders.charts.generation_spread import generation_spread
from dooders.sdk.modules.recombination import RECOMBINATION_TYPES


def euclidean_distance(coord1: tuple, coord2: tuple) -> float:
    """ 
    Calculates the euclidean distance between two points.

    Parameters
    ----------
    coord1 : tuple
        The first point.
    coord2 : tuple
        The second point.

    Returns
    -------
    float
        The euclidean distance between two points.
    """
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

    if layer not in ['dynamic', 'static']:
        raise ValueError(
            f"Layer must be 'dynamic' or 'static', not '{layer}'.")

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


def display_layer_results(layer: str,
                          results: Dict[str, Any],
                          save_path: str) -> None:
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
    save_path : str
        The path to save the charts to. If None, the charts will not be saved.
    """
    title = layer.capitalize()
    display(Markdown('## ' + title + ' Embeddings'))
    df = get_embedding_df(layer, results)
    centroid_df = df.groupby('generation').mean().reset_index()
    centroid_distance = evolution_distance(centroid_df)
    display(Markdown(f'### Evolution distance: {centroid_distance}'))

    gene_embedding(df,
                   title=f'{title} Layer Embeddings',
                   color_by='generation',
                   save_path=save_path,
                   show_cbar=False,
                   layer=layer)

    gene_embedding(centroid_df,
                   title=f'{title} Layer Embedding Centroids',
                   color_by='generation',
                   save_path=save_path,
                   show_cbar=False,
                   layer=layer)

    generation_spread(df, save_path=save_path, layer=layer)
    evolution_speed(centroid_df, save_path=save_path, layer=layer)


def load_results(type: str, experiment_name: str) -> Dict[str, Any]:
    """ 
    Loads the results of the experiment from a JSON file.

    Parameters
    ----------
    type : str
        Recombination type. i.e. crossover, averaging, lottery, random_range, none.
    experiment_name : str
        The name of the experiment to load the results from.

    Returns
    -------
    Dict[str, Any]
        The results of the experiment.
    """
    try:
        with open(f'results/{experiment_name}/{type}.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{type}.json' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file '{type}.json'.")
    except Exception as e:
        raise RuntimeError(
            f"Error loading results from file '{type}.json': {e}")

    return results


def display_report(recombination_type: str = None,
                   results: Dict[str, Any] = None,
                   experiment_name: Optional[str] = None,
                   save_charts: bool = False) -> None:
    """ 
    Displays a report for the recursive artificial selection experiment.

    Parameters
    ----------
    recombination_type : str
        The type of recombination used in the experiment. Static or Dynamic.
    results : Dict[str, Any], optional
        The results of the recursive artificial selection experiment.
    experiment_name : str, optional
        The name of the experiment to load the results from (default is None).
    """
    if results is None and experiment_name:
        results = load_results(recombination_type, experiment_name)

    if results is None:
        raise ValueError(
            "Results dictionary is not provided, and experiment_name is not valid.")

    try:
        with open(f'results/{experiment_name}/settings.json', 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = None

    if save_charts:
        chart_path = f'results/{experiment_name}/charts'
        save_path = f'{chart_path}/{recombination_type}_'
        if os.path.exists(chart_path):
            pass
        else:
            os.makedirs(chart_path)
    else:
        save_path = None

    # Display the recombination type
    display(Markdown(f'# {recombination_type.capitalize()} Recombination'))
    print(f"Settings: {settings}\n")

    dooder_counts = results['fit_dooder_counts']
    average_accuracies = [statistics.mean(
        values) for values in results['accuracies']]

    # Display the fit count and accuracy plot
    fit_count_and_accuracy(dooder_counts, average_accuracies, save_path)

    # Display the static layer embeddings
    display_layer_results('static', results, save_path)

    # Display the dynamic layer embeddings
    display_layer_results('dynamic', results, save_path)


def report(recombination_type: str = None,
           results: Dict[str, Any] = None,
           experiment_name: Optional[str] = None,
           save_charts: bool = False) -> None:
    """ 
    Generates a report for the recursive artificial selection experiment.

    If recombination_type is None, then a report is generated for
    each recombination type.

    Parameters
    ----------
    recombination_type : str, optional
        The type of recombination used in the experiment. Static or Dynamic.
    results : Dict[str, Any], optional
        The results of the recursive artificial selection experiment.
    experiment_name : str, optional
        The name of the experiment to load the results from (default is None).
    """

    recombination_types = list(RECOMBINATION_TYPES.keys())

    if recombination_type is None:
        for recombination_type in recombination_types:
            display_report(recombination_type,
                           results,
                           experiment_name,
                           save_charts)
    else:
        display_report(recombination_type,
                       results,
                       experiment_name,
                       save_charts)
