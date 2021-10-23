from logging import debug
from flask import Flask
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os

from models import ExchangeDataAPI, DataStore, CoinbaseExchangeAPI, BinanceExchangeAPI

RETRIEVE_PRICES_DELAY = 2
SEND_DATA_DELAY = 2
CRYPTO_TICKERS = ['btc', 'eth']
PORT = 8001
ALLOWED_ORIGIN = 'http://localhost:3000'

# Scheduled function to recieve latest price data & update the data store. 
def retrieve_prices(ds, dataAPI):
    data_list, error_list = dataAPI.get_all_ticker_data()
    ds.update_data_store(data_list, error_list)


# Scheduled function to broadcast data from data store to the frontend
def send_data(ds, socketio):
    socketio.emit('crypto-price-data-stream', {'crypto-price-data': ds.retrieve_crypto_price_data()})
    socketio.emit('exchange-health-stream', {'exchange-health-data': ds.retrieve_exchange_health_data()})


def run_app():
    # Initialize data store
    ds = DataStore()

    # Setup crypto exchange data api
    binance_api_key = os.environ.get("BINANCE_API_KEY")
    binance_api_secret = os.environ.get("BINANCE_API_SECRET")
    cryptoExchangeDataAPI = ExchangeDataAPI([CoinbaseExchangeAPI(), BinanceExchangeAPI(api_key=binance_api_key, api_secret=binance_api_secret)], CRYPTO_TICKERS)
    cryptoExchangeDataAPI.connect()

    # Setup flask socket.io app
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGIN)

    # Setup background scheduling to run these services every 2 seconds. 
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(lambda: retrieve_prices(ds, cryptoExchangeDataAPI),'interval',seconds=RETRIEVE_PRICES_DELAY)
    scheduler.add_job(lambda: send_data(ds, socketio),'interval',seconds=SEND_DATA_DELAY)
    atexit.register(lambda: scheduler.shutdown())

    # Run app
    scheduler.start()
    socketio.run(app, port=PORT)

if __name__ == '__main__':
    run_app()
