import logging
from typing import Optional, List

logger = logging.getLogger("bot.validators")

# Allowed configuration values
ALLOWED_SIDES: List[str] = ["BUY", "SELL"]
ALLOWED_TYPES: List[str] = ["MARKET", "LIMIT", "STOP_MARKET"]

def validate_symbol(symbol: str) -> str:
    """
    Validates the trading symbol (e.g., BTCUSDT).
    
    Args:
        symbol (str): The symbol to validate.
        
    Returns:
        str: The cleaned, uppercase symbol.
        
    Raises:
        ValueError: If symbol is empty or invalid.
    """
    if not symbol or not isinstance(symbol, str):
        error_msg = "Symbol must be a non-empty string (e.g., 'BTCUSDT')."
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    cleaned_symbol = symbol.strip().upper()
    if len(cleaned_symbol) < 3:
        error_msg = f"Symbol '{symbol}' is too short. Must be a valid trading pair like 'BTCUSDT'."
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    return cleaned_symbol


def validate_side(side: str) -> str:
    """
    Validates that the order side is either BUY or SELL.
    
    Args:
        side (str): The side value.
        
    Returns:
        str: Cleaned, uppercase side value.
        
    Raises:
        ValueError: If the side is invalid.
    """
    if not side or not isinstance(side, str):
        error_msg = f"Side must be a non-empty string. Choose from {ALLOWED_SIDES}."
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    cleaned_side = side.strip().upper()
    if cleaned_side not in ALLOWED_SIDES:
        error_msg = f"Invalid side '{side}'. Must be one of: {', '.join(ALLOWED_SIDES)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    return cleaned_side


def validate_type(order_type: str) -> str:
    """
    Validates that the order type is one of the supported types (MARKET, LIMIT, STOP_MARKET).
    
    Args:
        order_type (str): The order type.
        
    Returns:
        str: Cleaned, uppercase order type.
        
    Raises:
        ValueError: If the order type is unsupported.
    """
    if not order_type or not isinstance(order_type, str):
        error_msg = f"Order type must be a non-empty string. Choose from {ALLOWED_TYPES}."
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    cleaned_type = order_type.strip().upper()
    if cleaned_type not in ALLOWED_TYPES:
        error_msg = f"Invalid order type '{order_type}'. Supported types: {', '.join(ALLOWED_TYPES)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    return cleaned_type


def validate_quantity(quantity: float) -> float:
    """
    Validates that quantity is greater than zero.
    
    Args:
        quantity (float): The quantity of the asset.
        
    Returns:
        float: Verified positive quantity.
        
    Raises:
        ValueError: If quantity is zero, negative, or not a number.
    """
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        error_msg = f"Quantity must be a valid number, received: {quantity}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if qty <= 0.0:
        error_msg = f"Quantity must be strictly greater than 0. Received: {qty}"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    return qty


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """
    Validates that a valid price is supplied if the order type is LIMIT.
    
    Args:
        price (Optional[float]): The limit price.
        order_type (str): The type of the order (should be already validated).
        
    Returns:
        Optional[float]: Verified price float or None.
        
    Raises:
        ValueError: If order type is LIMIT but price is missing or invalid.
    """
    if order_type.upper() == "LIMIT":
        if price is None:
            error_msg = "Price parameter is mandatory for LIMIT orders."
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        try:
            val_price = float(price)
        except (TypeError, ValueError):
            error_msg = f"Price must be a valid number, received: {price}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if val_price <= 0.0:
            error_msg = f"Price must be strictly greater than 0 for LIMIT orders. Received: {val_price}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        return val_price
        
    # For MARKET or STOP_MARKET orders, price is not required
    return None


def validate_stop_price(stop_price: Optional[float], order_type: str) -> Optional[float]:
    """
    Validates that a valid stopPrice is supplied if the order type is STOP_MARKET.
    
    Args:
        stop_price (Optional[float]): The stop/trigger price.
        order_type (str): The type of the order (should be already validated).
        
    Returns:
        Optional[float]: Verified stopPrice float or None.
        
    Raises:
        ValueError: If order type is STOP_MARKET but stopPrice is missing or invalid.
    """
    if order_type.upper() == "STOP_MARKET":
        if stop_price is None:
            error_msg = "stopPrice parameter is mandatory for STOP_MARKET orders."
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        try:
            val_stop = float(stop_price)
        except (TypeError, ValueError):
            error_msg = f"stopPrice must be a valid number, received: {stop_price}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        if val_stop <= 0.0:
            error_msg = f"stopPrice must be strictly greater than 0 for STOP_MARKET orders. Received: {val_stop}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        return val_stop
        
    # For MARKET or LIMIT orders, stop price is not required
    return None


def validate_all(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: Optional[float] = None, 
    stop_price: Optional[float] = None
) -> dict:
    """
    Helper function to run all validations and return a dictionary of cleaned parameters.
    
    Args:
        symbol (str): Trading pair.
        side (str): BUY or SELL.
        order_type (str): MARKET, LIMIT, or STOP_MARKET.
        quantity (float): Quantity of contract.
        price (Optional[float]): Limit price (for LIMIT).
        stop_price (Optional[float]): Stop trigger price (for STOP_MARKET).
        
    Returns:
        dict: Cleaned and verified parameters.
    """
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_type = validate_type(order_type)
    clean_qty = validate_quantity(quantity)
    clean_price = validate_price(price, clean_type)
    clean_stop_price = validate_stop_price(stop_price, clean_type)
    
    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "type": clean_type,
        "quantity": clean_qty,
        "price": clean_price,
        "stopPrice": clean_stop_price
    }
