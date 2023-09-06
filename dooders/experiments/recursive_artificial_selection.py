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

# TODO: Experiment logging for information like number of fit dooders, time taken, etc.

import time
from typing import Dict, List

from dooders.data.experiment_results import calculate_accuracies
from dooders.data.inference_record_dataframe import get_inference_record_df
from dooders.experiment import Experiment
from dooders.experiments.base import save_experiment
from dooders.reports.recursive_artificial_selection import report
from dooders.sdk.modules.recombination import RECOMBINATION_TYPES
from dooders.sdk.modules.selection import get_embeddings, recombine_genes

DEFAULT_SETTINGS = {
    'MaxCycles': 100,
    'SimulationCount': 2000,
    'GenePool': 'retain',
    'Generations': 50,
}


def get_accuracies(results: Dict[str, List]) -> List[float]:

    inference_df = get_inference_record_df(results)
    accuracies = calculate_accuracies(inference_df)

    return [accuracy for accuracy in accuracies.values()]


def experiment_results(experiment):
    return {
        'fit_count': len(experiment.gene_pool),
        'average_accuracy': sum(get_accuracies(experiment.experiment_results)) / len(experiment.experiment_results),
        'elapsed_time': experiment.elapsed_time,
    }


def recursive_artificial_selection(settings: Dict[str, str] = DEFAULT_SETTINGS,
                                   experiment_name: str = 'recursive_artificial_selection',
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
            for dooder in experiment.simulation.arena.dooders():

                new_genes = recombine_genes(
                    gene_pool, recombination_type=settings['RecombinationType'])

                dooder.internal_models.inherit_weights(new_genes)

    for i in range(generations):
        experiment = Experiment(experiment_name, settings)
        experiment.batch_simulate(settings['SimulationCount'],
                                  i+1,
                                  custom_logic=inherit_weights)
        gene_pool = experiment.gene_pool.copy()

        experiment_results['accuracies'].append(
            get_accuracies(experiment.experiment_results))
        experiment_results['fit_dooder_counts'].append(len(gene_pool))
        experiment_results['generation_embeddings'].append(
            get_embeddings(gene_pool))

    return experiment_results


def run_experiment(experiment_name: str = 'recursive_artificial_selection',
                   settings: Dict[str, str] = DEFAULT_SETTINGS,
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

    recombination_types = list(RECOMBINATION_TYPES.keys())

    if save_experiment:
        save_experiment('settings', settings, experiment_name)

    for type in recombination_types:
        print(f'Starting {type} experiment at {time.ctime()}\n')

        settings['RecombinationType'] = type
        generations = settings['Generations']

        results = recursive_artificial_selection(
            settings, experiment_name, generations)

        if show_report:
            report(type, results)

        if save_results:
            save_experiment(type, results, experiment_name)

        print(f'Finished {type} experiment. Ended at {time.ctime()}\n')
