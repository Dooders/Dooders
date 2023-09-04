import datetime
from functools import wraps

import structlog

log_entries = {}


def capture_to_list(logger, log_method, event_dict) -> dict:
    """ 
    Capture log entries to a list

    Parameters
    ----------
    logger : structlog.BoundLogger
        The logger instance
    log_method : str
        The log method used
    event_dict : dict
        The event dictionary

    Returns
    -------
    dict
        The event dictionary
    """

    # Get the simulation_id from event_dict
    simulation_id = event_dict.pop('simulation_id')

    # Create an empty list if simulation_id doesn't exist in log_entries
    if simulation_id not in log_entries:
        log_entries[simulation_id] = []

    # Append the event_dict to the list corresponding to simulation_id
    log_entries[simulation_id].append(event_dict)

    return event_dict


# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %I:%M:%S", utc=False),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        capture_to_list,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()


def log_performance():
    """ 
    Decorator to log performance of a model

    TODO: Add running accuracy from internal model attribute
    """
    def decorator(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            start_time = datetime.datetime.now()
            result = func(instance, *args, **kwargs)
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time

            data = {
                'simulation_id': instance.simulation.simulation_id,
                'dooder_id': instance.id,
                'cycle_number': instance.simulation.cycle_number,
                'model_name': args[0],
                'input_array': args[1].tolist(),
                'output_array': result.tolist(),
                'reality_array': args[2].tolist(),
                'elapsed_time': elapsed_time.total_seconds(),
                'accurate': instance.check_accuracy(result, args[2])
            }

            logger.info("Thinking", **data)
            return result
        return wrapper
    return decorator


# # Save log entries as JSON
# import json

# with open("log_entries.json", "w") as json_file:
#     json.dump(log_entries, json_file, indent=4)
