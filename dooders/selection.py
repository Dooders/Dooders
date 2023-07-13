import glob
import random

import numpy as np

from dooders.sdk.modules.recombination import recombine


def weight_file_list(path: str) -> list:
    """ 
    Returns a list of all the weight files in a directory

    Parameters
    ----------
    path : (str)
        The path to the directory containing the weight files

    Returns
    -------
    files : (list)
        A list of all the weight files in the directory
    """
    files = []

    for file in glob.glob(path + "*"):
        if "Consume" in file:
            files.append(file)

    return files


def random_dooder_weights(files: list) -> tuple:
    """ 
    Returns a random dooder's weights from a list of weight files

    Parameters
    ----------
    files : (list)
        A list of all the weight files in the directory

    Returns
    -------
    dooder_id : (str)
        The id of the dooder whose weights were selected
    weights : (np.ndarray)
        The weights of the dooder whose weights were selected
    """

    random_file = random.choice(files)
    dooder_id = random_file.split('\\')[1].split('_')[0]
    weights = np.load(random_file, allow_pickle=True)

    return dooder_id, weights


def random_parents(path: str) -> tuple:
    """ 
    Returns two random dooders' weights from a directory of weight files

    Parameters
    ----------
    path : (str)
        The path to the directory containing the weight files

    Returns
    -------
    parent_a : (np.ndarray)
        The weights of the first dooder
    parent_b : (np.ndarray)
        The weights of the second dooder
    """
    files = weight_file_list(path)

    parent_a = random_dooder_weights(files)

    parent_b = random_dooder_weights(files)

    if parent_a == parent_b:
        parent_b = random_dooder_weights(files)

    return parent_a, parent_b
