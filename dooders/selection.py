"""
This module implements Recursive Artificial Selection (RAS), a genetic 
programming approach that emulates natural selection to evaluate and 
evolve various designs. RAS leverages the principles of evolution to 
iteratively refine and optimize designs, creating an enhanced generation 
of 'Dooders' based on the success of previous simulations.

The primary objectives of this module are to facilitate the execution 
of RAS and provide a comprehensive framework for managing the genetic 
programming process. This allows users to explore and evolve designs 
that exhibit desirable traits, improving solutions in various domains.
"""

import random
from typing import Dict, List, Tuple

import numpy as np
from pydantic import BaseModel
from sklearn.decomposition import PCA

from dooders.experiment import Experiment
from dooders.sdk.modules.recombination import recombine

# Global PCA instance for embedding
GENE_EMBEDDING = PCA(n_components=3)


class EmbeddingTemplate(BaseModel):
    genetic: np.ndarray
    environment: np.ndarray

    class Config:
        arbitrary_types_allowed = True


DEFAULT_SETTINGS = {
    'MaxCycles': 100,
    'SimulationCount': 1000,
    'RecombinationType': 'crossover',
    'GenePool': 'retain',
}


def get_embeddings(gene_pool: Dict[str, dict]) -> List[Dict[str, np.ndarray]]:
    """ 
    Returns a list of the embeddings of the weights of each Dooder in the provided
    gene pool.

    TODO: Add option to return centroids for the gene pool.

    Parameters
    ----------
    gene_pool : dict
        A dictionary containing the Dooder IDs as keys and their weights as values.

    Returns
    -------
    gene_pool_embeddings : list
        A list of the embeddings of the weights of each Dooder in the gene pool.
        Example: [{'genetic': [0.1, 0.2, 0.3], 'environment': [0.4, 0.5, 0.6]}]

    Example
    --------
    >>> gene_pool = {'dooder_1': {'Consume': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]}}
    >>> get_embeddings(gene_pool)
    [{'genetic': [0.1, 0.2, 0.3], 'environment': [0.4, 0.5, 0.6]}]
    """
    gene_pool_embeddings = []
    for dooder in gene_pool.values():

        genetic_weights = dooder['Consume'][0]
        environment_weights = dooder['Consume'][1]
        genetic_embedding = GENE_EMBEDDING.fit(
            genetic_weights).singular_values_
        environment_embedding = GENE_EMBEDDING.fit(
            environment_weights).singular_values_
        embedding = EmbeddingTemplate(
            genetic=genetic_embedding, environment=environment_embedding).dict()
        gene_pool_embeddings.append(embedding)

    return gene_pool_embeddings


def select_parents(gene_pool: Dict[str, dict]) -> Tuple[Tuple[str, np.ndarray], Tuple[str, np.ndarray]]:
    """ 
    Returns two random Dooders' weights from the gene pool.

    TODO: Implement a selection strategy to select the most fit Dooders.

    Parameters
    ----------
    gene_pool : dict
        A dictionary containing the Dooder IDs as keys and their weights as values.

    Returns
    -------
    Tuple[Tuple[str, np.ndarray], Tuple[str, np.ndarray]]
        A tuple containing two tuples, each containing a Dooder ID and their weights.
    """
    parent_a_id, parent_b_id = random.sample(gene_pool.keys(), 2)
    parent_a_weights = gene_pool[parent_a_id]['Consume']
    parent_b_weights = gene_pool[parent_b_id]['Consume']

    return (parent_a_id, parent_a_weights), (parent_b_id, parent_b_weights)


def recombine_genes(gene_pool: Dict[str, dict], recombination_type: str = 'crossover') -> np.ndarray:
    """ 
    Produces a new set of genes from two random Dooders' weights 
    from a provided gene pool.

    TODO: Add a "one-parent" option to allow for a single parent to be used for recombination.

    Current recombination types: 'crossover', 'random', 'range', 'average'

    Parameters
    ----------
    gene_pool : dict
        A dictionary containing the Dooder IDs as keys and their weights as values.
    recombination_type : str, optional
        The type of recombination to use (default is 'crossover').

    Returns 
    -------
    np.ndarray
        A new set of genes produced from two random Dooders' weights 
        from the provided gene pool.
    """
    parent_a, parent_b = select_parents(gene_pool)
    recombined_genes = recombine(
        parent_a[1], parent_b[1], recombination_type=recombination_type)

    return np.array(recombined_genes, dtype=object)


def recursive_artificial_selection(settings: Dict[str, str] = DEFAULT_SETTINGS,
                                   generations: int = 100) -> Dict[str, List]:
    """ 
    Runs a Recursive Artificial Selection (RAS) experiment.

    Intended to evaluate the evolutionary potential of a design, RAS
    leverages the principles of evolution to iteratively refine and
    optimize designs, creating an enhanced generation of 'Dooders' based
    on the success of previous simulations.

    Parameters
    ----------
    settings : dict, optional
        The settings to use for the experiment (default is DEFAULT_SETTINGS).
    generations : int, optional
        The number of generations for the experiment (default is 100).

    Returns
    -------
    dict
        A dictionary containing the count of fit Dooders and the generation 
        embeddings after each generation. Containing a list of the count of
        fit Dooders and a list of the generation embeddings for each generation.
    """
    gene_pool = {}
    experiment_results = {'fit_dooder_counts': [], 'generation_embeddings': []}

    def inherit_weights(experiment: Experiment):
        """ 
        Inherit the weights of the Dooders in the gene pool.
        """
        if gene_pool:
            new_genes = recombine_genes(
                gene_pool, recombination_type=settings['RecombinationType'])
            dooder = experiment.simulation.arena.get_dooder()
            dooder.internal_models['Consume'].inherit_weights(new_genes)

    for i in range(generations):
        experiment = Experiment(settings)
        experiment.batch_simulate(settings['SimulationCount'],
                                  i+1,
                                  'recursive_artificial_selection',
                                  custom_logic=inherit_weights)
        gene_pool = experiment.gene_pool.copy()
        experiment_results['fit_dooder_counts'].append(len(gene_pool))
        experiment_results['generation_embeddings'].append(
            get_embeddings(gene_pool))

    return experiment_results
