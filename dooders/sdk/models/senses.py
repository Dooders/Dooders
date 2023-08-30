import numpy as np


class Senses:
    """ 
    Senses Model
    ------------
    This module contains the models that allow dooders
    to sense the environment.

    Sense types are for the following:
    - energy detection
    - dooder detection
    - hazard detection

    Methods
    -------
    gather(dooder: 'Dooder') -> list
        Gather the sensory array from the dooder's perception
    """
    SENSE_TYPES = {
        'energy_detection': 'Energy',
        # 'dooder_detection': 'Dooder',
        # hazard_detection: 'Hazard',
    }

    @classmethod
    def gather(cls, dooder) -> list:
        """ 
        Gather the sensory array from the dooder's perception

        Parameters
        ----------
        dooder : Dooder
            The dooder that is gathering the sensory array

        Returns
        -------
        list
            The sensory array from the dooder's perception
        """
        sensory_array = list()
        for model_name in cls.SENSE_TYPES:
            object_name = cls.SENSE_TYPES[model_name]
            perception_array = dooder.perception.array(object_name)

            result = dooder.think(
                model_name, perception_array, perception_array)

            sensory_array.append(result)

        combined_array = np.concatenate(
            [arr.squeeze() for arr in sensory_array])

        return np.array([combined_array], dtype='float32')
