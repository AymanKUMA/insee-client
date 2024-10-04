"""insee client CLI module."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import argparse
from .logger import logger
import sys

from .insee_client import InseeClient

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
    bulk_parser.add_argument("--q",
                             type=str,
                             help="Query parameter")
    bulk_parser.add_argument("--date",
                             type=str,
                             help="Date parameter (YYYY-MM-DD)")
    bulk_parser.add_argument("--curseur",
                             type=str,
                             help="Cursor parameter")
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

    # Subparser for the 'get_by_number' command
    by_number_parser = subparsers.add_parser("insee_get_by_number",
                                             help="Fetch legal data by number")
    by_number_parser.add_argument("data_type",
                                  choices=["siren", "siret"],
                                  help="Type of data to retrieve")
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
    return parser.parse_args()

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
    pyinsee v0.1.0   |   github.com/AymanKUMA/insee-client
    ------------------------------------------------------
    Welcome to the INSEE API CLI application . . . . . . . 
    """

    print(title)

    # Create an instance of InseeClient
    client = InseeClient(content_type="json")

    if args.command == "insee_get_bulk":
        kwargs = {k: v for k, v in vars(args).items() if k not in ["data_type",
                                                                   "command",
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
            logger.info(response)
        except ValueError as e:
            msg = f"Error: {e}"
            logger.exception(msg)
            sys.exit(1)

    elif args.command == "insee_get_by_number":
        kwargs = {k: v for k, v in vars(args).items() if k not in ["data_type",
                                                                   "id_code",
                                                                   "command"]
                                                                   and v not in [None,
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
        except ValueError as e:
            msg = f"Error: {e}"
            logger.exception(msg)
            sys.exit(1)

if __name__ == "__main__":
    main()
