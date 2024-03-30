import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from dotenv import load_dotenv
from alpaca_trade_api import REST
from timedelta import Timedelta

load_dotenv()

ALPACA_CREDS = {
    "API_KEY":os.getenv('API_KEY'),
    "API_SECRET": os.getenv("API_SECRET"),
    "BASE_URL":os.getenv("BASE_URL"),
    #Switch to false if you would like to do non-paper trading
    "PAPER":True
}

class MLTrades(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=os.getenv("BASE_URL"), key_id = os.getenv('API_KEY'), secret_key = os.getenv("API_SECRET"))

    def pos_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price)
        return cash,last_price , quantity
    
    def getDates(self):
        today = self.get_datetime()
        threePrior = today - Timedelta(days = 4)
        return today.strfttime('%Y-%m-%d'), threePrior
    
    def getNews(self):
        today , three  = self.getDates()
        news = self.api.get_news(symbol=self.symbol, start= three , end=today)
        news = [ev.__dict__["_raw"]["headline"]for ev in news]

    def on_trading_iteration(self):
        cash , last_price, quantity = self.pos_sizing()
        if cash > last_price:
            if self.last_trade == None:
                news = self.get_news()
                print(news)
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type = "bracket",
                    take_profit_price= last_price*1.2,
                    stop_loss_price= last_price * .95
                )
                self.submit_order(order)
                self.last_trade = "buy"

broker = Alpaca(ALPACA_CREDS)  
strat = MLTrades(name='mlstrat', broker = broker, parameteres = {"symbol":"SPY","cash_at_risk":.5})

#Back Testing Functions
start_date = datetime(2023,12,15)
end_date = datetime(2023,12,31)

strat.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY","cash_at_risk":.5}
)