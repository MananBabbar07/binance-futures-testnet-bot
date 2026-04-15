import argparse
from bot.orders import place_order
from bot.validators import *
from bot.logging_config import setup_logging

setup_logging()

parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")

parser.add_argument("--symbol", required=True)
parser.add_argument("--side", required=True)
parser.add_argument("--type", required=True)
parser.add_argument("--quantity", required=True)
parser.add_argument("--price", required=False)

args = parser.parse_args()

try:
    validate_symbol(args.symbol)
    validate_side(args.side)
    validate_order_type(args.type)
    validate_quantity(args.quantity)

    if args.type == "LIMIT" and not args.price:
        raise ValueError("Price required for LIMIT order")

    print("\n📌 Order Summary:")
    print(vars(args))

    order = place_order(
        args.symbol,
        args.side,
        args.type,
        args.quantity,
        args.price
    )

    print("\n✅ Order Success:")
    print({
        "orderId": order.get("orderId"),
        "status": order.get("status"),
        "executedQty": order.get("executedQty"),
        "avgPrice": order.get("avgPrice", "N/A")
    })

except Exception as e:
    print(f"\n❌ Error: {str(e)}")