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

class MLTrades(Strategy):
    def initialize(self, symbol:str="SPY"):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(
                self.symbol,
                10,
                "buy",
                type = "market"
            )
            self.submit_order(order)
            self.last_trade = "buy"

broker = Alpaca(ALPACA_CREDS)  
strat = MLTrades(name='mlstrat', broker = broker, parameteres = {})

#Back Testing Functions
start_date = datetime(2023,12,15)
end_date = datetime(2023,12,31)

strat.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={}
)