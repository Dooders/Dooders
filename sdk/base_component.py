from abc import ABC, abstractmethod
from typing import List
from base_object import BaseObject

#! Mess with this at some point
class BaseComponent(ABC):
    
    objects = {}
    components = {}
    
    @abstractmethod
    def get_object_types(self) -> List[BaseObject]:
        pass
    
    @abstractmethod
    def get_objects(self, object_type=BaseObject) -> List[BaseObject]:
        pass
    
    @abstractmethod
    def get_object(self, object_id) -> BaseObject:
        pass
