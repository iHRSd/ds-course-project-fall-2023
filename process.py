import json 
import pandas as pd 
import threading 
import time 
import requests 
from kafka import KafkaConsumer
 
consumer = KafkaConsumer(
    'app',  # Replace with the actual topic name
    bootstrap_servers=['your_kafka_broker_1:9092', 'your_kafka_broker_2:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)

for message in consumer:
    print("Received message: ", message.value)
    data = message.value.decode("utf-8")
    df = pd.read_json(data)
    print("Received data: ", df.head())# Assuming data is in the message value
    # Extract relevant financial data from 'data' (e.g., closing prices, timestamps)
    # Calculate indicators using appropriate functions (MA, EMA, RSI)
    # Handle results (store, visualize, send to other systems)
 
# DataFrame to store the processed data 
processed_data_df = pf.DataFrame() 
 
def select_appropriate_field(data): 
    if data['data_type'] == 'order_book': 
        return data['price'] 
    elif data['data_type'] == 'market_data': 
        return data['market_cap'] 
    # Add more conditions if other data types are relevant 
    else: 
        return None

def moving_average(series, periods=20): 
    """ 
    Calculate the Moving Average (MA) for the given data. 
    :param series: Pandas Series with numerical data. 
    :param periods: Number of periods over which to calculate the average. 
    :return: Pandas Series containing the moving averages. 
    """ 
    return series.rolling(window=periods).mean() 
 
def exponential_moving_average(series, periods=20): 
    """ 
    Calculate the Exponential Moving Average (EMA) for the given data. 
    :param series: Pandas Series with numerical data. 
    :param periods: Number of periods over which to calculate the EMA. 
    :return: Pandas Series containing the exponential moving averages. 
    """ 
    return series.ewm(span=periods, adjust=False).mean() 
 
def relative_strength_index(series, periods=14): 
    """ 
    Calculate the Relative Strength Index (RSI) for the given data. 
    :param series: Pandas Series with numerical data. 
    :param periods: Number of periods over which to calculate the RSI. 
    :return: Pandas Series containing the RSI values. 
    """ 
    delta = series.diff() 
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean() 
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean() 
 
    rs = gain / loss 
    rsi = 100 - (100 / (1 + rs)) 
 
    return rsi

def stream_processed_data(): 
    series_dict = { 
        'order_book': pd.Series(), 
        'market_data': pd.Series(), 
        # Add more as needed 
    } 
 
    while True: 
        dp = df.read_json(data) 
        data = message.value.decode("utf-8") 
 
        data_type = data.get('data_type') 
        if data_type in series_dict: 
            value = select_appropriate_field(data_dict) 
            if value is not None: 
                series = series_dict[data_type] 
                # Concatenate new value to the series 
                new_series = pd.Series([value]) 
                series = pd.concat([series, new_series]).dropna() 
                series_dict[data_type] = series 
 
                # Perform calculations 
                ma = moving_average(series) 
                ema = exponential_moving_average(series) 
                rsi = relative_strength_index(series) 
 
                # Prepare and send data 
                processed_data = { 
                    'data_type': data_type, 
                    'MA': ma.iloc[-1] if not ma.empty else None, 
                    'EMA': ema.iloc[-1] if not ema.empty else None, 
                    'RSI': rsi.iloc[-1] if not rsi.empty else None 
                } 

                # Send data to port 9092 (broker)
                try: 
                    print(f"processed_data : {processed_data}")
                    producer.send("app", value="MA, EMA ,RSI".encode("utf-8"))
                except Exception as e: 
                    print(f"Error sending data: {e}") 

