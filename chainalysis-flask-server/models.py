from abc import ABC, abstractmethod
import cbpro
from binance.client import Client


# Abstract class for easily adding in more exchange APIs
class ExchangeAPI(ABC):
    @abstractmethod
    # Connect to crypto API
    def establish_connection(self):
        pass

    @abstractmethod
    # Get ticker price data aand return an ExchangeData object
    def get_ticker_data(self, ticker):
        pass

    @abstractmethod
    # Get exchange name
    def get_name(self):
        pass


class CoinbaseExchangeAPI(ExchangeAPI):
    name = "Coinbase"

    ticker_map = {
        "btc": "BTC-USD",
        "eth": "ETH-USD"
    }

    def establish_connection(self):
        self.public_client = cbpro.PublicClient()

    def get_ticker_data(self, ticker):
        ticker_info = self.public_client.get_product_ticker(product_id=self.ticker_map[ticker])
        if (type(ticker_info) is dict and 'ask' in ticker_info and 'bid' in ticker_info):
            buy_price = ticker_info['ask'];
            sell_price = ticker_info['bid'];
            data = ExchangeData(self.name, ticker, buy_price, sell_price)
            return ExchangeResponse(error=False, exchangeData=data)
        else:
            return ExchangeResponse(error=True, exchangeData=None)

    def get_name(self):
        return self.name


class BinanceExchangeAPI(ExchangeAPI):
    name = "Binance"

    ticker_map = {
        "btc": "BTCUSDT",
        "eth": "ETHUSDT"
    }

    def establish_connection(self):
        self.client = Client()

    def get_ticker_data(self, ticker):
        ticker_info = self.client.get_ticker(symbol=self.ticker_map[ticker])
        if (type(ticker_info) is dict and 'askPrice' in ticker_info and 'bidPrice' in ticker_info):
            buy_price = ticker_info['askPrice'];
            sell_price = ticker_info['bidPrice'];
            data = ExchangeData(self.name, ticker, buy_price, sell_price)
            return ExchangeResponse(error=False, exchangeData=data)
        else:
            return ExchangeResponse(error=True, exchangeData=None)

    def get_name(self):
        return self.name


# For error handling
class ExchangeResponse:
    def __init__(self, error, exchangeData):
        self.error = error
        self.exchangeData = exchangeData


# Standardized data model for price data from any exchange API.
class ExchangeData:
    def __init__(self, exchange, ticker, buy, sell):
        self.exchange = exchange
        self.ticker = ticker
        self.buy = buy
        self.sell = sell

    def __str__(self):
        return self.exchange + ": " + self.ticker + ", buy: " + str(self.buy) + ", sell: " + str(self.sell)

    def __repr__(self):
        return str(self)


class ExchangeDataAPI:
    def __init__(self, exchanges, tickers):
        self.exchanges = exchanges
        self.tickers = tickers

    def connect(self):
        for exchange in self.exchanges:
            exchange.establish_connection();

    def get_all_ticker_data(self):
        dataList = []
        exchangeErrorList = set()
        for ticker in self.tickers: 
            for exchange in self.exchanges:
                response = exchange.get_ticker_data(ticker);
                if (response.error == False):
                    dataList.append(response.exchangeData)
                else:
                    exchangeErrorList.add(exchange.get_name())
        return dataList, list(exchangeErrorList);


class DataStore:
    __store = {
        "crypto_price_data": {},
        "exchange_health": {},
    }

    def update_data_store(self, dataList, errorList):
        # Reset store when new data is coming in. 
        crypto_price_data = {}
        # Choose best buy & sell exchanges
        for data in dataList:
            if (data.ticker not in crypto_price_data):
                crypto_price_data[data.ticker] = {
                    "best_buy_exchange": data.exchange,
                    "best_sell_exchange": data.exchange,
                    "best_buy_price": data.buy,
                    "best_sell_price": data.sell, 
                }
            else:
                if (data.buy < crypto_price_data[data.ticker]['best_buy_price']):
                    crypto_price_data[data.ticker]['best_buy_price'] = data.buy
                    crypto_price_data[data.ticker]['best_buy_exchange'] = data.exchange
                if (data.sell > crypto_price_data[data.ticker]['best_sell_price']):
                    crypto_price_data[data.ticker]['best_sell_price'] = data.sell
                    crypto_price_data[data.ticker]['best_sell_exchange'] = data.exchange
        self.__store['crypto_price_data'] = crypto_price_data

        exchange_health = {}
        for errorExchange in errorList:
            exchange_health[errorExchange] = {"error": True}
        self.__store['exchange_health'] = exchange_health
            

    def retrieve_crypto_price_data(self):
        return self.__store["crypto_price_data"]

    def retrieve_exchange_health_data(self):
        return self.__store["exchange_health"]
