"""logger module."""
import logging
import logging.config
from pathlib import Path
import os
from dotenv import load_dotenv
from .config import DEFAULT_ENV_PATH

# Load environment variables from default.env file
load_dotenv(dotenv_path=DEFAULT_ENV_PATH)
# Getting .evn file path
ENV_FILE_PATH = os.getenv("PYINSEE_ENV_FILE_PATH")
if ENV_FILE_PATH is None:
    raise ValueError("ENV_FILE_PATH is not set in the environment variables.")

# Load environment variables from .env file
load_dotenv(ENV_FILE_PATH)

# Retrieve the data and log directories from environment variables
DATA_DIR = os.getenv("DATA_DIR", "data") # Set default data directory
LOG_DIR = os.path.join(DATA_DIR, "logs") # Set default log directory
RAW_DIT = os.path.join(DATA_DIR, "raw") # Set default raw directory
PROCESSED_DIR = os.path.join(DATA_DIR, "processed") # Set default processed directory
METADATA_DIR = os.path.join(DATA_DIR, "metadata") # Set default metadata directory

if DATA_DIR is None:
    msg = "DATA_DIR is not set in the environment variables. Please set it in the .env file using the setup_cli script."
    raise ValueError(msg)

# Ensure the log directory exists
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Set up logging
LOG_FILE = os.path.join(LOG_DIR, "insee_client.log")  # Correct path to log file

# Define logging configuration
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s | %(name)s | %(levelname)s : %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': LOG_FILE,
            'level': 'DEBUG',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        }
    },
    'root': {
        'handlers': ['file_handler', 'console'],
        'level': 'DEBUG',
    }
}

# Apply logging configuration
logging.config.dictConfig(logging_config)

# Define a global logger
logger = logging.getLogger(__name__)

