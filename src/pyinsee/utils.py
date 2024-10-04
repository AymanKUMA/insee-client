"""Utility functions for the company_data_collection package."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
from .logger import logger
import re
from pathlib import Path
from .config import DATA_DIR

# Define the regex patterns
QUERY_URL_REGEX = r"(?:[^=&]+=[^=&]*&?)*"

def create_data_directories(base_dir: Path) -> None:
    """Creates necessary data directories if they don't exist.

    Args:
        base_dir (Path): The base directory for data storage.

    Returns:
        None
    """
    LOGS_DIR = base_dir / "logs"
    METADATA_DIR = base_dir / "metadata"
    RAW_DIR = base_dir / "raw"
    PROCESSED_DIR = base_dir / "processed"

    for directory in [LOGS_DIR, METADATA_DIR, RAW_DIR, PROCESSED_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

create_data_directories(Path(DATA_DIR))

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
            logger.info("Valid query string")
        if not match:
            logger.error("Invalid query string")
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
    """

    # Determine the correct directory based on data_type
    if data_type == "logs":
        save_dir = os.path.join(Path(DATA_DIR), "logs")
    elif data_type == "metadata":
        save_dir = os.path.join(Path(DATA_DIR), "metadata")
    elif data_type == "processed":
        save_dir = os.path.join(Path(DATA_DIR), "processed")
    else:  # Default to raw
        save_dir = os.path.join(Path(DATA_DIR), "raw")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Build the full file path
    file_path = Path(save_dir) / filename

    # Save the data
    if response_type == "json":
        logger.debug("Saving data to %s...", file_path)
        with file_path.open("w") as f:
            json.dump(data, f)
    elif response_type == "csv":
        logger.debug("Saving data to %s...", file_path)
        with file_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)
    else:
        msg = "Unsupported response_type. Must be 'json' or 'csv'."
        raise ValueError(msg)

    logger.info("%s data saved successfully.", str(data_type).capitalize())
    logger.debug(" Data successfully saved to %s", file_path)

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
              data_type="processed")
