
<img src="static\img\Insee_logo.png" alt="Logo" height="100">


# Pyinsee - insee API Client

The Insee Client package is a Python library that provides a simple and easy-to-use interface for interacting with the Insee API. It allows you to retrieve legal data, such as company information, and save it to a dataset.



## Installation

To install the Insee Client package, run the following command:

```bash
  pip install pyinsee
```

Or 

```bash
  pip install git+https://github.com/AymanKUMA/insee-client.git 
```


## Initial usage

To run this project, you will need to add the following environment variables to your .env file.

The Insee Client package provides a command-line interface (CLI) for setting up environment variables. You can use the CLI by running the following command:

```
user@machine:~$ setup-cli --help


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


usage: setup-cli [-h] [--env-path ENV_PATH] [--example]

Set up the environment variables for the project.

options:
  -h, --help           show this help message and exit
  --env-path ENV_PATH  Path to an existing .env file or directory where a new one should be created.
  --example            Print an example .env file.
```

Note that the .env file will be created automatically via the CLI. 

You will be prompted to provide the following values:

* Data output directory (default: data)
* Insee API consumer key
* Insee API consumer secret
* API URL (default: https://api.insee.fr/entreprises/sirene/V3.11/)

If a .env file already exists at the specified path, you will be asked if you want to update the file.

Once the environment variables are available you can start using the insee-cli or the python module.




## Usage/Examples

### Insee CLI

Using insee cli you can either retrive bulk data, or a single data either by "*siren*" or "*siret*": 
```
   usage: insee-cli [-h] {insee_get_bulk,insee_get_by_number} ...

   CLI for querying INSEE data.

   positional arguments:
     {insee_get_bulk,insee_get_by_number}
        insee_get_bulk      Fetch bulk data from INSEE API
        insee_get_by_number Fetch legal data by number

   options:
      -h, --help            show this help message and exit
```

The first option is getting bulk data: 
```
    usage: insee-cli insee_get_bulk [-h] [--q Q] [--date DATE] [--curseur CURSEUR] [--debut DEBUT] [--nombre NOMBRE]
                                    [--tri [TRI ...]] [--champs [CHAMPS ...]] [--facette [FACETTE ...]] [--mvn MVN]
                                    [--save SAVE]
                                    {siren,siret} {json,csv}

    positional arguments:
      {siren,siret}         Type of data   to retrieve
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

If the argument '**save**' is not provided the CLI display the results. Note that the data is saved in the directory *data/raw/...*


