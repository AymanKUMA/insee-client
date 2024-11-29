"""This module contains the legal data API client.

To use the API, you need to register for an API key at
https://api.insee.fr/ and then set the API_KEY or CLIENT_KEY and CLIENT_SECRET variables using the setup cli to your
corresponding credentials.

Example:
    from pyinsee.insee_client import InseeClient
    
    # get bulk data
    client_bulk = InseeClient()
    bulk_data, header = client_bulk.get_bulk(
        data_type="siren",
        nombre = 5,
        date = "2022-01-01",
        )

    # get by number
    client_by_number = InseeClient()
    siren_data = client_by_number.get_by_number(
        data_type="siren",
        id_code = "000325175",
    )
"""
from __future__ import annotations

import base64
import json
from .logger import logger
from typing import ClassVar, TypedDict
import requests

from .config import (
    CLIENT_KEY,
    CLIENT_SECRET,
    INSEE_DATA_URL,
    RESPONSE_CODES,
    API_KEY,
)
from .utils import QueryBuilder

# adding the query bulder to the class
QUERY_BUILDER = QueryBuilder()

class BulkParams(TypedDict, total=False):
    """TypedDict for the BulkParams."""
    q: str | None
    date: str | None
    curseur: str | None
    debut: str | int | None
    nombre: str | int | None
    tri: str | list | None
    champs: str | list | None
    facette: str | list | None
    masquerValeursNulles: str | bool | None

class InseeClient:
    """Class for the legal data API client.

    To use the API, you need to register for an API key at
    https://insee.fr/ and then set the API_KEY variable in utils.py to your
    API key.

    Args:
        content_type (str, optional): The content type of the API response.
        Defaults to "json".

    Attributes:
        content_type (str): The content type of the API response.

    Methods:
        __init__(self, content_type : str = "json")

    class variables:
        __api_key: ClassVar[str | None] = None
        __base_url: ClassVar[str] = INSEE_DATA_URL
        __credentials: ClassVar[str] = base64.b64encode(
            f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode("utf-8")
        __response_codes: ClassVar[dict] = RESPONSE_CODES
        __token_url: ClassVar[str] = "https://api.insee.fr/token"
        )

    public methods:
        get_legal_data(self, data_type: str, id_code: str)
        get_bulk_data(self, data_type: str, **kwargs)

    private methods:
        _set_class_variables(self)
        _save_data(self, data : dict, filename : str)
        _get_token(self)
        _get_data(self, url : str)
        _get_bulk_data(self, url : str)
        _get_legal_data(self, url : str)
        _get_request(self, url : str, headers : dict, context : str)
    """

    # Setting up the class variables
    __api_key: ClassVar[str | None] = None
    __base_url: ClassVar[str] = INSEE_DATA_URL
    __credentials: ClassVar[str] = base64.b64encode(
        f"{CLIENT_KEY}:{CLIENT_SECRET}".encode()).decode("utf-8")
    __response_codes: ClassVar[dict] = RESPONSE_CODES
    __token_url: ClassVar[str] = "https://api.insee.fr/token"

    def __init__(self, content_type : str = "json") -> None:
        """Initialize the LegalData class.

        Args:
            api_key (str): The API key for the insee API.
            content_type (str, optional): The content type of the API response.
            Defaults to "json".

        Returns:
            None

        Raises:
            ValueError: If the content type is not 'json' or 'csv'.
        """
        if content_type not in ["json", "csv"]:
            msg = "Unsupported content type. Use 'json' or 'csv'."
            raise ValueError(msg)

        # Ensure class-level variables are set (this method will run once per class)
        self._set_class_variables()

        self.content_type = content_type
        self.headers = {
            'X-INSEE-Api-Key-Integration': f"{InseeClient.__api_key}",
        }
        self._set_headers(content_type=content_type)

    @classmethod
    def _set_class_variables(cls) -> None:
        """Set the class-level variables such as API key and credentials."""
        # Check if essential variables are set
        if not all([cls.__response_codes, cls.__base_url, cls.__credentials]):
            msg = "One or more required environment variables are missing."
            raise ValueError(msg)

        # Only request a new API key if it's not already set
        if cls.__api_key is None:
            logger.info("Fetching new API key from INSEE.")
            cls._fetch_api_key()

    @classmethod
    def _fetch_api_key(cls) -> None:
        """Fetch the API key (token) by authenticating with the INSEE API."""
        url = cls.__token_url
        headers = {
            "Authorization": f"Basic {cls.__credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "grant_type": "client_credentials",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data, timeout=10)

        if response.status_code == cls.__response_codes["OK"]:
            try:
                data = response.json()
                msg = f" Expires in: {data.get('expires_in')} Seconds"
                logger.warning(msg)
                msg = f" Token type: {data.get('token_type')}"
                logger.warning(msg)
                cls.__api_key = data.get("access_token")
                logger.info("API key retrieved successfully.")
            except json.JSONDecodeError:
                logger.exception("Failed to decode JSON response for API key.")
                msg = "Invalid API response."
                raise ValueError(msg) from json.JSONDecodeError
        else:
            msg = f"Failed to authenticate with INSEE: {response.status_code}, {response.text}"
            logger.error(msg)
            msg = "Failed to authenticate with INSEE API. setting the api key from env variable."
            logger.warning(msg)

            # setting up the API key from the env variable if the retrieval fails
            if API_KEY:
                cls.__api_key = API_KEY 
            else:
                msg = "API_KEY is not set in the environment variables."
                raise ValueError(msg)



    def _set_headers(self, content_type: str = "json") -> None:
        """Set headers according to the content type.

        Args:
            content_type (str, optional): The content type of the API response.
            Defaults to "json".

        Returns:
            None

        Raises:
            ValueError: If the content type is not 'json' or 'csv'.
        """
        logger.info("Setting headers' content type...")
        if content_type == "json":
            self.headers["Accept"] = "application/json"
        elif content_type == "csv":
            self.headers["Accept"] = "text/csv"
        else:
            msg = "Unsupported content type. Use 'json' or 'csv'."
            raise ValueError(msg)
        msg = f"Content type is set to {content_type}."
        logger.info(msg)

    def _get_headers(self) -> dict:
        """Get the headers for the API request.

        Returns:
            dict: The headers for the API request.
        """
        return self.headers

    def _get_info(self) -> dict:
        """Get the information about the API."""
        url = f"{InseeClient.__base_url}informations"
        context = f" Getting information... | [{self.content_type}]"
        response = self._get_request(url=url, headers=self.headers, context=context)
        return response.json()

    def _get_request(self, url: str, headers: dict, context: str) -> requests.Response:  # noqa: E501
        """Get the request for the API.
    
        Args:
            url (str): The URL for the API request.
            headers (dict): The headers for the API request.
            context (str): The context of the API request.
    
        Returns:
            requests.Response: The response from the API.
    
        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        logger.info("Requesting %s", context)
        try:
            response = requests.get(url=url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
        else:
            return response
        return response

    @staticmethod
    def verify_siren(siren : (int | str)) -> bool:
        """Verify if the siren is valid.

        Args:
            siren (int | str): The siren to verify.

        Returns:
            bool: True if the siren is valid, False otherwise.
        """
        length = 9
        return len(str(siren)) == length

    @staticmethod
    def verify_siret(siret : (int | str)) -> bool:
        """Verify if the siret is valid.

        Args:
            siret (int | str): The siret to verify.

        Returns:
            bool: True if the siret is valid, False otherwise.
        """
        length = 14
        return len(str(siret)) == length

    def get_bulk(self,
                      data_type: str = "siren",
                      **kwargs: BulkParams) -> dict:
        """Get bulk data (SIREN or SIRET) from INSEE API.

        Args:
            data_type (str): The type of data to retrieve, either "siren" or "siret".
            **kwargs (dict | None): The query parameters for the API request.
                q: str
                date: str
                curseur: str
                debut: (str, int)
                nombre: (str, int)
                tri: (str, list)
                champs: (str, list)
                facette.champ: (str, list)
                masquerValeursNulles: (str, bool)

        Raises:
            ValueError: If the query parameters are not valid or if `data_type` is not valid.

        Returns:
            dict: The response from the API.
        """
        # Validate the data_type
        if data_type not in ["siren", "siret"]:
            msg = f"Invalid data type: {data_type}. Must be 'siren' or 'siret'."
            raise ValueError(msg)

        # Expected keys
        expected_keys: dict = {
            "q": str,
            "date": str,
            "curseur": str,
            "debut": (str, int),
            "nombre": (str, int),
            "tri": (str, list),
            "champs": (str, list),
            "facette.champ": (str, list),
            "masquerValeursNulles": (str, bool),
        }

        # Regex patterns for special validations
        regex_patterns: dict = {
            "q": r"^[\w\s:()]+$",
            "date": r"\d{4}-\d{2}-\d{2}",
        }

        # Adjust the `facette.champ` argument if needed
        if "facette" in kwargs:
            kwargs["facette.champ"] = kwargs.pop("facette")

        # Build the query string
        query_string = QUERY_BUILDER.set_query_string(
            query_kwargs=kwargs,
            expected_types=expected_keys,
            regex_patterns=regex_patterns,
        )

        # Build the URL based on the data type (siren or siret)
        url = f"{InseeClient.__base_url}{data_type}?{query_string}"

        # Logging the request
        msg = f"Fetching bulk {data_type.upper()} data..."
        logger.info(msg)
        context = f"Fetching bulk {data_type.upper()} data from {url} | [{self.content_type}]"

        # Make the request
        response = self._get_request(url=url, headers=self.headers, context=context)

        # Handle response
        if self.content_type == "json":
            # Handle errors
            if response.status_code >= RESPONSE_CODES["BAD_REQUEST"]:
                status_code = f"Response code: {response.status_code}"
                description = f"Description: {response.json()['header']['message']}"
                msg = f"{status_code} - {description}"
                logger.error(msg)
                return None

            # Return the appropriate data based on the type
            if data_type == "siren":
                return response.json()["unitesLegales"], response.json()["header"]
            # "etablissements" if data_type == "siret":
            return response.json()["etablissements"], response.json()["header"]

        # Return raw content for non-JSON content types
        return response.content, response.headers

    def get_by_number(self,
                       data_type: str = "siren",
                       id_code : str | int | None = None,
                       **kwargs: dict) -> dict:
        """Get legal data from INSEE API for a given sirnen or siret number.

        Args:
            data_type (str): The type of data to retrieve, either "siren" or "siret".
            id_code (str | int): The id_code of the company.
            kwargs (dict | None): The query parameters for the API request.
            date : str                    champs : (str, list)
            masquerValeurNulles: (str, bool)

        Raises:
            ValueError: If the query parameters are not valid or if `data_type` is not valid.

        Returns:
            dict: The legal data for the company.
        """
        # Expected keys
        expected_keys : dict = {
            "date": str,
            "champs": (str, list),
            "masquerValeursNulles": (str, bool),
        }

        # Regex patterns
        regex_patterns : dict = {
            "date": r"\d{4}-\d{2}-\d{2}",
        }

        # Validate the data_type
        if data_type not in ["siren", "siret"]:
            msg = f"Invalid data type: {data_type}. Must be 'siren' or 'siret'."
            raise ValueError(msg)

        # Validate the id_code
        if not id_code:
            msg = f"Missing id_code for {data_type.upper()} data."
            raise ValueError(msg)
        if data_type == "siren" and not self.verify_siren(siren = id_code):
            msg = f"Invalid {data_type.upper()} number."
            raise ValueError(msg)
        if data_type == "siret" and not self.verify_siret(siret = id_code):
            msg = f"Invalid {data_type.upper()} number."
            raise ValueError(msg)

        # Build the query string
        query_string = QUERY_BUILDER.set_query_string(query_kwargs=kwargs,
                                                      expected_types=expected_keys,
                                                      regex_patterns=regex_patterns)

        # Build the URL based on the data type (siren or siret)
        url = f"{InseeClient.__base_url}{data_type}/{id_code}?{query_string}"

        # Logging the request
        logger.info("Fetching legal data for siren number " + str(id_code))  # noqa: G003
        context = f"Fetching {data_type.upper()} data from {url} | [{self.content_type}]"

        # Make the request
        response = self._get_request(url=url, headers=self.headers, context=context)
        if not response:
            logger.error(" Error fetching legal data for siren number %s", str(id_code))
            return None

        # Handle response
        # Return the appropriate data based on the type
        if data_type == "siren":
            return response.json()["uniteLegale"], response.json()["header"]
        elif data_type == "siret":  # data_type == "siret"
            return response.json()["etablissement"], response.json()["header"]

        # Return raw content for non-JSON content types
        return response.content, response.header

# ????????????????????????????????????????????????????????????????????????????
# ? TESTS FOR THE LEGAL DATA CLASS
if __name__ == "__main__":
    client_bulk = InseeClient()

    bulk_data, header = client_bulk.get_bulk(
        data_type="siren",
        nombre = 5,
        date = "2022-01-01",
        )

    client_by_number = InseeClient()
    siren_data = client_by_number.get_by_number(
        data_type="siren",
        id_code = "000325175",
    )
