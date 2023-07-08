from collections import namedtuple
from functools import reduce
from typing import List

import numpy as np
import pandas as pd


def calculate_accuracies(inference_df: pd.DataFrame) -> dict:
    """ 
    Calculates the accuracies for each Dooder in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the accuracies for.

    Returns
    -------
    accuracy_results : dict
        A dictionary of the accuracies for each Dooder.
    """
    accuracy_results = {}

    grouped_df = inference_df.groupby('dooder')

    for dooder, group in grouped_df:
        results = [a for a in group['accurate'] if a is not None]
        true_count = sum(results)
        total_count = len(results)
        percentage = (true_count / total_count) * \
            100 if total_count > 0 else 0.0
        accuracy_results[dooder] = round(percentage, 2)

    return accuracy_results


def probability_from_counts(count_list: list) -> float:
    """ 
    Calculates the probability of a given list of reality counts by the comparison
    of the inverse probabilities of each count.

    This returns the probability that given 5 cycles, the probability that at least
    one cycle the Dooder will successfully choose an energy object.

    Parameters
    ----------
    count_list : list
        A list of counts for each class.

    Returns
    -------
    probability : float
        The probability that at least one cycle the Dooder will successfully choose
        an energy object.
    """
    inverse_probabilities = [(9-x)/9 for x in count_list]
    probability = 1 - reduce(lambda x, y: x * y, inverse_probabilities)

    return probability


def get_reality_counts(inference_df: pd.DataFrame) -> dict:
    """ 
    Calculates the reality counts for each Dooder in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the reality counts for.

    Returns
    -------
    reality_counts : dict
        A dictionary of the reality counts for each Dooder.
    """
    reality_counts = {}

    for dooder, group in inference_df.groupby('dooder'):
        filtered_df = group.head(5)
        count = filtered_df['reality'].apply(len).tolist()
        reality_counts[dooder] = count

    return reality_counts


def near_hunger(inference_df: pd.DataFrame) -> dict:
    """ 
    Calculates the number of times each Dooder was near hunger in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the number of times each Dooder was near hunger for.
    """

    near_hunger_counts = inference_df[inference_df['hunger'] == 4].groupby(
        'dooder').size().to_dict()

    return near_hunger_counts


def probabilities(inference_df: pd.DataFrame) -> dict:
    """ 
    Calculates the probabilities for each Dooder in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the probabilities for.

    Returns
    -------
    probabilities : dict
        A dictionary of the probabilities for each Dooder.
    """

    reality_counts = get_reality_counts(inference_df)

    probabilities = {}

    for dooder, count in reality_counts.items():
        result = probability_from_counts(count)
        probabilities[dooder] = result

    return probabilities


def calculate_accuracy_from_list(value_list: list) -> float:
    """ 
    Calculates the accuracy from a list of values.

    Parameters
    ----------
    value_list : list
        A list of values to calculate the accuracy from.

    Returns
    -------
    percentage : float
        The accuracy of the list of values.
    """
    results = [a for a in value_list if a is not None]
    true_count = sum(results)
    total_count = len(results)
    percentage = (true_count / total_count) * 100 if total_count > 0 else 0.0

    return percentage


def accuracy_over_cycles(inference_results: list) -> list:
    """ 
    Calculates the accuracy over cycles from a list of inference results.

    Parameters
    ----------
    inference_results : list
        A list of inference results to calculate the accuracy over cycles for.

    Returns
    -------
    accuracy_list : list
        A list of the accuracy over cycles.
    """

    accuracy_list = []

    for i in range(len(inference_results)):
        accuracy = calculate_accuracy_from_list(inference_results[:i+1])
        accuracy_list.append(accuracy)

    return accuracy_list


def min_max_avg_per_cycle(inference_df: pd.DataFrame) -> list:
    """
    Calculates the min, max and average accuracy per cycle 
    for each Dooder in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the min, 
        max and average accuracy per cycle for.

    Returns
    -------
    cycle_tuples : list
        A list of tuples containing the min, 
        max and average accuracy per cycle for each Dooder.
    """

    all_results = []

    for dooder, group in inference_df.groupby('dooder'):
        inference_results = group['accurate'].to_list()
        all_results.append(accuracy_over_cycles(inference_results))

    cycle_tuples = []

    for accuracies in zip(*all_results):
        max_value = max(accuracies)
        min_value = min(accuracies)
        avg_value = sum(accuracies)/len(accuracies)
        cycle_tuples.append((max_value, min_value, avg_value))

    return cycle_tuples


# Define a named tuple to store the result
SequenceInfo = namedtuple(
    "SequenceInfo", ["target_value", "value", "length", "start"])


def find_longest_sequence(sequence_list: list, target_value: int) -> SequenceInfo:
    """ 
    Finds the longest sequence of a given target value in a list of values.

    Parameters
    ----------
    sequence_list : list
        A list of values to find the longest sequence of a given target value in.
    target_value : int
        The target value to find the longest sequence of.

    Returns
    -------
    longest_sequence : SequenceInfo
        A named tuple containing the target value, the value of the longest sequence,
        the length of the longest sequence and the start index of the longest sequence.
    """
    if not sequence_list:
        return SequenceInfo(target_value, None, 0, 0)

    longest_sequence = SequenceInfo(target_value, None, 0, 0)
    current_sequence = SequenceInfo(target_value, None, 0, 0)

    for i, value in enumerate(sequence_list):
        if value == current_sequence.value:
            current_sequence = current_sequence._replace(
                length=current_sequence.length + 1)
        else:
            if current_sequence.length > longest_sequence.length:
                longest_sequence = current_sequence

            current_sequence = SequenceInfo(target_value, value, 1, i)

    if current_sequence.length > longest_sequence.length:
        longest_sequence = current_sequence

    return longest_sequence


def decision_analysis(inference_df: pd.DataFrame) -> dict:
    """ 
    Calculates the longest sequence of decisions for each Dooder in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the longest sequence of decisions for.

    Returns
    -------
    decision_counts : dict
        A dictionary of the longest sequence of decisions for each Dooder.
    """

    decision_counts = {}

    for dooder, group in inference_df.groupby('dooder'):
        decisions = [int(x) for x in group['decision']]
        result = find_longest_sequence(decisions, dooder)
        decision_counts[dooder] = result.length

    return decision_counts


def average_embedding_by_age(dooder_df: pd.DataFrame) -> list:
    """ 
    Calculates the average embedding by age for each Dooder in the dooder dataframe.

    Parameters
    ----------
    dooder_df : pd.DataFrame
        The dooder dataframe to calculate the average embedding by age for.

    Returns
    -------
    avg_embedding : list
        A list of the average embedding by age for each Dooder.
    """
    age_dict = {k: [] for k in range(100)}

    for _, dooder in dooder_df.iterrows():
        embeddings = dooder['last_encoding']
        age_dict[dooder['age'] - 1].append(embeddings)

    avg_embedding = []

    for age, embeddings in age_dict.items():
        if embeddings:
            embeddings_avg = np.mean(embeddings, axis=0)
            embeddings_avg_rounded = [round(x, 5) for x in embeddings_avg]
            avg_embedding.append(embeddings_avg_rounded)

    return avg_embedding


def stuck_streak_count(decision_list: List[str]) -> int:
    """ 
    Calculates the stuck streak count for a list of decisions.

    Parameters
    ----------
    decision_list : list
        A list of decisions to calculate the stuck streak count for.

    Returns
    -------
    streak_count : int
        The stuck streak count for the list of decisions.
    """
    streak_count = 1
    last_value = decision_list[-1]

    for decision in reversed(decision_list[:-1]):
        if decision == last_value:
            streak_count += 1
        else:
            break

    return streak_count


def stuck_streak_counts(inference_df: pd.DataFrame) -> dict:
    """ 
    Calculates the stuck streak counts for each Dooder in the inference dataframe.

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe to calculate the stuck streak counts for.

    Returns
    -------
    streak_counts : dict
        A dictionary of the stuck streak counts for each Dooder.
    """
    streak_counts = {}

    for dooder, group in inference_df.groupby('dooder'):
        decisions = [int(x) for x in group['decision']]
        result = stuck_streak_count(decisions)
        streak_counts[dooder] = result

    return streak_counts
