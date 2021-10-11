import logging
import logging.config
import os
import re

logger = logging.getLogger(__name__)

logger.debug('readFiles.py loaded')

# TODO: Description
# Parameters:
# Usage:
class getFiles:
    def __init__(self, projectFolderPath, buildFolder, connectionManagerParser, errorStack):
        logger.debug('init getFiles')
        self._errorStack = errorStack
        self._files = self._listfiles(projectFolderPath,buildFolder,connectionManagerParser)
        self._indx = -1
        self._maxIndx = len(self._files)-1

    def _listfiles(self, projectFolderPath,buildFolder,connectionManagerParser):
        logger.debug('listing files')
        deploymentFilesPath = projectFolderPath
        fileList = list()
        defaultPattern = '([a-zA-Z]+)'

        if deploymentFilesPath:

            if buildFolder:
                deploymentFilesPath = projectFolderPath + '/' + buildFolder
            
            try:
                files = os.listdir(deploymentFilesPath)
            except:
               logger.error('Error while reading files', exc_info=self._errorStack)
               raise

            for filename in files:
                if filename.endswith(".sql"):
                    if connectionManagerParser:
                        connectionManager =  re.findall(connectionManagerParser, filename)[0] # extracts the first match
                    else: 
                        connectionManager =  re.findall(defaultPattern, filename)[0] # extracts the first word
                    fileList.append({'fullFileName': deploymentFilesPath + '/' + filename, 'connectionManager': connectionManager})

            return fileList

        else:
            logger.error('Project folder not defined.')
            raise Exception('Project folder not defined.')

    def __iter__(self):
        return self

    def __next__(self):
        if self._indx >= self._maxIndx:
            raise StopIteration
        self._indx += 1
        return self._files[self._indx]

        