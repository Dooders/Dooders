from dataclasses import dataclass


@dataclass
class ValueGenerator:
    distribution_type: str
    min_value: int
    max_value: int
    
class Config:
    """ 
    Class to hold the settings for the simulation
    
    Attributes
    ----------
    settings : dict
        Dictionary of settings
        
    Methods
    -------
    update(new_settings: dict) -> None
        Update the settings with new settings
    get(setting_name: str) -> object
        Get a setting from the settings
    """
    def __init__(self) -> None:
        self.settings: dict = {
            'MaxCycles': 100,
            'SeedCount': 1,
            'EnergyPerCycle': ValueGenerator('uniform', 5, 10),
            'MaxTotalEnergy': 10,
            'GridHeight': 5,
            'GridWidth': 5,
            'EnergyLifespan': ValueGenerator('uniform', 2, 5),
        }

    def update(self, new_settings: dict) -> None:
        """ 
        Update the settings with new settings
        
        Parameters
        ----------
        new_settings : dict
            New settings to update the current settings with
        """
        for key, value in new_settings.items():
            if key in self.settings:
                self.settings[key] = value
            else:
                raise KeyError(f"{key} does not exist in the settings")

    def get(self, setting_name: str) -> object:
        """ 
        Get a setting from the settings
        
        Parameters
        ----------
        setting_name : str
            Name of the setting to get
        """
        try:
            return self.settings[setting_name]
        except KeyError:
            raise KeyError(f"{setting_name} does not exist in the settings")

