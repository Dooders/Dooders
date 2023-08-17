import json
import os
from typing import Dict, List


def save_experiment(type: str, results: Dict[str, List], experiment_name: str) -> None:
    """ 
    Saves the results of the experiment to a JSON file.

    Parameters
    ----------
    type : str
        The type of experiment (the recombination type).
    results : dict
        The results of the experiment.
    experiment_name : str
        The name of the experiment. 
        Directory will be created in the results folder.
    """
    if not os.path.exists(f'results/{experiment_name}'):
        os.makedirs(f'results/{experiment_name}')

    with open(f'results/{experiment_name}/{type}.json', 'w') as f:
        json.dump(results, f)