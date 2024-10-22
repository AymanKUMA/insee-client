"""insee client CLI module."""
from __future__ import annotations

import json
import pprint
import sys
from pathlib import Path

import requests
sys.path.append(str(Path(__file__).parent.parent))

import argparse
from .logger import logger
import sys

from .insee_client import InseeClient
from .utils import get_today_date, save_data


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="CLI for querying INSEE data.")

    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the 'get_bulk' command
    bulk_parser = subparsers.add_parser("insee_get_bulk",
                                        help="Fetch bulk data from INSEE API")
    bulk_parser.add_argument("data_type",
                             choices=["siren", "siret"],
                             help="Type of data to retrieve")
    bulk_parser.add_argument("content_type",
                             choices=["json", "csv"],
                             help="Content type of the response")
    bulk_parser.add_argument("--q",
                             type=str,
                             help="Query parameter")
    bulk_parser.add_argument("--date",
                             type=str,
                             help="Date parameter (YYYY-MM-DD)")
    bulk_parser.add_argument("--curseur",
                             type=str,
                             default="*",
                             help="Cursor parameter (start value = *) Then you'll get the next cursor in the response")
    bulk_parser.add_argument("--debut",
                             type=str,
                             help="Start date or number")
    bulk_parser.add_argument("--nombre",
                             type=str,
                             help="Number of items",
                             default=20)
    bulk_parser.add_argument("--tri",
                             type=str,
                             nargs="*",
                             help="Sorting criteria")
    bulk_parser.add_argument("--champs",
                             type=str,
                             nargs="*",
                             help="Fields to retrieve")
    bulk_parser.add_argument("--facette",
                             type=str,
                             nargs="*",
                             help="Facette fields")
    bulk_parser.add_argument("--mvn",
                             type=str,
                             help="Hide null values (true/false)")
    bulk_parser.add_argument("--save",
                             type=bool,
                             help="Save data to a file",
                             default=False)

    # Subparser for the 'get_by_number' command
    by_number_parser = subparsers.add_parser("insee_get_by_number",
                                             help="Fetch legal data by number")
    by_number_parser.add_argument("data_type",
                                  choices=["siren", "siret"],
                                  help="Type of data to retrieve")
    by_number_parser.add_argument("content_type",
                                  choices=["json", "csv"],
                                  help="Content type of the response")
    by_number_parser.add_argument("id_code",
                                  type=str,
                                  help="ID code of the company")
    by_number_parser.add_argument("--date",
                                  type=str,
                                  help="Date parameter (YYYY-MM-DD)")
    by_number_parser.add_argument("--champs",
                                  type=str,
                                  nargs="*",
                                  help="Fields to retrieve")
    by_number_parser.add_argument("--mvn",
                                  type=str,
                                  help="Hide null values (true/false)")
    by_number_parser.add_argument("--save",
                                  type=bool,
                                  help="Save data to a file",
                                  default=False)
    return parser.parse_args()


def save_metadata(response: requests.Response, data_type: str, response_type: str, response_data_type: str) -> None:
    """Save metadata to a file.

    Args:
        data (dict): The metadata to be saved.
        filename (str): The name of the file to save the metadata to.
        response_type (str): The type of the response (json/csv).

    Returns:
        None
    """
    if response_type == "json":
        meta_data = json.loads(json.dumps(response[1]))
        save_data(data=meta_data,
                              filename=f"insee_metadata_{data_type}.json",
                              response_type="json",
                              response_data_type=response_data_type,
                              data_type="metadata")
    else:
        meta_data = json.loads(json.dumps(dict(response[1])))
        save_data(data=meta_data,
                               filename=f"insee_metadata_{data_type}.json",
                               response_type="json",
                               response_data_type=response_data_type,
                               data_type="metadata")


def main() -> None:
    """Main function."""
    args = parse_args()

    title = """

    ██████╗ ██╗   ██╗██╗███╗   ██╗███████╗███████╗███████╗
    ██╔══██╗╚██╗ ██╔╝██║████╗  ██║██╔════╝██╔════╝██╔════╝
    ██████╔╝ ╚████╔╝ ██║██╔██╗ ██║███████╗█████╗  █████╗  
    ██╔═══╝   ╚██╔╝  ██║██║╚██╗██║╚════██║██╔══╝  ██╔══╝
    ██║        ██║   ██║██║ ╚████║███████║███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝
     ...  .    .     |    pyinsee v0.1.0
    :     :    :     |    github.com/AymanKUMA/insee-client
     '''  '''' '     |    Welcome to the INSEE API CLI
    ------------------------------------------------------
    
    """

    print(title)

    # Create an instance of InseeClient
    client = InseeClient(content_type=args.content_type)

    if args.command == "insee_get_bulk":
        kwargs = {k: v for k, v in vars(args).items() if k not in ["data_type",
                                                                   "content_type",
                                                                   "command",
                                                                   "save",
                                                                   ] and v not in [
                                                                       None,
                                                                       "",
                                                                       [],
                                                                       {}]}
        # To ensure that the masquerValeursNulles parameter is correctly set as a key
        if 'mvn' in kwargs.keys():
            kwargs['masquerValeursNulles'] = kwargs.pop('mvn')
        try:
            logger.info("CLI command: insee_get_bulk | Fetching bulk data ...")
            response = client.get_bulk(data_type=args.data_type, **kwargs)

            if response is not None:
                save_metadata(response=response, 
                              data_type=args.data_type, 
                              response_type=args.content_type,
                              response_data_type=args.data_type)
                if args.content_type == "json":
                    if args.save:
                        data_list = response[0]
                        data_dict = {}
                        for item in data_list:
                            data_dict[item["siren"]] = item

                        save_data(data=data_dict, 
                              filename=f"{args.data_type}_{args.content_type}_{get_today_date()}.{args.content_type}", 
                              response_type=args.content_type, response_data_type=args.data_type)
                    else:
                        pprint.pprint(response[0])
                    
                else:
                    if args.save:
                        save_data(data=response[0].decode("utf-8"),
                              filename=f"{args.data_type}_{args.content_type}_{get_today_date()}.{args.content_type}",
                              response_type=args.content_type, response_data_type=args.data_type)
                    else:
                        print(type(response[0].decode("utf-8")))
                        print(response[0].decode("utf-8").replace("\\n", "\n"))

        except ValueError as e:
            msg = f"Error: {e}"
            logger.exception(msg)
            sys.exit(1)

    elif args.command == "insee_get_by_number":
        kwargs = {k: v for k, v in vars(args).items() if k not in ["data_type",
                                                                   "content_type",
                                                                   "id_code",
                                                                   "command",
                                                                   "save",
                                                                   ] and v not in [None,
                                                                                  "",
                                                                                  [],
                                                                                  {}]}
        # To ensure that the masquerValeursNulles parameter is correctly set as a key
        if 'mvn' in kwargs.keys():
            kwargs['masquerValeursNulles'] = kwargs.pop('mvn')
        try:
            logger.info("CLI command: insee_get_by_number | Fetching legal data ...")
            response = client.get_by_number(data_type=args.data_type,
                                            id_code=args.id_code,
                                            **kwargs)
            logger.info(response)
            if args.save:
                save_data(data=response, 
                              filename=f"{args.data_type}_{args.content_type}_{get_today_date()}.{args.content_type}", 
                              response_type=args.content_type, response_data_type=args.data_type)

        except ValueError as e:
            msg = f"Error: {e}"
            logger.exception(msg)
            sys.exit(1)

if __name__ == "__main__":
    main()


