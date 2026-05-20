import logging
from typing import Optional, Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger("bot.orders")

def place_futures_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Places a Futures order on the Binance Futures Testnet (USDT-M).
    Supports MARKET, LIMIT, and STOP_MARKET order types.
    
    Args:
        client (Client): The initialized python-binance client instance.
        symbol (str): The symbol to trade (e.g., 'BTCUSDT').
        side (str): Order direction, 'BUY' or 'SELL'.
        order_type (str): Type of the order, 'MARKET', 'LIMIT', or 'STOP_MARKET'.
        quantity (float): The trade quantity.
        price (Optional[float]): The limit price (required for LIMIT orders).
        stop_price (Optional[float]): The trigger/stop price (required for STOP_MARKET orders).
        
    Returns:
        Dict[str, Any]: The response dictionary from the Binance API.
        
    Raises:
        BinanceAPIException: If the Binance API returns an error.
        BinanceRequestException: If the request fails before reaching Binance.
        Exception: For other unexpected failures.
    """
    # 1. Prepare base parameters
    # Note: Quantity is sent as a string or float. We keep it as float or string.
    # To avoid scientific notation issues with float representation, we format it.
    order_params: Dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }

    # 2. Add type-specific parameters
    if order_type == "LIMIT":
        # Price is mandatory for LIMIT order
        order_params["price"] = price
        # timeInForce is mandatory for LIMIT order on Binance Futures
        order_params["timeInForce"] = "GTC"  # Good Till Cancelled
        
    elif order_type == "STOP_MARKET":
        # stopPrice is mandatory for STOP_MARKET order
        order_params["stopPrice"] = stop_price

    # 3. Log the API request details
    logger.info(
        f"Sending Futures Order Request: symbol={symbol}, side={side}, type={order_type}, "
        f"quantity={quantity}, price={price}, stopPrice={stop_price}"
    )
    logger.debug(f"Complete request parameters: {order_params}")

    # 4. Perform request with proper exception handling
    try:
        # Call binance-python's futures_create_order method
        response = client.futures_create_order(**order_params)
        
        # 5. Log the successful API response
        logger.info(
            f"Order successfully placed! OrderID: {response.get('orderId')} | Status: {response.get('status')}"
        )
        logger.debug(f"Complete API Response: {response}")
        
        return response

    except BinanceAPIException as e:
        error_msg = (
            f"Binance API Exception occurred while placing order.\n"
            f"  - Message: {e.message}\n"
            f"  - Code: {e.code}\n"
            f"  - HTTP Status: {e.status_code}"
        )
        logger.error(error_msg)
        raise e

    except BinanceRequestException as e:
        error_msg = f"Binance Request Exception occurred (connection issue): {str(e)}"
        logger.error(error_msg)
        raise e

    except Exception as e:
        error_msg = f"Unexpected system error occurred while placing order: {str(e)}"
        logger.error(error_msg)
        raise e
