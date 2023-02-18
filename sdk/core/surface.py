from sdk.core.core import Core
from sdk.core.settings import Settings
import importlib


class Surface(Core):

    @classmethod
    def build(cls, surface_type) -> object:
        module = f'sdk.surfaces.{surface_type}'
        chosen_surface = getattr(importlib.import_module(module), surface_type.title())
        settings = Settings.get('variables', surface_type)
        #! should clean up code below, or the process of getting settings
        final_settings = {k: v.args['value'] for k, v in settings.items() if v is not None}
        return chosen_surface(final_settings)
