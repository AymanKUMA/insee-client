"""basic configurations for the project.

The INSEE_API_KEY and INPI_API_KEY are global variables used in the Project.
They enable you to access the legal data API.
To use the API, you need to register for API keys at https://api.insee.fr/
and https://api.inpi.fr/ and then set the API KEYS variables in utils.py to your
API key.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# setting up the logger
logging.getLogger(__name__)


def get_env_file_path():
    """Load the path to the default.env file from the package directory."""
    package_dir = Path(__file__)# Directory where this default env file is located
    default_env_path = package_dir / "default.env"
    
    if not default_env_path.exists():
        raise FileNotFoundError(f"default.env file not found at: {default_env_path}")
    
    return str(default_env_path)

DEFAULT_ENV_PATH = get_env_file_path()

load_dotenv(dotenv_path=DEFAULT_ENV_PATH)
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH")
if ENV_FILE_PATH is None:
    msg = "ENV_FILE_PATH is not set in the environment variables."
    raise ValueError(msg)

load_dotenv(ENV_FILE_PATH)

DATA_DIR = os.environ.get("DATA_DIR")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
INSEE_DATA_URL = os.environ.get("INSEE_DATA_URL")

if DATA_DIR is None:
    msg = "DATA_DIR is not set in the environment variables."
    raise ValueError(msg)
if CONSUMER_KEY is None:
    msg = "CONSUMER_KEY is not set in the environment variables."
    raise ValueError(msg)
if CONSUMER_SECRET is None:
    msg = "CONSUMER_SECRET is not set in the environment variables."
    raise ValueError(msg)
if INSEE_DATA_URL is None:
    msg = "INSEE_DATA_URL is not set in the environment variables."
    raise ValueError(msg)

# Set up the response codes
RESPONSE_CODES = {
    # Success
    "OK": 200,
    "CREATED": 201,
    "ACCEPTED": 202,
    "NON_AUTHORITATIVE_INFORMATION": 203,
    "NO_CONTENT": 204,
    "RESET_CONTENT": 205,
    "PARTIAL_CONTENT": 206,
    "MULTI_STATUS": 207,
    "ALREADY_REPORTED": 208,
    "IM_USED": 226,
    # Redirection
    "MULTIPLE_CHOICES": 300,
    "MOVED_PERMANENTLY": 301,
    "FOUND": 302,
    "SEE_OTHER": 303,
    "NOT_MODIFIED": 304,
    "USE_PROXY": 305,
    "TEMPORARY_REDIRECT": 307,
    "PERMANENT_REDIRECT": 308,
    # Client error
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "PAYMENT_REQUIRED": 402,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "METHOD_NOT_ALLOWED": 405,
    "NOT_ACCEPTABLE": 406,
    "PROXY_AUTHENTICATION_REQUIRED": 407,
    "REQUEST_TIMEOUT": 408,
    "CONFLICT": 409,
    "GONE": 410,
    "LENGTH_REQUIRED": 411,
    "PRECONDITION_FAILED": 412,
    "PAYLOAD_TOO_LARGE": 413,
    "URI_TOO_LONG": 414,
    "UNSUPPORTED_MEDIA_TYPE": 415,
    "RANGE_NOT_SATISFIABLE": 416,
    "EXPECTATION_FAILED": 417,
    "IM_A_TEAPOT": 418,
    "MISDIRECTED_REQUEST": 421,
    "UNPROCESSABLE_ENTITY": 422,
    "LOCKED": 423,
    "FAILED_DEPENDENCY": 424,
    "UPGRADE_REQUIRED": 426,
    "PRECONDITION_REQUIRED": 428,
    "TOO_MANY_REQUESTS": 429,
    "REQUEST_HEADER_FIELDS_TOO_LARGE": 431,
    "UNAVAILABLE_FOR_LEGAL_REASONS": 451,
    # Server error
    "INTERNAL_SERVER_ERROR": 500,
    "NOT_IMPLEMENTED": 501,
    "BAD_GATEWAY": 502,
    "SERVICE_UNAVAILABLE": 503,
    "GATEWAY_TIMEOUT": 504,
    "HTTP_VERSION_NOT_SUPPORTED": 505,
    "VARIANT_ALSO_NEGOTIATES": 506,
    "INSUFFICIENT_STORAGE": 507,
    "LOOP_DETECTED": 508,
    "NOT_EXTENDED": 510,
    "NETWORK_AUTHENTICATION_REQUIRED": 511,
}
