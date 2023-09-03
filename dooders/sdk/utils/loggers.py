import datetime
from functools import wraps

import structlog

log_entries = []


def capture_to_list(logger, log_method, event_dict):
    log_entries.append(event_dict)
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
