import pandas as pd
from IPython.display import Markdown, display

from dooders.charts.accuracy import accuracy_range_by_cycle
from dooders.charts.boxplot import starting_success_probability as boxplot
from dooders.charts.gene_embedding import gene_embedding
from dooders.charts.histogram import death_age_by_cycle
from dooders.charts.histogram import starting_success_probability as histogram
from dooders.data.data import ExperimentData

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


BASE_REPORT = ['dooder_df_component',
               'embedding_df_component',
               'inference_df_component',
               'histogram_component',
               'gene_embedding_component',
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
        display(death_age_by_cycle(self.dooder_df))

    def gene_embedding_component(self):
        display(gene_embedding(self.dooder_df, color_by='age'))

    def probability_histogram_component(self):
        display(histogram(self.dooder_df))

    def probability_box_component(self):
        display(boxplot(self.dooder_df))

    def accuracy_range_component(self):
        display(accuracy_range_by_cycle(self.inference_df))

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
