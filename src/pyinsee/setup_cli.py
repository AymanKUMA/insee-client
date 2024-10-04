import argparse
from getpass import getpass
from pathlib import Path

def create_or_update_env_file(env_path: Path, consumer_key: str = '', consumer_secret: str = '', insee_data_url: str = '', data_dir: str = '') -> None:
    """Creates or updates the .env file with user-provided environment variables.

    Args:
        env_path (Path): The path to the .env file.
        consumer_key (str): The consumer key (default: empty string).
        consumer_secret (str): The consumer secret (default: empty string).
        insee_data_url (str): The INSEE data URL (default: empty string).
        data_dir (str): The data directory (default: empty string).

    Returns:
        None
    """
    existing_vars = {}
    
    # Load existing environment variables if the file exists
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                key, value = line.strip().split('=')
                existing_vars[key] = value

    # Initialize environment variables with existing or default values
    env_vars = {
        'DATA_DIR': data_dir or existing_vars.get('DATA_DIR', 'data'),
        'CONSUMER_KEY': consumer_key or existing_vars.get('CONSUMER_KEY', ''),
        'CONSUMER_SECRET': consumer_secret or existing_vars.get('CONSUMER_SECRET', ''),
        'INSEE_DATA_URL': insee_data_url or existing_vars.get('INSEE_DATA_URL', 'https://api.insee.fr/entreprises/sirene/V3.11/')
    }

    # Handle user input for updates
    for var, value in env_vars.items():
        current_value = existing_vars.get(var, '')

        # Mask API keys if the variable name matches specific keys
        if var in ["CONSUMER_KEY", "CONSUMER_SECRET"]:
            masked_value = f"{current_value[:4]}{'*' * (len(current_value) - 8)}{current_value[-4:]}" if len(current_value) > 8 else current_value
            print(f"Current value for {var}: {masked_value}")
        else:
            print(f"Current value for {var}: {current_value}")

        # Prompt user for a new value apear as **** if the variable name matches specific keys
        if var in ["CONSUMER_KEY", "CONSUMER_SECRET"]:
            new_value = getpass(f"Update {var} (leave empty to keep current): ").strip()
        else:
            new_value = input(f"Update {var} (leave empty to keep current): ").strip()
        
        # Update environment variables
        if new_value:
            env_vars[var] = new_value
        else:
            env_vars[var] = current_value

    # Write updated values to .env file
    with open(env_path, 'w') as file:
        for var, value in env_vars.items():
            file.write(f"{var}={value}\n")
    
    print(f".env file created/updated at: {env_path}")

def print_example() -> None:
    """Prints the default .env file.

    Returns:
        None
    """
    path_to_example: Path = Path(__file__).parents[2] / "example.env"
    print("Here is the example .env file:")
    for line in path_to_example.read_text().splitlines():
        print(line)

def create_default_env_file(env_file_path: Path) -> None:
    """Creates a default.env file with the path to the .env file if it doesn't exist.

    Args:
        env_file_path (Path): The path to the .env file.

    Returns:
        None
    """
    package_dir: Path = Path(__file__).parent
    default_env_path: Path = package_dir / "default.env"
    
    with open(default_env_path, 'w') as f:
        f.write(f"ENV_FILE_PATH={env_file_path}")
    print(f"default.env file created/updated at: {default_env_path}")

def setup_env(env_path: Path = Path(".env")) -> None:
    parser = argparse.ArgumentParser(description="Set up the environment variables for the project.")
    
    parser.add_argument(
        '--env-path', 
        type=Path, 
        help="Path to an existing .env file or directory where a new one should be created.",
        default=Path(".env")
    )

    parser.add_argument(	
        '--example',
        action='store_true',
        help="Print an example .env file."
    )

    if parser.parse_args().example:
        print_example()
        return

    args: argparse.Namespace = parser.parse_args()
    
    env_path: Path = args.env_path
    
    # Ensure the directory exists
    if env_path.is_dir():
        env_file_path: Path = env_path / ".env"
        env_path.mkdir(parents=True, exist_ok=True)
    else:
        env_file_path: Path = env_path

    # Check if the .env file exists
    if env_file_path.exists():
        # Confirm with the user if they want to update the existing file
        update = input(f"File exists at given path: {env_file_path}\nDo you want to update the existing .env file? (yes/no): ").strip().lower()
        
        if update == 'yes':
            create_or_update_env_file(env_file_path)  # Call the function to handle updates
        else:
            print("No updates made to the .env file.")
    else:
        # .env file does not exist, ask for new inputs
        print("No existing .env file found. Please provide the following values:")
        data_dir: str = input("Enter the data output directory (default 'data'): ") or "data"
        consumer_key: str = input("Enter your Insee API consumer key: ")
        consumer_secret: str = input("Enter your Insee API consumer secret: ")
        insee_data_url: str = input("Enter the basic API URL (default 'https://api.insee.fr/entreprises/sirene/V3.11/'): ") or "https://api.insee.fr/entreprises/sirene/V3.11/"
        
        # Create data directory
        create_data_directory(data_dir)
        create_or_update_env_file(env_file_path, consumer_key, consumer_secret, insee_data_url, data_dir)
    
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

def main(): 
    """
    The main entry point of the .env setup CLI application.
    
    This function initiates the setup process by printing a welcome message and 
    calling the setup_env function to handle the environment setup.
    
    Parameters: None
    
    Returns: None
    """
    print("Welcome to the .env setup CLI!")
    setup_env()

if __name__ == "__main__":
    main()
