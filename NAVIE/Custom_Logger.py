import logging.handlers
from configparser import ConfigParser

CONFIGURATION_FILE = "settings.conf"
parser = ConfigParser()
parser.read(CONFIGURATION_FILE)
LOG_PATH = parser.get('settings', 'log_path')
PROJECT_NAME = parser.get("settings", "project_name")
LOG_FILE = LOG_PATH + PROJECT_NAME
LOG_LEVEL = parser.get('settings','log_level')

# Define a custom log level "DATA" with a numeric value of 15
DATA_LOG_LEVEL = 15
logging.addLevelName(DATA_LOG_LEVEL, "DATA")

def log_data(self, message, *args, **kwargs):
    if self.isEnabledFor(DATA_LOG_LEVEL):
        self._log(DATA_LOG_LEVEL, message, args, **kwargs)

# Add the custom log level "DATA" and the corresponding log_data method to the Logger class
logging.Logger.data = log_data

logger = logging.getLogger(PROJECT_NAME)
log_handler = logging.FileHandler(LOG_FILE+'.log')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")

log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(LOG_LEVEL)
logger.debug('Logger Initialized')