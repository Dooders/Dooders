import pandas as pd
from IPython.display import Markdown, display

from dooders.data.data import ExperimentData

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


BASE_REPORT = ['dooder_df_component', 
               'embedding_df_component', 
               'inference_df_component',
               'histogram_component', 
               'probability_histogram_component', 
               'probability_box_component', 
               'accuracy_range_component'
               ]

class BaseReport:
    
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name
        self.data = ExperimentData(experiment_name)
        self.embedding_df = self.data.embedding_df
        self.dooder_df = self.data.dooder_df
        self.inference_df = self.data.inference_df
        self.compile_report()
        
    def render(self):
        pass
    
    def compile_report(self):
        self.report = {}
        for component in BASE_REPORT:
            self.report[component] = getattr(
                self, component)()

    def histogram_component(self):
        pass

    def probability_histogram_component(self):
        pass

    def probability_box_component(self):
        pass

    def accuracy_range_component(self):
        pass

    def dooder_df_component(self):
        display(Markdown('## Dooder Dataframe'))
        display(self.dooder_df.head())
        display(self.dooder_df.describe())

    def embedding_df_component(self):
        display(Markdown('## Embedding Dataframe'))
        display(self.embedding_df.head())

    def inference_df_component(self):
        display(Markdown('## Inference Dataframe'))
        display(self.inference_df.head())