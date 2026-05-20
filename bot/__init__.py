"""
Trading Bot Package
An enterprise-grade, clean, and structured Python client for placing orders on Binance Futures Testnet.
"""

from bot.logging_config import setup_logging
from bot.client import get_binance_client
from bot.validators import (
    validate_all,
    validate_symbol,
    validate_side,
    validate_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.orders import place_futures_order

__all__ = [
    "setup_logging",
    "get_binance_client",
    "place_futures_order",
    "validate_all",
    "validate_symbol",
    "validate_side",
    "validate_type",
    "validate_quantity",
    "validate_price",
    "validate_stop_price",
]
