from binance.enums import *
from bot.client import get_client
import logging

client = get_client()

def place_order(symbol, side, order_type, quantity, price=None):
    try:
        logging.info(f"REQUEST → {symbol} {side} {order_type} {quantity} {price}")

        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )
        else:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=TIME_IN_FORCE_GTC
            )

        logging.info(f"RESPONSE → {order}")
        return order

    except Exception as e:
        logging.error(f"ERROR → {str(e)}")
        raise