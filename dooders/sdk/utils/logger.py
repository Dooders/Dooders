import logging
import os


def get_logger():
    """ Creates a Log File and returns Logger object """

    # Build Log file directory, based on the OS and supplied input
    log_dir = 'logs/'
    log_file_name = 'log'
    
    try:
        os.remove('logs/log.json')
    except OSError:
        pass

    # Create Log file directory if not exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Build Log File Full Path
    logPath = log_file_name if os.path.exists(log_file_name) else os.path.join(
        log_dir, (str(log_file_name) + '.json'))

    # Create logger object and set the format for logging and other attributes
    logger = logging.Logger(log_file_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(logPath, 'a+')
    formatter = logging.Formatter("{'Timestamp': '%(asctime)s', %(message)s},")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

######################################
#! May use this decorator in the future
#def log(self, granularity, scope):
#    def decorator(function):
 #       @functools.wraps(function)
 #       def wrapper(*args, **kwargs):
#
 #           message = function(*args, **kwargs)

 #           if granularity <= self.params.granularity:
 #               cycle_number = self.simulation.time.time
  #              id = self.id
   #             experiment_id = self.experiment_id
#                logger_obj = get_logger()
#                prefix = f'{experiment_id} - {function.__name__} - {scope} - {cycle_number} - '
#                final_message = prefix + message
 #               logger_obj.info(final_message)
#
 #       return wrapper
#
 #   return decorator
