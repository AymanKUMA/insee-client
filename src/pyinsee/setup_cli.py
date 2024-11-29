import argparse
from pathlib import Path
import site

def create_default_env_file(env_file_path: Path) -> None:
    """Creates a default.env file with the path to the .env file if it doesn't exist.

    Args:
        env_file_path (Path): The path to the .env file.

    Returns:
        None
    """
    if site.ENABLE_USER_SITE:
        package_dir: Path = Path(site.getusersitepackages())
    else:
        package_dir: Path = Path(site.getsitepackages()[0])
    print(f"Creating a default.env file in: {package_dir}")
    default_env_dir: Path = package_dir / "default-env-files"
    default_env_dir.mkdir(parents=True, exist_ok=True)
    default_env_path: Path = default_env_dir / "default.env"
    
    with open(default_env_path, 'w+') as f:
        lines = f.readlines()
        changed = False
        for i, line in enumerate(lines):
            if "PYINSEE_ENV_FILE_PATH=" in line:
                lines[i] = f"PYINSEE_ENV_FILE_PATH={env_file_path}\n"
                changed = True
        if not changed:
            lines.append(f"PYINSEE_ENV_FILE_PATH={env_file_path}\n")
        f.seek(0)
        f.writelines(lines)
    print(f"default.env file created/updated at: {default_env_path}")

def create_env_file(env_path: Path, client_key: str | None, client_secret: str | None, api_key: str | None, insee_data_url: str, data_dir: str) -> None:
    """Creates the .env file with user-provided environment variables."""
    env_path.parent.mkdir(parents=True, exist_ok=True)
    with open(env_path, 'w') as file:
        file.write(f"DATA_DIR={data_dir}\n")
        file.write(f"CLIENT_KEY={client_key}\n") if client_key else file.write("CLIENT_KEY=\n")
        file.write(f"CLIENT_SECRET={client_secret}\n") if client_secret else file.write("CLIENT_SECRET=\n")
        file.write(f"API_KEY={api_key}\n") if api_key else file.write("API_KEY=\n")
        file.write(f"INSEE_DATA_URL={insee_data_url}\n")
    print(f".env file created at: {env_path}")

    # create default.env file
    create_default_env_file(env_path)

    # create data directory
    create_data_directory(data_dir)

def update_env_file(env_path: Path, client_key: str, client_secret: str, api_key: str | None, insee_data_url: str, data_dir: str) -> None:
    """Updates or creates the .env file with the provided environment variables."""
    env_path.parent.mkdir(parents=True, exist_ok=True)
    existing_vars = {}

    if env_path.exists():
        with open(env_path) as file:
            for line in file:
                key, value = line.strip().split('=', 1)
                existing_vars[key] = value

    env_vars = {
        'DATA_DIR': data_dir or existing_vars.get('DATA_DIR', 'data'),
        'CLIENT_KEY': client_key or existing_vars.get('CLIENT_KEY', ''),
        'CLIENT_SECRET': client_secret or existing_vars.get('CLIENT_SECRET', ''),
        'API_KEY': api_key or existing_vars.get('API_KEY', ''),
        'INSEE_DATA_URL': insee_data_url or existing_vars.get('INSEE_DATA_URL', 'https://api.insee.fr/entreprises/sirene/V3.11/')
    }

    with open(env_path, 'w') as file:
        for key, value in env_vars.items():
            file.write(f"{key}={value}\n") if value else file.write(f"{key}=\n")
    print(f".env file updated at: {env_path}")

    # create default.env file
    create_default_env_file(env_path)

    # create data directory
    create_data_directory(data_dir or existing_vars.get('DATA_DIR', 'data'))

def setup_env(args: argparse.Namespace) -> None: 
    """Sets up the .env file with the provided arguments."""
    assert (args.client_key and args.client_secret) or args.api_key, "Either client key and secret or API key must be provided."
    env_path = args.env_path
    if env_path.is_dir():
        env_path = env_path / ".env"

    if env_path.exists() and not args.overwrite:
        print(f".env file exists at {env_path}. Use --overwrite to update it.")
        return

    update_env_file(
        env_path=env_path,
        client_key=args.client_key,
        client_secret=args.client_secret,
        api_key=args.api_key,
        insee_data_url=args.api_url,
        data_dir=args.data_dir
    )
    

def create_data_directory(base_dir: str) -> None:
    """
    Creates the base data directory and its subdirectories: logs, raw, processed, metadata.

    Args:
        base_dir (str): The base directory where the data directory and its subdirectories will be created.

    Returns:
        None
    """
    # Convert base_dir to Path object
    base_path = Path(base_dir)

    # Check if the base_path ends with '/data'
    if base_path.name == 'data':
        data_dir = base_path  # Use the existing data directory
    else:
        data_dir = base_path / "data"  # Create a 'data' directory in base_path

    # Define paths for each subdirectory
    logs_dir = data_dir / "logs"
    raw_dir = data_dir / "raw"
    processed_dir = data_dir / "processed"
    metadata_dir = data_dir / "metadata"

    # Create the data directory and subdirectories if they don't exist
    try:
        data_dir.mkdir(parents=True, exist_ok=True)  # Create data directory if it doesn't exist
        logs_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)
        processed_dir.mkdir(parents=True, exist_ok=True)
        metadata_dir.mkdir(parents=True, exist_ok=True)
        print(f"Directories created successfully: {data_dir}")
    except Exception as e:
        print(f"Error creating directories: {e}")

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Set up the .env file for the application.")
    parser.add_argument('--env-path', type=Path, default=Path(".env"), help="Path to the .env file.")
    parser.add_argument('--data-dir', type=Path, required=True, help="Path to the data directory.")
    parser.add_argument('--client-key', type=str, help="client key for the API.")
    parser.add_argument('--client-secret', type=str, help="client secret for the API.")
    parser.add_argument('--api-key', type=str, default="", help="API key for the API, set it up only in case the OAuth flow doesn't work.")
    parser.add_argument('--api-url', type=str, default="https://api.insee.fr/api-sirene/3.11/", help="API base URL.")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite the existing .env file.")
    return parser.parse_args()

def main(): 
    """
    The main entry point of the .env setup CLI application.
    
    This function initiates the setup process by printing a welcome message and 
    calling the setup_env function to handle the environment setup.
    
    Parameters: None
    
    Returns: None
    """
    print("""

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

    """)
    args = parse_arguments()
    setup_env(args)

if __name__ == "__main__":
    main()
