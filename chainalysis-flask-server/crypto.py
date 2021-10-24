from flask import Flask
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from models import ExchangeDataAPI, DataStore, CoinbaseExchangeAPI, BinanceExchangeAPI
from threading import Lock

RETRIEVE_PRICES_DELAY = 2
SEND_DATA_DELAY = 2
CRYPTO_TICKERS = ['btc', 'eth']
PORT = 8001
ALLOWED_ORIGIN = 'http://localhost:3000'


# Setup flask socket.io app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGIN, async_mode='eventlet')
thread = None
thread_lock = Lock()

# Initialize data store
ds = DataStore()


# Scheduled function to receive latest price data & update the data store. 
def retrieve_prices(dataAPI):
    global ds
    
    data_list, error_list = dataAPI.get_all_ticker_data()
    ds.update_data_store(data_list, error_list)


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(send_data_thread)


def send_data_thread():
    global ds
    while True:
        socketio.sleep(2)
        socketio.emit('crypto-price-data-stream', {'crypto-price-data': ds.retrieve_crypto_price_data()})
        socketio.emit('exchange-health-stream', {'exchange-health-data': ds.retrieve_exchange_health_data()})


def run_app():
    # Setup crypto exchange data api
    cryptoExchangeDataAPI = ExchangeDataAPI([CoinbaseExchangeAPI(), BinanceExchangeAPI()], CRYPTO_TICKERS)
    cryptoExchangeDataAPI.connect()

    # Setup background scheduling to run these services every 2 seconds.
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(lambda: retrieve_prices(ds, cryptoExchangeDataAPI), 'interval', seconds=RETRIEVE_PRICES_DELAY)
    atexit.register(lambda: scheduler.shutdown())

    # Run app
    scheduler.start()
    socketio.run(app, port=PORT, host='0.0.0.0')

if __name__ == '__main__':
    run_app()
