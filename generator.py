import psutil
import os
import random
import numpy as np
import time
import logging
from flask import Flask
from threading import Thread
from flask import Flask, jsonify

p = psutil.Process(os.getpid())
p.cpu_affinity([0])
stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]

# Instead of API, we used flask!
app = Flask(__name__)


@app.route("/")
def get_data():
    data = generate_additional_data()
    return jsonify(data)


def generate_data():
    global data
    stock_symbol = random.choice(stocks)
    prev_price = 1000 
    dt = 1 
    mu = 0.0002 
    sigma = 0.01 

    price_change = np.exp((mu - 0.5 * sigma**2) * dt +
              sigma * np.sqrt(dt) * np.random.normal())
    opening_price = max(0, prev_price * price_change)
    closing_price = max(0, opening_price +
              round(random.normalvariate(0, 10), 2))
    high = max(opening_price, closing_price) + \
              round(abs(random.normalvariate(0, 5)), 2)
    low = min(opening_price, closing_price) - \
              round(abs(random.normalvariate(0, 5)), 2)
    volume = max(0, int(np.random.poisson(5000) *
              (1 + 0.1 * np.random.normal())))

    data = {
        "stock_symbol": stock_symbol,
        "opening_price": opening_price,
        "closing_price": closing_price,
        "high": high,
        "low": low,
        "volume": volume,
        "timestamp": time.time()
    }
    return data


def generate_additional_data():
    stock_symbol = random.choice(stocks)
    timestamp = time.time()
    data_types = ['order_book', 'news_sentiment',
           'market_data', 'economic_indicator']
    data_type = random.choice(data_types)

    if data_type == 'order_book':
        data = {
            "data_type": "order_book",
            "timestamp": timestamp,
            "stock_symbol": stock_symbol,
            "order_type": random.choice(['buy', 'sell']),
            "price": random.uniform(100, 1000),
            "quantity": random.randint(1, 100)
        }
    elif data_type == 'news_sentiment':
        data = {
            "data_type": "news_sentiment",
            "timestamp": timestamp,
            "stock_symbol": stock_symbol,
            "sentiment_score": random.uniform(-1, 1),
            "sentiment_magnitude": random.uniform(0, 1)
        }
    elif data_type == 'market_data':
        data = {
            "data_type": "market_data",
            "timestamp": timestamp,
            "stock_symbol": stock_symbol,
            "market_cap": random.uniform(1e9, 1e12),
            "pe_ratio": random.uniform(5, 30)
        }
    elif data_type == 'economic_indicator':
        data = {
            "data_type": "economic_indicator",
            "timestamp": timestamp,
            "indicator_name": "GDP Growth Rate",
            "value": random.uniform(-5, 5)
        }
    logging.info(f"Generated Data: {data}")
    return data

# Because of removing API (and replace with Flask): removed send_data and send_additional_data
def send_data_additional_data():
    while True:
        data = generate_additional_data()
        time.sleep(random.uniform(1, 5)) 


if __name__ == "__main__":
    try:
        thread = Thread(target=send_data_additional_data)
        thread.start()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
