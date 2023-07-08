import statistics

import pandas as pd


def get_dooder_df(experiment_results: dict) -> pd.DataFrame:
    """ 
    Returns a dataframe of all dooders in the experiment results.

    Parameters
    ----------
    experiment_results : dict
        The experiment results dictionary.

    Returns
    -------
    dooder_df : pd.DataFrame
        A dataframe of all dooders in the experiment results.
    """

    dooder_details = []

    for result in experiment_results.values():
        arena_data = result.get('state', {}).get('arena', {})
        dooder_details.extend(arena_data.values())

    columns = list(dooder_details[0].keys())
    dooder_df = pd.DataFrame(dooder_details, columns=columns)

    dooder_df = process_dooder_df(dooder_df)

    return dooder_df


def process_dooder_df(dooder_df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Processes the dooder DataFrame.

    Parameters
    ----------
    dooder_df : pd.DataFrame
        The dooder DataFrame.

    Returns
    -------
    processed_df : pd.DataFrame
        The processed dooder DataFrame.
    """

    result = (
        dooder_df
        .pipe(experiment_result)
        .pipe(encoding_columns)
        .pipe(calculate_metrics)
    )

    return result


def experiment_result(df: pd.DataFrame, lower_threshold: int = 5, upper_threshold: int = 99) -> pd.DataFrame:
    """ 
    Returns a dataframe of all dooders in the experiment results.

    Parameters
    ----------
    df : pd.DataFrame
        The dooder DataFrame.
    lower_threshold : int
        The lower threshold for the age category.
    upper_threshold : int
        The upper threshold for the age category.

    Returns
    -------
    df : pd.DataFrame
        The dooder DataFrame with the age category column added.
    """

    # Categorize age
    experiment_result = []
    for age in df['age']:
        if age <= lower_threshold:
            experiment_result.append('FailedEarly')
        elif age > upper_threshold:
            experiment_result.append('Passed')
        else:
            experiment_result.append('Failed')

    df['experiment_result'] = experiment_result

    return df


def encoding_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Returns a dataframe of all dooders in the experiment results.

    Parameters
    ----------
    df : pd.DataFrame
        The dooder DataFrame.

    Returns
    -------
    df : pd.DataFrame
        The dooder DataFrame with the encoding columns added.
    """
    # Extract specific elements from 'encoded_weights' column
    df['first_encoding'] = df['encoded_weights'].apply(
        lambda x: x['0'])
    df['last_encoding'] = df.apply(
        lambda row: row['encoded_weights'][str(row['age'] - 1)], axis=1)

    return df


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Returns a dataframe of all dooders in the experiment results.

    Parameters
    ----------
    df : pd.DataFrame
        The dooder DataFrame.

    Returns
    -------
    df : pd.DataFrame
        The dooder DataFrame with the metrics added.
    """

    opportunity_variation = []
    average_opportunities = []
    average_starting_opportunities = []
    average_ending_opportunities = []

    for d in df.itertuples():
        opportunities = [len(x['reality'])
                         for x in d.inference_record.values()]
        avg_opportunity = sum(opportunities) / len(opportunities)
        avg_first_opportunity = sum(opportunities[:1]) / len(opportunities[:1])
        avg_last_opportunity = sum(
            opportunities[-2:]) / len(opportunities[-2:])
        opportunity_variation.append(statistics.variance(opportunities))
        average_opportunities.append(avg_opportunity)
        average_starting_opportunities.append(avg_first_opportunity)
        average_ending_opportunities.append(avg_last_opportunity)

    df['average_opportunity'] = average_opportunities
    df['opportunity_variation'] = opportunity_variation
    df['avg_first_opportunity'] = average_starting_opportunities
    df['avg_last_opportunity'] = average_ending_opportunities

    return df
