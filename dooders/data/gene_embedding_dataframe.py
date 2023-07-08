import pandas as pd


def get_gene_embedding_df(experiment_results: dict) -> pd.DataFrame:
    """ 
    Returns a dataframe of all dooders in the experiment results.

    Parameters
    ----------
    experiment_results : dict
        The experiment results dictionary.

    Returns
    -------
    gene_embedding_df : pd.DataFrame
        A dataframe of all dooders in the experiment results.
    """

    gene_embedding_records = []

    for data in experiment_results.values():
        arena_data = data['state']['arena']
        for dooder in arena_data.values():
            for cycle, record in dooder['encoded_weights'].items():
                temp = {
                    'id': dooder['id'],
                    'cycle': cycle,
                    'X': record[0],
                    'Y': record[1],
                    'Z': record[2]
                }
                gene_embedding_records.append(temp)

    columns = list(gene_embedding_records[0].keys())
    gene_embedding_df = pd.DataFrame(gene_embedding_records, columns=columns)

    return gene_embedding_df
