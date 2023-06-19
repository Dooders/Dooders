# Base report class

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
        
    def render(self):
        pass
    
    def compile_report(self):
        pass
        


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