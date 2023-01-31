

from typing import Callable, Dict, Union
from pydantic import BaseModel


class Setting(BaseModel):
    type: str
    function: Union[Callable, str]
    args: Union[Dict, str]
    description: Union[str, None]
    dependency: Union[str, None]

class Settings(BaseModel):
    pass