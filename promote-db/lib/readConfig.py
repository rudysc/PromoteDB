import logging
import logging.config
from configparser import SafeConfigParser
import codecs

logger = logging.getLogger(__name__)

logger.debug('readConfig.py loaded')

# TODO: Description
# Parameters:
# Usage:
class readConfig:
    def __init__(self, configDbConnectionString, configFilePath):
        logger.debug('init readConfig')
        self.dbLogConfigured = False,
        self.buildFolder = '',
        self.connectionManagerParser = '',
        self.errorStack = False,
        self.configuredConnectionManagers = {}
        self._readConfig(configDbConnectionString, configFilePath)

    def _readConfig(self, configDbConnectionString, configFilePath):
        if configDbConnectionString:
            self._readDbConfig(configDbConnectionString)
        else:
            self._readFileConfig(configFilePath)

    def _readDbConfig(self,configDbConnectionString):
        logger.debug('Reading config from database with connection string "{}"'.format(configDbConnectionString))

        # TODO lets extract the stuff
        
        self.dbLogConfigured = False,
        self.buildFolder = '',
        self.connectionManagerParser = '',
        self.errorStack = False,

        self.configuredConnectionManagers = {}

    def _readFileConfig(self,configFilePath):
        logger.debug('Reading config from file: "{}"'.format(configFilePath))

        parser = SafeConfigParser()
        try:
            with codecs.open(configFilePath, 'r', encoding='utf-8') as confFile:
                parser.readfp(confFile)
            
                self.dbLogConfigured = parser.get('main', 'dbLogConfigured')
                self.buildFolder = parser.get('main', 'buildFolder')
                self.connectionManagerParser = parser.get('main', 'connectionManagerParser')
                self.errorStack = parser.get('main', 'errorStack')

                for connectionManagerName, connectionString in parser.items('configuredConnectionManagers'):
                    self.configuredConnectionManagers[connectionManagerName] = connectionString.strip("'")
        except:
            logger.error('Error while reading config file', exc_info=True)
            raise