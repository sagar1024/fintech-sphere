from django.test import TestCase

# Create your tests here.

import requests
import os

API_KEY = 'OWSXIPKVLK7APWRW'
def get_stock_price(stock_symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  #Raise an exception for HTTP errors
        data = response.json()

        #Extracting the latest stock price
        time_series = data.get("Time Series (5min)")
        if time_series:
            latest_timestamp = sorted(time_series.keys())[0]
            latest_data = time_series[latest_timestamp]
            stock_price = latest_data["1. open"]
            return stock_price
        else:
            print("No time series data found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

#Testing with Apple's stock symbol
stock_symbol = 'AAPL'
stock_price = get_stock_price(stock_symbol, API_KEY)

if stock_price:
    print(f"The current stock price of {stock_symbol} is: ${stock_price}")
else:
    print("Failed to fetch the stock price.")
