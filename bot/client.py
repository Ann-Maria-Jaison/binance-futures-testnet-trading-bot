import os
import logging
from typing import Optional
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

logger = logging.getLogger("bot.client")

def get_binance_client() -> Client:
    """
    Loads API keys from the environment variables, validates them,
    and initializes the Binance API Client configured for Futures Testnet.
    
    Returns:
        Client: An instance of python-binance Client connected to Futures Testnet.
        
    Raises:
        ValueError: If API keys are missing, empty, or contain default placeholder values.
    """
    # Load environment variables from the .env file in the working directory
    load_dotenv()

    api_key: Optional[str] = os.getenv("BINANCE_API_KEY")
    api_secret: Optional[str] = os.getenv("BINANCE_API_SECRET")

    # Clean the keys by stripping whitespaces
    api_key = api_key.strip() if api_key else ""
    api_secret = api_secret.strip() if api_secret else ""

    # Check for empty or missing keys
    if not api_key or not api_secret:
        error_msg = (
            "Binance API Key and Secret must be configured in the environment or a .env file. "
            "Please check that BINANCE_API_KEY and BINANCE_API_SECRET are set."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Check for default placeholders
    placeholders = ["your_testnet_api_key_here", "your_testnet_api_secret_here", "placeholder", "key", "secret"]
    if api_key.lower() in placeholders or api_secret.lower() in placeholders:
        error_msg = (
            "Detected default placeholder values for BINANCE_API_KEY or BINANCE_API_SECRET. "
            "Please replace them with your actual Binance Futures Testnet credentials."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("Initializing Binance Client connected to Futures Testnet...")
    
    try:
        # Initialize client with testnet parameter set to True
        # For python-binance, testnet=True automatically configures the REST and WebSocket URLs for Testnet
        client = Client(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True
        )
        
        # Test connectivity by pinging the Futures API
        # This acts as an immediate sanity check for API keys and connection issues
        client.futures_ping()
        logger.info("Binance Futures Testnet Client successfully connected and verified.")
        return client

    except BinanceAPIException as e:
        logger.error(f"Binance API error during initialization: {e.message} (Code: {e.code})")
        raise e
    except Exception as e:
        logger.error(f"Unexpected connection error during initialization: {str(e)}")
        raise e
