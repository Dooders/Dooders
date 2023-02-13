from sdk.core.core import Core


class Surface(Core):
    
    @classmethod
    def build(cls, settings) -> object:
        
        surface = cls.get_component('sdk.surfaces', settings['name'])
        
        return surface(settings)