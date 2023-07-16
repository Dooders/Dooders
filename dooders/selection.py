"""
This module implements Recursive Artificial Selection (RAS), a genetic 
programming approach that emulates natural selection in order to evaluate and 
evolve various designs. RAS operates by using surviving 'Dooders' from one 
simulation as the genetic foundation for subsequent simulations involving a 
new set of Dooders. Fit Dooders, those that successfully complete the simulation, 
are considered for recombination with other fit Dooders.

RAS leverages the principles of evolution to iteratively refine and optimize 
designs. By recombining genetic material from successful Dooders, RAS aims to 
enhance the overall fitness of the simulated population over time.

The key objectives of this module are to facilitate the execution of RAS and 
provide a framework for managing the genetic programming process. By employing 
RAS, users can explore and evolve designs that exhibit desirable traits, leading 
to improved solutions in a variety of domains.
"""

import random
from typing import List, Tuple

import numpy as np
from pydantic import BaseModel
from sklearn.decomposition import PCA

from dooders.experiment import Experiment
from dooders.sdk.modules.recombination import recombine

gene_embedding = PCA(n_components=3)


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


def get_embeddings(gene_pool: dict) -> List[dict]:
    """ 
    Returns a list of the embeddings of the weights of each dooder in a gene pool

    Parameters
    ----------
    gene_pool : (dict)
        A dictionary containing the dooder ids as keys and their weights as values

    Returns
    -------
    all_weights : (list)
        A list of the embeddings of the weights of each dooder in a gene pool
    """
    all_weights = []
    for dooder in gene_pool.values():
        genetic_weights = dooder['Consume'][0]
        environment_weights = dooder['Consume'][1]
        genetic_embedding = gene_embedding.fit(
            genetic_weights).singular_values_
        environment_embedding = gene_embedding.fit(
            environment_weights).singular_values_
        embedding = EmbeddingTemplate(
            genetic=genetic_embedding, environment=environment_embedding).dict()
        all_weights.append(embedding)

    return all_weights


def select_parents(gene_pool: dict) -> Tuple[tuple, tuple]:
    """ 
    Returns two random dooders' weights from a directory of weight files

    Parameters
    ----------
    gene_pool : (dict)
        A dictionary containing the dooder ids as keys and their weights as values

    Returns
    -------
    parent_a : (tuple)
        The id and weights of the first dooder
    parent_b : (tuple)
        The id and weights of the second dooder
    """

    parent_a, parent_b = random.sample(list(gene_pool.keys()), 2)

    parent_a_weights = gene_pool[parent_a]['Consume']
    parent_b_weights = gene_pool[parent_b]['Consume']

    return (parent_a, parent_a_weights), (parent_b, parent_b_weights)


def recombine_genes(gene_pool: dict, recombination_type: str = 'crossover') -> np.ndarray:
    """ 
    Produces a new set of genes from two random dooders' weights 
    from a provided gene pool

    Parameters
    ----------
    gene_pool : (dict)
        A dictionary containing the dooder ids as keys and their weights as values
    recombination_type : (str)
        The type of recombination to use. 
        Options are 'crossover', 'random','range', and 'average'

    Returns 
    -------
    new_genes : (np.ndarray)
        The new set of genes produced from the two random dooders' weights
    """

    parent_a, parent_b = select_parents(gene_pool)

    parent_a_genes = parent_a[1][0]
    parent_b_genes = parent_b[1][0]

    new_genes = recombine(parent_a_genes, parent_b_genes,
                          recombination_type=recombination_type)

    return np.array(new_genes)


def recursive_artificial_selection(settings: dict = DEFAULT_SETTINGS, generations: int = 100) -> list:
    """ 
    Runs a recursive artificial selection experiment

    Parameters
    ----------
    settings : (dict)
        The settings to use for the experiment
    iterations : (int)
        The number of iterations to run the experiment

    Returns
    -------
    results : (list)
        A list of the number of unique dooders in the gene pool after each iteration
    """

    gene_pool = {}
    results = {'fit_dooder_counts': [],
               'generation_embeddings': []
               }

    def inherit_weights(experiment):

        if gene_pool == {}:
            pass
        else:
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
        results['fit_dooder_counts'].append(len(experiment.gene_pool.keys()))
        results['generation_embeddings'].append(get_embeddings(gene_pool))
        del experiment

    return results
