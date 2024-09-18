"""Utility functions for the company_data_collection package."""
from __future__ import annotations

import csv
import datetime as dt
import json
import logging
import re
from pathlib import Path

# Define the directories
BASE_DIR = Path.cwd() / "data"
LOGS_DIR = BASE_DIR / "logs"
METADATA_DIR = BASE_DIR / "metadata"
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

# Define the regex patterns
QUERY_URL_REGEX = r"(?:[^=&]+=[^=&]*&?)*"

# Create directories if they don't exist
for directory in [LOGS_DIR, METADATA_DIR, RAW_DIR, PROCESSED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

def setup_logging() -> None:
    """Set up logging."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)


class QueryBuilder:
    """To build the query string from kwargs."""
    def _validate_key_and_type(self,
                               key: str,
                               value : any,
                               expected_types: dict[str, type | tuple]) -> None:
        """Validate that the key is expected and the value is of the correct type."""
        expected_type = expected_types.get(key)

        # Check if the key is valid
        if expected_type is None:
            msg = f"Unexpected key: {key}"
            raise ValueError(msg)

        # Check type validity (supporting tuple types like (str, int))
        if not isinstance(value, expected_type if isinstance(
                                        expected_type,
                                        tuple,
                                    ) else (expected_type,),
                        ):
            msg = f"Invalid type for {key}: expected {expected_type}, got {type(value)}"
            raise TypeError(msg)

    def _validate_regex(self,
                        key: str,
                        value: str,
                        regex_patterns: dict[str, str] | None) -> None:
        """Validate the value using a regex pattern, if provided."""
        if regex_patterns:
            pattern = regex_patterns.get(key)
            if pattern and not re.match(pattern, value):
                msg = f"Invalid format for {key}: {value} does not match {pattern}"
                raise ValueError(msg)

    def _build_query_part(self,
                          key: str,
                          value: any) -> str:
        """Build a query string part for the key-value pair."""
        if isinstance(value, list):
            # Join the list items into a comma-separated string
            str_val = ",".join(str(item) for item in value)  # Ensures each item is a string  # noqa: E501
            return f"{key}={str_val}"
        # Handle the case where value is not a list (e.g., a string or int)
        return f"{key}={value}"

    def set_query_string(self,
                          query_kwargs: dict,
                          expected_types: dict[str, type | tuple],
                          regex_patterns: dict[str, str] | None = None) -> str:
        """Build the query string from kwargs."""
        query_string_parts = []

        # Validate the arguments and build the query string
        for key, value in query_kwargs.items():
            # Validate key and type
            self._validate_key_and_type(key, value, expected_types)

            # Validate the format using regex (if applicable)
            if isinstance(value, str):
                self._validate_regex(key, value, regex_patterns)

            # Build the query string part and add it to the list
            query_part = self._build_query_part(key, value)
            query_string_parts.append(query_part)
        query_string = "&".join(query_string_parts)
        match = re.match(QUERY_URL_REGEX, query_string)
        if match:
            logging.basicConfig(level=logging.INFO)
            logging.info(" Valid query string")
        if not match:
            logging.basicConfig(level=logging.ERROR)
            logging.error(" Invalid query string")
            return ""

        return "&".join(query_string_parts)

def _get_today_date() -> str:
    """Get the current date.

    Returns:
        str: The current date in the format YYYY-MM-DD.
    """
    now = dt.datetime.now(tz=dt.datetime.now().astimezone().tzinfo)
    return now.strftime("%Y-%m-%d")

def save_data(data: dict,
              filename: str,
              response_type: str = "json",
              data_type: str = "raw") -> None:
    """Save data to a file.

    Args:
        data (dict): The data to be saved.
        filename (str): The name of the file to save the data to.
        response_type (str, optional): The type of the response (json/csv). Defaults to "json".
        data_type (str, optional): The type of data being saved (logs/metadata/raw/processed). Defaults to "raw".

    Returns:
        None
    """  # noqa: E501
    logging.basicConfig(level=logging.INFO)

    # Determine the correct directory based on data_type
    if data_type == "logs":
        save_dir = LOGS_DIR
    elif data_type == "metadata":
        save_dir = METADATA_DIR
    elif data_type == "processed":
        save_dir = PROCESSED_DIR
    else:  # Default to raw
        save_dir = RAW_DIR

    # Build the full file path
    file_path = save_dir / filename

    # Save the data
    if response_type == "json":
        logging.info(" Saving data to %s...", file_path)
        with file_path.open("w") as f:
            json.dump(data, f)
    elif response_type == "csv":
        logging.info(" Saving data to %s...", file_path)
        with file_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
    else:
        msg = "Unsupported response_type. Must be 'json' or 'csv'."
        raise ValueError(msg)

    logging.info(" Data successfully saved to %s", file_path)

if __name__ == "__main__":
    # Saving raw data
    save_data(data={"key": "value"},
              filename="raw_data.json",
              response_type="json",
              data_type="raw")

    # Saving processed data as CSV
    save_data(data=[["header1", "header2"], ["row1_col1", "row1_col2"]],
              filename="processed_data.csv",
              response_type="csv",
              data_type="raw")
