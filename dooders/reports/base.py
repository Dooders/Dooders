from dooders.data.data import ExperimentData


BASE_REPORT = ['histogram_component', 
               'probability_histogram_component', 
               'probability_box_component', 
               'accuracy_range_component', 
               'dooder_df_component', 
               'embedding_df_component', 
               'inference_df_component'
               ]

class BaseReport:
    
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name
        self.data = ExperimentData(experiment_name)
        self.embedding_df = self.data.embedding_df
        self.dooder_df = self.data.dooder_df
        self.inference_df = self.data.inference_df
        
    def render(self):
        pass
    
    def compile_report(self):
        pass
    
    
death_age_by_cycle(dooder_df)
gene_embedding(dooder_df, color_by='age')
starting_success_probability(dooder_df)


def histogram_component():
    pass

def probability_histogram_component():
    pass

def probability_box_component():
    pass

def accuracy_range_component():
    pass

def dooder_df_component():
    pass

def embedding_df_component():
    pass

def inference_df_component():
    pass