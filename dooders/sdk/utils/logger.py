import os
import logging
from logging.handlers import QueueHandler, QueueListener
import queue

def get_logger():
    """ Creates a Log File and returns Logger object """

    log_dir = 'logs/'
    log_file_name = 'log'

    try:
        os.remove('logs/log.json')
    except OSError:
        pass

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logPath = log_file_name if os.path.exists(log_file_name) else os.path.join(
        log_dir, (str(log_file_name) + '.json'))

    logger = logging.Logger(log_file_name)
    logger.setLevel(logging.INFO)  # Change the logging level to INFO
    handler = logging.FileHandler(logPath, 'a+')  # Using a standard FileHandler
    formatter = logging.Formatter("{'Timestamp': '%(asctime)s', %(message)s},")
    handler.setFormatter(formatter)

    log_queue = queue.Queue(-1)  # Create an asynchronous queue
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    # Start a listener for the queue
    queue_listener = QueueListener(log_queue, handler)
    queue_listener.start()

    return logger, queue_listener




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
