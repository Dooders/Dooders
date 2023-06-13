import json
import pandas as pd

file_path = 'experiments/twenty_thousand_simulations/experiment_results.json'

with open(file_path, "r") as f:
    json_data = json.load(f)
    
    
class ExperimentData:
    pass