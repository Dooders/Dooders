from functools import reduce

import pandas as pd


def total_accuracy(inference_record: dict) -> float:
    """ 
    Calculates the total accuracy of the inference record.

    Parameters
    ----------
    inference_record : dict
        The inference record to calculate the total accuracy for.

    Returns
    -------
    percentage : float
        The total accuracy of the inference record.
    total_count : int
        The total number of inferences in the inference record.
    """
    results = [a['accurate']
               for a in inference_record.values() if a['accurate'] is not None]
    true_count = sum(results)
    total_count = len(results)
    percentage = (true_count / total_count) * 100 if total_count > 0 else 0.0

    return percentage, total_count


def running_accuracy(inference_record: dict) -> list:
    """ 
    Calculates the running accuracy of the inference record.

    Parameters
    ----------
    inference_record : dict
        The inference record to calculate the running accuracy for.

    Returns
    -------
    accuracies : list
        A list of the running accuracies.
    """
    count_true = 0
    total = 0
    accuracies = []

    for value in inference_record.values():
        total += 1
        if value['accurate']:
            count_true += 1
        accuracies.append(count_true / total)

    return accuracies


# def n_running_accuracy(inference_df: pd.DataFrame, n: int = 5) -> list:
#     """
#     """
#     count_true = 0
#     total = 0
#     accuracies = []

#     for i, (_, value) in enumerate(inference_df):
#         total += 1
#         if value['accurate']:
#             count_true += 1
#         if i >= n:
#             oldest_item = record_items[i - n]
#             if oldest_item[1]['accurate']:
#                 count_true -= 1
#             total -= 1
#         accuracies.append(count_true / total)

#     return accuracies


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
