from typing import Callable, Dict, List, Union

from pydantic import BaseModel

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
    
class EmbeddingLayers(BaseModel):
    static: List[float]
    dynamic: List[float]