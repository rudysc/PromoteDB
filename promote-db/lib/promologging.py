# not used just an example ho to use logging through a file

import logging
import sys

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG)

