#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot CLI
Author: Antigravity

A clean, production-ready Command Line Interface to place MARKET, LIMIT, 
and STOP_MARKET orders on Binance Futures Testnet (USDT-M).
"""

import sys
import argparse
import logging
from typing import Dict, Any

# Reconfigure stdout and stderr to use UTF-8 encoding on Windows to prevent UnicodeEncodeError with emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from bot import (
    setup_logging,
    get_binance_client,
    place_futures_order,
    validate_all,
)
from binance.exceptions import BinanceAPIException, BinanceRequestException

def parse_arguments() -> argparse.Namespace:
    """
    Parses CLI arguments for placing a futures order.
    """
    parser = argparse.ArgumentParser(
        description="🚀 Binance Futures Testnet (USDT-M) Trading Bot CLI",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
    )
    
    parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL"],
        help="Order side:\n  BUY  - Go Long\n  SELL - Go Short"
    )
    
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET"],
        help="Order type:\n  MARKET      - Instant execution\n  LIMIT       - Pending order at a specific price\n  STOP_MARKET - Stop trigger market order"
    )
    
    parser.add_argument(
        "--quantity",
        type=float,
        required=True,
        help="Order quantity in terms of base asset (e.g., 0.001)"
    )
    
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Limit price (Required for LIMIT orders)"
    )
    
    parser.add_argument(
        "--stopPrice",
        "--stop-price",
        type=float,
        default=None,
        dest="stopPrice",
        help="Stop / Trigger price (Required for STOP_MARKET orders)"
    )

    return parser.parse_args()


def print_banner() -> None:
    """
    Prints a beautiful startup banner to standard output.
    """
    banner = """
===========================================================
     📊 BINANCE FUTURES TESTNET (USDT-M) TRADING BOT 📊
===========================================================
    """
    print(banner)


def print_order_summary(params: Dict[str, Any]) -> None:
    """
    Prints a clean, formatted summary of the order request.
    """
    print("\n--- 📝 ORDER REQUEST SUMMARY ---")
    print(f"  🔹 Symbol      : {params['symbol']}")
    print(f"  🔹 Side        : {params['side']}")
    print(f"  🔹 Type        : {params['type']}")
    print(f"  🔹 Quantity    : {params['quantity']}")
    
    if params["type"] == "LIMIT":
        print(f"  🔹 Limit Price : {params['price']}")
        print(f"  🔹 Time InForce: GTC (Good Till Cancelled)")
    elif params["type"] == "STOP_MARKET":
        print(f"  🔹 Stop Price  : {params['stopPrice']}")
        
    print("--------------------------------\n")


def print_order_response(response: Dict[str, Any]) -> None:
    """
    Prints details of a successful order response.
    """
    print("\n===========================================================")
    print("  ✅ SUCCESS: ORDER PLACED SUCCESSFULLY")
    print("===========================================================")
    print(f"  🔸 Order ID        : {response.get('orderId')}")
    print(f"  🔸 Client Order ID : {response.get('clientOrderId')}")
    print(f"  🔸 Symbol          : {response.get('symbol')}")
    print(f"  🔸 Side            : {response.get('side')}")
    print(f"  🔸 Type            : {response.get('type')}")
    print(f"  🔸 Orig Quantity   : {response.get('origQty')}")
    print(f"  🔸 Execution Status: {response.get('status')}")
    
    # LIMIT orders might return price, STOP_MARKET returns stopPrice, etc.
    if response.get('price') and float(response.get('price')) > 0:
        print(f"  🔸 Price           : {response.get('price')}")
    if response.get('stopPrice') and float(response.get('stopPrice')) > 0:
        print(f"  🔸 Stop Price      : {response.get('stopPrice')}")
        
    print(f"  🔸 Time in Force   : {response.get('timeInForce')}")
    print(f"  🔸 Position Side   : {response.get('positionSide', 'BOTH')}")
    print("===========================================================\n")


def main() -> None:
    # 1. Initialize Logger
    # Sets up dual logging to logs/trading.log and terminal stdout
    logger = setup_logging()

    # 2. Parse Command Line Arguments
    args = parse_arguments()

    print_banner()

    # 3. Perform Input Validation
    logger.info("Performing local parameter validations...")
    try:
        # Run validations to catch errors before sending network requests
        cleaned_params = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stopPrice
        )
        logger.info("Local parameter validation passed.")
    except ValueError as e:
        print(f"\n❌ VALIDATION ERROR: {e}", file=sys.stderr)
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

    # 4. Print Order Request Summary
    print_order_summary(cleaned_params)

    # 5. Connect to Binance Futures Testnet API
    try:
        client = get_binance_client()
    except ValueError as e:
        print(f"\n❌ CONFIGURATION ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except (BinanceAPIException, BinanceRequestException) as e:
        print(f"\n❌ CONNECTION ERROR: Binance API Client could not connect. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED CONNECTION ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # 6. Place Order on Testnet
    logger.info("Executing order placement on Binance Futures Testnet...")
    try:
        response = place_futures_order(
            client=client,
            symbol=cleaned_params["symbol"],
            side=cleaned_params["side"],
            order_type=cleaned_params["type"],
            quantity=cleaned_params["quantity"],
            price=cleaned_params["price"],
            stop_price=cleaned_params["stopPrice"]
        )
        
        # 7. Print Successful Response
        print_order_response(response)
        
    except BinanceAPIException as e:
        print(f"\n❌ BINANCE API ERROR: [{e.code}] {e.message}", file=sys.stderr)
        sys.exit(1)
    except BinanceRequestException as e:
        print(f"\n❌ NETWORK REQUEST ERROR: Could not connect to API server. Details: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
