from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return Client(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET"),
        testnet=True
    )