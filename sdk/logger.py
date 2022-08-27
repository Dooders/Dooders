import functools
import logging
import os


class CustomFormatter(logging.Formatter):
    """ Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """

    def format(self, record):
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(CustomFormatter, self).format(record)


def get_logger():
    """ Creates a Log File and returns Logger object """

    # Build Log file directory, based on the OS and supplied input
    log_dir = 'logs/'
    log_file_name = 'log'

    # Create Log file directory if not exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Build Log File Full Path
    logPath = log_file_name if os.path.exists(log_file_name) else os.path.join(
        log_dir, (str(log_file_name) + '.log'))

    # Create logger object and set the format for logging and other attributes
    logger = logging.Logger(log_file_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(logPath, 'a+')
    """ Set the formatter of 'CustomFormatter' type as we need to log base function name and base file name """
    handler.setFormatter(CustomFormatter(
        "{'timestamp': '%(asctime)s', %(message)s},"))
    logger.addHandler(handler)

    # Return logger object
    return logger


def log(self, granularity, scope):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):

            message = function(*args, **kwargs)

            if granularity <= self.params.granularity:
                cycle_number = self.simulation.time.time
                unique_id = self.unique_id
                experiment_id = self.experiment_id
                logger_obj = get_logger()
                prefix = f'{experiment_id} - {function.__name__} - {scope} - {cycle_number} - '
                final_message = prefix + message
                logger_obj.info(final_message)

        return wrapper

    return decorator
