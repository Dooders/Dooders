import pandas as pd


def get_inference_record_df(experiment_results: dict) -> pd.DataFrame:
    """ 
    Returns a dataframe of all dooders in the experiment results.

    Parameters
    ----------
    experiment_results : dict
        The experiment results dictionary.

    Returns
    -------
    inference_record_df : pd.DataFrame
        A dataframe of all dooders in the experiment results.
    """
    inference_records = []

    for simulation_key in experiment_results:
        arena_dict = experiment_results.get(simulation_key)['state']['arena']

        for key in arena_dict:
            inference_record = arena_dict.get(key)['inference_record']

            record_list = []
            for record in inference_record:
                single_record = inference_record.get(record)
                single_record['cycle'] = int(record)
                single_record['dooder'] = key
                inference_records.append(single_record)

    inference_df = pd.DataFrame(inference_records)

    return inference_df
