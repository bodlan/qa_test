"""
Basic logging, centralized so sinks/other logging necessities can be customized centrally
"""
import logging
from libraries.config.config import CONFIG

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler(CONFIG.LOG_FILE))
logger.info("Logging instantiated")
logger.propagate = False
