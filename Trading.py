import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ALPACA_CREDS = {
    "API_KEY":os.getenv('API_KEY'),
    "API_SECRET": os.getenv("API_SECRET"),
    #Switch to false if you would like to do non-paper trading
    "PAPER":True
}