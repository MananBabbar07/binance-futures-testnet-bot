from binance.enums import *
from bot.client import get_client
import logging
import time

client = get_client()

def place_order(symbol, side, order_type, quantity, price=None):
    try:
        # ✅ Log request
        logging.info(
            f"REQUEST -> {symbol} {side} {order_type} qty={quantity} price={price}"
        )

        # ✅ Place order
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

        # ✅ Log initial response
        logging.info(f"INITIAL RESPONSE -> status={order['status']}")

        # ⏳ Wait briefly (Binance processes async)
        time.sleep(1)

        # ✅ Fetch updated order status
        updated_order = client.futures_get_order(
            symbol=symbol,
            orderId=order["orderId"]
        )

        # ✅ Clean structured log (IMPORTANT)
        logging.info(
            f"UPDATED RESPONSE -> status={updated_order['status']} "
            f"executedQty={updated_order['executedQty']} "
            f"avgPrice={updated_order.get('avgPrice')}"
        )

        return updated_order

    except Exception as e:
        logging.error(f"ERROR -> {str(e)}")
        raise