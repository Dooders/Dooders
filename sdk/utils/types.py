from pydantic import BaseModel
from typing import Callable, Dict, Union


UniqueID = str

class Setting(BaseModel):
    function: Union[Callable, str]
    args: Union[Dict, str, None]
    
class Variable(BaseModel):
    name: str
    type: str
    description: Union[str, None]
    default: Setting
    # dependency: Union[str, None]