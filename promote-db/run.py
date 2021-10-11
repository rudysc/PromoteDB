import logging
import logging.config
import os
from lib.readFiles import getFiles
from lib.readConfig import readConfig
from lib.promoteUtility import connectionManagerIsConfigured

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.debug('Running main')

    # TODO: implements as parameters
    logger.debug('Parameters: ')
    projectFolderPath = '' # add me
    configFilePath = './PromoteDB/promote-db/config.conf'
    configDbConnectionString = ''

    # reading config
    config = readConfig(configDbConnectionString,configFilePath)
    dbLogConfigured = config.dbLogConfigured
    buildFolder = config.buildFolder
    connectionManagerParser = config.connectionManagerParser
    errorStack = config.errorStack
    configuredConnectionManagers = config.configuredConnectionManagers

    logger.debug('Config values:\n dbLogConfigured: {} \n buildFolder: {} \n connectionManagerParser: {} \n errorStack: {}'.format(dbLogConfigured,buildFolder,connectionManagerParser,errorStack))
    logger.debug(configuredConnectionManagers)

    executionInitilized = False

    # processing files
    for file in getFiles(projectFolderPath, buildFolder, connectionManagerParser, errorStack):
        logger.info('Processing file "{}", with connection manager "{}"'.format(file['fullFileName'], file['connectionManager']))
        
        if dbLogConfigured and not executionInitilized:
            # TODO: initiolize execution
            # executionId, executionDate = createExecution()
            print('Init execution log. Returning executionId, executionDate')
         
        # Check if Connection manager is configured
        if connectionManagerIsConfigured(file['connectionManager'].lower(), configuredConnectionManagers):
            logger.debug('Connection manager "{}" exist in Config'.format(file['connectionManager']))
        else:
            logger.error('Connection manager "{}" not defined in Config.'.format(file['connectionManager']))
            raise Exception('Connection manager "{}" not defined in Config.'.format(file['connectionManager']))

        # TODO: execute file

    