
<img src="static\img\Insee_logo.png" alt="Logo" height="100">


# Pyinsee - insee API Client

The Insee Client package is a Python library that provides a simple and easy-to-use interface for interacting with the Insee API. It allows you to retrieve legal data, such as company information, and save it to a dataset.



## Installation

To install the Insee Client package, run the following command:

```shell
  pip install pyinsee
```

Or 

```shell
  pip install git+https://github.com/AymanKUMA/insee-client.git 
```


## Initial usage

To run this project, you will need to add the following environment variables to your .env file.

The Insee Client package provides a command-line interface (CLI) for setting up environment variables. You can use the CLI by running the following command:

```shell
setup-cli --help
```
Output:
```


    ██████╗ ██╗   ██╗██╗███╗   ██╗███████╗███████╗███████╗
    ██╔══██╗╚██╗ ██╔╝██║████╗  ██║██╔════╝██╔════╝██╔════╝
    ██████╔╝ ╚████╔╝ ██║██╔██╗ ██║███████╗█████╗  █████╗
    ██╔═══╝   ╚██╔╝  ██║██║╚██╗██║╚════██║██╔══╝  ██╔══╝
    ██║        ██║   ██║██║ ╚████║███████║███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝
     ...  .    .     |    pyinsee v0.1.0
    :     :    :     |    github.com/AymanKUMA/insee-client
     '''  '''' '     |    Welcome to the .env setup CLI!
    ------------------------------------------------------


usage: py-insee-setup [-h] [--env-path ENV_PATH] --data-dir DATA_DIR [--client-key CLIENT_KEY] [--client-secret CLIENT_SECRET] [--api-key API_KEY] [--api-url API_URL] [--overwrite]

Set up the .env file for the application.

options:
  -h, --help            show this help message and exit
  --env-path ENV_PATH   Path to the .env file.
  --data-dir DATA_DIR   Path to the data directory.
  --client-key CLIENT_KEY
                        client key for the API.
  --client-secret CLIENT_SECRET
                        client secret for the API.
  --api-key API_KEY     API key for the API, set it up only in case the OAuth flow doesn't work.
  --api-url API_URL     API base URL.
  --overwrite           Overwrite the existing .env file.
```

Note that the .env file will be created automatically via the CLI. 

You will be prompted to provide the following values:

* Data output directory (default: data)
* Insee API consumer key
* Insee API consumer secret
* API URL (default: https://api.insee.fr/api-sirene/3.11/)

If a .env file already exists at the specified path, you will be asked if you want to update the file.

Once the environment variables are available you can start using the insee-cli or the python module.




## Usage/Examples

### Insee CLI

Using py-insee cli you can either retrive bulk data, or a single data either by "*siren*" or "*siret*": 
```
usage: py-insee  [-h] {insee_get_bulk,insee_get_by_number} ...

CLI for querying INSEE data.

positional arguments:
  {insee_get_bulk,insee_get_by_number}
    insee_get_bulk      Fetch bulk data from INSEE API
    insee_get_by_number
                        Fetch legal data by number

options:
  -h, --help            show this help message and exit
```

The first option is getting bulk data: 
```
usage: py-insee  insee_get_bulk [-h] [--q Q] [--date DATE] [--curse
CURSEUR] [--debut DEBUT] [--nombre NOMBRE] [--tri [TRI ...]] [--cham
[CHAMPS ...]] [--facette [FACETTE ...]] [--mvn MVN] [--save SAVE]
                                
                                {siren,siret} {json,csv}

positional arguments:
  {siren,siret}         Type of data to retrieve
  {json,csv}            Content type of the response

options:
  -h, --help            show this help message and exit
  --q Q                 Query parameter
  --date DATE           Date parameter (YYYY-MM-DD)
  --curseur CURSEUR     Cursor parameter (start value = *) Then you'll get the next cursor in the response
  --debut DEBUT         Start date or number
  --nombre NOMBRE       Number of items
  --tri [TRI ...]       Sorting criteria
  --champs [CHAMPS ...]
                        Fields to retrieve
  --facette [FACETTE ...]
                        Facette fields
  --mvn MVN             Hide null values (true/false)
  --save SAVE           Save data to a file

```

The first option is getting data by number:

```
usage: py-insee insee_get_by_number [-h] [--date DATE] [--champs [CHAMPS ...]] [--mvn MVN] [--save SAVE] {siren,siret} id_code

positional arguments:
  {siren,siret}         Type of data to retrieve
  id_code               ID code of the company

options:
  -h, --help            show this help message and exit
  --date DATE           Date parameter (YYYY-MM-DD)
  --champs [CHAMPS ...]
                        Fields to retrieve
  --mvn MVN             Hide null values (true/false)
  --save SAVE           Save data to a file
```

If the argument '**save**' is not provided the CLI display the results. Note that the data is saved in the directory *data/raw/...*

### Python usage
Setup the envirement variable via the cli in your project and then import the Client from the pyinsee: 

```python
from pyinsee.insee_client import InseeClient
```

1. **Get data bulk :**
Get bulk data of either siren or siret numbers: 

```
get_bulk(data_type: 'str' = 'siren', **kwargs: 'BulkParams') -> 'dict' method of pyinsee.insee_client.InseeClient instance
    Get bulk data (SIREN or SIRET) from INSEE API.

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
```

**Example** 
```python 
# get bulk
client_bulk = InseeClient()

bulk_data, header = client_bulk.get_bulk(
  data_type="siren",
  nombre = 5,
  date = "2022-01-01",
)
```

2. **Get data by number :**
Get data either by Siren or Siret numbers. 

```
get_by_number(data_type: 'str' = 'siren', id_code: 'str | int | None' = None, **kwargs: 'dict') -> 'dict' method of pyinsee.insee_client.InseeClient instance
    Get legal data from INSEE API for a given sirnen or siret number.

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
```

**Example**

```python
# get by number
client_by_number = InseeClient()

siren_data = client_by_number.get_by_number(
    data_type="siren",
    id_code = "000325175",
)
```
### Updates

The API provided by the INSEE has changed and currently I'm trying to use Oauth service to retrieve the API key instead of setting it manually.