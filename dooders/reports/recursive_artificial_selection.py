import statistics
from typing import Any, Dict

import pandas as pd
from IPython.display import Markdown, display

from dooders.charts.fit_count_and_accuracy import fit_count_and_accuracy
from dooders.charts.gene_embedding import gene_embedding

recombination_types = ['crossover', 'average', 'random', 'range', 'none']


def get_embedding_df(layer: str, results: Dict[str, Any]) -> pd.DataFrame:
    """ 
    Returns a dataframe of the embeddings for a given layer and recombination type.

    Parameters
    ----------
    layer : str
        The layer to get the embeddings for. Genetic or Adaptive.
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

    return df


def report(recombination_type: str, results: Dict[str, Any]) -> None:
    """ 
    Generates a report for the recursive artificial selection experiment.
    
    Including: 
    - Count and accuracy plot
    - Genetic embeddings
    - Adaptive embeddings
    
    Parameters
    ----------
    recombination_type : str
        The type of recombination used in the experiment. Genetic or Adaptive.
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

    # Display the genetic embeddings
    display(Markdown('## Genetic Embeddings'))
    genetic_df = get_embedding_df('genetic', results)
    gene_embedding(genetic_df)
    centroid_df = genetic_df.groupby('generation').mean().reset_index()
    gene_embedding(centroid_df, title='Genetic Centroid')

    # Display the adaptive embeddings
    display(Markdown('## Adaptive Embeddings'))
    adaptive_df = get_embedding_df('adaptive', results)
    gene_embedding(adaptive_df)
    centroid_df = adaptive_df.groupby('generation').mean().reset_index()
    gene_embedding(centroid_df, title='Adaptive Centroid')






    # Count and accuracy plot

    ### Genetic Embeddings ###
    # Centroid and embedding plots (side by side?)
    # Spread by generation plot
    # Evolution speed by generation plot
    # Overall distance metric (start to end)

    ### Adaptive Embeddings ###
    # Centroid and embedding plots (side by side?)
    # Spread by generation plot
    # Evolution speed by generation plot
    # Overall distance metric (start to end)

    # Then have a function for comparative analysis
