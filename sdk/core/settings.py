""" 
Settings
--------
This module contains the settings class for the SDK.
"""

from typing import Callable, Dict, Union
from pydantic import BaseModel


class Setting(BaseModel):
    function: Union[Callable, str]
    args: Union[Dict, str, None]

class Settings(BaseModel):
    pass

    @classmethod
    def from_dict(cls, settings: Dict) -> 'Settings':
        """ Create a settings object from a dictionary """
        pass