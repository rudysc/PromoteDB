# not used just an example ho to use logging through a conf file

# from lib.promologging import logger
import logging
import logging.config
import os

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logger.debug('A debug message')
    logger.info('An info message')
    logger.warning('Something is not right.')
    logger.error('A Major error has happened.')
    logger.critical('Fatal error. Cannot continue')