import logging
import logging.config

logger = logging.getLogger(__name__)

logger.debug('promoteUtility.py loaded')


# TODO: Description
# Parameters:
# Usage:
def connectionManagerIsConfigured(connectionManagerToCheck, connectionMananagerDict):
    logger.debug('Checking connection manager "{}"'.format(connectionManagerToCheck))
    if connectionManagerToCheck in connectionMananagerDict:
        return 1
    return 0

# TODO: Description
# Parameters:
# Usage:
def translateArguments(args[]):
    logger.debug('Checking connection manager "{}"'.format(connectionManagerToCheck))
    if connectionManagerToCheck in connectionMananagerDict:
        return 1
    return 0