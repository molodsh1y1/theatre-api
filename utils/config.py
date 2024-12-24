import logging
import os
from pathlib import Path
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def get_env_variable(variable_name: str) -> str:
    """
    Retrieve the value of an environment variable.
    :param variable_name: The name of the environment variable to retrieve.
    :return: The value of the environment variable.
    :raises KeyError: If the environment variable is not found.
    """
    try:
        var_value = os.environ[variable_name]
        logging.info(f"Successfully retrieved the {variable_name} environment variable")
        return var_value
    except KeyError:
        error_msg = f"Set the {variable_name} environment variable"
        logging.error(error_msg)
        raise KeyError({"error": error_msg})
