"""logger module."""
import logging
import logging.config
from pathlib import Path
from .config import default_env_path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=default_env_path)
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH")
if ENV_FILE_PATH is None:
    msg = "ENV_FILE_PATH is not set in the environment variables."
    raise ValueError(msg)

load_dotenv(ENV_FILE_PATH)

# Retrieve the log directory from environment variables
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Ensure the log directory exists
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Set up logging
LOG_FILE = os.path.join(LOG_DIR, "insee_client.log")

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
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': LOG_FILE,
            'level': 'DEBUG',
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

# No need to define a global logger here


# Define a global logger
logger = logging.getLogger(__name__)
