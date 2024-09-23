import argparse
from pathlib import Path

def create_or_update_env_file(env_path: Path, log_dir: str, env_file_path: str, consumer_key: str, consumer_secret: str, insee_data_url: str) -> None:
    """Creates or updates the .env file with user-provided environment variables.

    Args:
        env_path (Path): The path to the .env file.
        log_dir (str): The log directory.
        env_file_path (str): The path to the .env file.
        consumer_key (str): The consumer key.
        consumer_secret (str): The consumer secret.
        insee_data_url (str): The INSEE data URL.

    Returns:
        None
    """
    env_vars = {
        'LOG_DIR': log_dir,
        'ENV_FILE_PATH': env_file_path,
        'CONSUMER_KEY': consumer_key,
        'CONSUMER_SECRET': consumer_secret,
        'INSEE_DATA_URL': insee_data_url
    }

    if env_path.exists():
        print(f"\nFile exists at given path: {env_path}")
        update = input("Do you want to update the existing .env file? (yes/no): ").strip().lower()

        if update != 'yes':
            print("Update canceled. Exiting.")
            return

        with open(env_path, 'r') as file:
            lines = file.readlines()
            existing_vars = {line.split('=')[0]: line.split('=')[1].strip() for line in lines}

        # Update only if user provides a new value
        for var, value in env_vars.items():
            if var in ["LOG_DIR", "CONSUMER_KEY", "CONSUMER_SECRET", "INSEE_DATA_URL"]:
                current_value = existing_vars.get(var, '')
                new_value = input(f"Update {var} (current: {current_value}, leave empty to keep current): ").strip()
                if new_value:
                    env_vars[var] = new_value
                else:
                    env_vars[var] = current_value

    else:
        # If file doesn't exist, use provided values
        env_vars = {
            'LOG_DIR': log_dir,
            'ENV_FILE_PATH': env_file_path,
            'CONSUMER_KEY': consumer_key,
            'CONSUMER_SECRET': consumer_secret,
            'INSEE_DATA_URL': insee_data_url
        }

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
    print(f"Package directory: {package_dir}")
    default_env_path: Path = package_dir / "default.env"
    
    with open(default_env_path, 'w') as f:
        f.write(f"ENV_FILE_PATH={env_file_path}")
    print(f"default.env file created/updated at: {default_env_path}")

def setup_env(env_path: Path = Path(".env")) -> None:
    """CLI for setting up the .env environment file with user input.

    Args:
        env_path (Path, optional): Path to an existing .env file or directory where a new one should be created. Defaults to ".env".

    Returns:
        None

    Raises:          
        argparse.ArgumentTypeError: If the provided path is not a valid .env file or directory.  
    """
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

    args: argparse.Namespace = parser.parse_args()
    
    if args.example:
        print_example()
        return

    env_path: Path = args.env_path
    
    # Check if user provided a directory or file path
    if env_path.is_dir():
        env_file_path: Path = env_path / ".env"
    else:
        env_file_path: Path = env_path

    log_dir: str = ""
    env_file_path_input: str = ""
    consumer_key: str = ""
    consumer_secret: str = ""
    insee_data_url: str = ""

    if env_file_path.exists():
        create_or_update_env_file(env_file_path, log_dir, env_file_path_input, consumer_key, consumer_secret, insee_data_url)
        env_file_path_input: str = str(env_file_path)
        create_default_env_file(env_file_path_input)
    else:
        log_dir: str = input("Enter the logs output directory (default 'logs'): ") or "logs"
        env_file_path_input: str = str(env_file_path)
        consumer_key: str = input("Enter your Insee API consumer key: ")
        consumer_secret: str = input("Enter your Insee API consumer secret: ")
        insee_data_url: str = input("Enter the basic API URL (default 'https://api.insee.fr/entreprises/sirene/V3.11/'): ") or "https://api.insee.fr/entreprises/sirene/V3.11/"

        create_or_update_env_file(env_file_path, log_dir, env_file_path_input, consumer_key, consumer_secret, insee_data_url)

        create_default_env_file(env_file_path_input)

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
