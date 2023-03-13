import json
import pandas as pd


class Investigate:
    
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.state = self.load_state("dooders/experiments/" + experiment_name, "state.json")
        self.log = self.load_log("dooders/experiments/" + experiment_name + "/log.json")
        self.data = self.state['information']

    def load_log(self, file_path):
        with open(file_path, 'r') as f:
            lines = [eval(line.strip())[0] for line in f]
            
        df = pd.DataFrame(lines)
        
        return df
    
    def load_state(self, folder_path, file_name):
        # Construct the full path to the JSON file
        file_path = folder_path + "/" + file_name
        
        # Open the file and read its contents
        with open(file_path, "r") as f:
            json_data = json.load(f)
        
        # Return the contents as a dictionary
        return json_data
