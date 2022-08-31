from abc import ABC, abstractmethod


class BaseComponent(ABC):
    
    _objects = {}
    component = {}
    
    
    def get_object_types(self) -> List[BaseObject]:
        pass
    
    def get_objects(self, object_type=BaseObject) -> List[BaseObject]:
        pass
    
    def get_object(self, object_id) -> BaseObject:
        pass
