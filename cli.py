import argparse
from bot.orders import place_order
from bot import validators
from bot.logging_config import setup_logging

setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")

    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, help="Price (required for LIMIT)")

    args = parser.parse_args()

    try:
        # ✅ Validation
        validators.validate_symbol(args.symbol)
        validators.validate_side(args.side)
        validators.validate_order_type(args.type)
        validators.validate_quantity(args.quantity)

        if args.type == "LIMIT":
            if not args.price:
                raise ValueError("Price required for LIMIT order")
            validators.validate_price(args.price)

        # ✅ Order summary
        print("\n📌 Order Summary:")
        print(vars(args))

        # ✅ Place order
        order = place_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        # ✅ Result interpretation
        print("\n📊 Order Result:")

        if order.get("type") == "MARKET":
            if order.get("status") == "FILLED":
                print("✅ Market order fully executed")
            else:
                print("⚠️ Market order not filled yet (unexpected)")

        elif order.get("type") == "LIMIT":
            if order.get("status") == "NEW":
                print("⏳ Limit order placed and waiting for execution")
            elif order.get("status") == "FILLED":
                print("✅ Limit order executed")

        # ✅ Clean output
        print({
            "orderId": order.get("orderId"),
            "symbol": order.get("symbol"),
            "side": order.get("side"),
            "type": order.get("type"),
            "status": order.get("status"),
            "executedQty": order.get("executedQty"),
            "avgPrice": order.get("avgPrice", "N/A")
        })

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()