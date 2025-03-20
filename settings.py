import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory where the project is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get environment settings
ENVIRONMENT: str = os.getenv("ENVIRONMENT")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE")
LOG_FILE_PATH: str = os.path.join(BASE_DIR, LOG_FILE)

KLINES_DIR: str = os.getenv("KLINES_DIR")
RESULTS_DIR: str = os.getenv("RESULTS_DIR")

DATE_FORMAT: str = "%Y-%m-%d"


def load_config(config_file_path: str) -> dict:
    with open(config_file_path, "r") as file:
        config_data = json.load(file)
    return config_data


CONFIG_PATH: str = os.getenv("CONFIG_PATH")
CONFIG_FILE_PATH: str = os.path.join(BASE_DIR, CONFIG_PATH)

config: dict = load_config(CONFIG_FILE_PATH)

SYMBOLS_CONFIG: dict = config.get("symbols")
PORTFOLIO_CONFIG: dict = config.get("portfolio")
STRATEGIES_CONFIG: dict = config.get("strategies")

SYMBOLS: list[str] = list(SYMBOLS_CONFIG.keys())
ASSET_TYPES: list[str] = ["single-asset", "multi-asset"]

TG_TOKEN: str = os.getenv("TG_TOKEN")

HTTPX_TIMEOUT = int(os.getenv("HTTPX_TIMEOUT"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS"))
RETRY_MULTIPLIER = int(os.getenv("RETRY_MULTIPLIER"))
RETRY_MIN_WAIT = int(os.getenv("RETRY_MIN_WAIT"))
RETRY_MAX_WAIT = int(os.getenv("RETRY_MAX_WAIT"))

