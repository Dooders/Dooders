""" 
This experiment implements Recursive Artificial Selection (RAS), a genetic 
programming approach that emulates natural selection to evaluate and 
evolve various designs. RAS leverages the principles of evolution to 
iteratively refine and optimize designs, creating an enhanced generation 
of 'Dooders' based on the success of previous simulations.

The primary objectives of this module are to facilitate the execution 
of RAS and provide a comprehensive framework for managing the genetic 
programming process. This allows users to explore and evolve designs 
that exhibit desirable traits, improving solutions in various domains.
"""

import json
import os
import shutil
from typing import Dict, List

from dooders.data.experiment_results import calculate_accuracies
from dooders.data.inference_record_dataframe import get_inference_record_df
from dooders.experiment import Experiment
from dooders.reports.recursive_artificial_selection import report
from dooders.selection import get_embeddings, recombine_genes

DEFAULT_SETTINGS = {
    'MaxCycles': 100,
    'SimulationCount': 2000,
    'RecombinationType': 'crossover',
    'GenePool': 'retain',
    'Generations': 50,
}


def save_results(type: str, results: Dict[str, List], filename: str = 'results.json') -> None:
    """ 
    Saves the results of the experiment to a JSON file.

    Parameters
    ----------
    type : str
        The type of experiment (the recombination type).
    results : dict
        The results of the experiment.
    filename : str, optional
        The name of the file to save the results to (default is 'results.json').
    """
    if not os.path.exists(f'results/ras/{type}'):
        os.makedirs(f'results/ras/{type}')
    else:
        shutil.rmtree(f'results/ras/{type}')
        os.makedirs(f'results/ras/{type}')

    with open(f'results/ras/{type}/{filename}', 'w') as f:
        json.dump(results, f)


def load_results(type: str, filename: str = 'results.json') -> Dict[str, List]:
    """ 
    Loads the results of the experiment from a JSON file.

    Parameters
    ----------
    type : str
        The type of experiment (the recombination type).
    filename : str, optional
        The name of the file to load the results from (default is 'results.json').

    Returns
    -------
    dict
        The results of the experiment.
    """
    with open(f'results/ras/{type}/{filename}', 'r') as f:
        results = json.load(f)

    return results


def get_accuracies(results: Dict[str, List]) -> List[float]:

    inference_df = get_inference_record_df(results)
    accuracies = calculate_accuracies(inference_df)

    return [accuracy for accuracy in accuracies.values()]


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
    experiment_results = {'fit_dooder_counts': [],
                          'generation_embeddings': [],
                          'accuracies': []}

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

        experiment_results['accuracies'].append(
            get_accuracies(experiment.experiment_results))
        experiment_results['fit_dooder_counts'].append(len(gene_pool))
        experiment_results['generation_embeddings'].append(
            get_embeddings(gene_pool))

    return experiment_results


def run_experiment(settings: Dict[str, str] = DEFAULT_SETTINGS,
                   show_report: bool = True,
                   save_results: bool = True) -> None:
    """ 
    Runs a Recursive Artificial Selection (RAS) experiment for each recombination type.

    Saves the results of each experiment to a JSON file in the results folder.

    Parameters
    ----------
    settings : dict, optional
        The settings to use for the experiment (default is DEFAULT_SETTINGS).
    show_report : bool, optional
        Whether or not to show the report for each experiment (default is True).
    save_results : bool, optional
        Whether or not to save the results of each experiment (default is True).
    """

    recombination_types = ['crossover', 'average', 'random', 'range', 'none']

    for type in recombination_types:
        print(f'Starting {type} experiment...')

        settings['RecombinationType'] = type
        generations = settings['Generations']

        results = recursive_artificial_selection(settings, generations)

        if show_report:
            report(type, results)

        if save_results:
            save_results(type, results)

        print(f'Finished {type} experiment.')
