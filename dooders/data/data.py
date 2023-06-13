import json

from dooders.data.dooder_dataframe import get_dooder_df
from dooders.data.gene_embedding_dataframe import get_gene_embedding_df
from dooders.data.inference_record_dataframe import get_inference_record_df


class ExperimentData:

    def __init__(self, name):
        self.json_data = self.load_data(name)
        self.embedding_df = get_gene_embedding_df(self.json_data)
        self.dooder_df = get_dooder_df(self.json_data)
        self.inference_df = get_inference_record_df(self.json_data)

    def load_data(self, name):
        file_path = f'experiments/{name}/experiment_results.json'

        with open(file_path, "r") as f:
            json_data = json.load(f)

        return json_data

    def transforms(self):
        pass
