#Replace the link with the actual URL of the stock price API you're using
#Adjust the return data['price'] line to match the structure of the API response
#Handle exceptions and errors appropriately to ensure robust error management

#Importing the req libs
import requests
from requests.exceptions import RequestException
from decimal import Decimal

api_key = "OWSXIPKVLK7APWRW"
def get_stock_price(stock_symbol):
    """Fetch the current price of a stock given its symbol using Alpha Vantage API.
    Args:
        stock_symbol (str): The stock symbol for which to fetch the price.
    Returns:
        Decimal: The current price of the stock as a Decimal, or None if there's an error.
    """
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Check if the expected keys are in the response
        if "Time Series (5min)" not in data:
            raise ValueError("Invalid response from Alpha Vantage API")
        
        # Get the most recent time entry
        latest_time = sorted(data["Time Series (5min)"].keys())[0]
        latest_data = data["Time Series (5min)"][latest_time]
        
        # Extract the closing price and convert it to Decimal
        stock_price = Decimal(latest_data["4. close"])
        return stock_price
    
    except (requests.RequestException, ValueError) as e:
        # Log the exception or handle it as needed
        print(f"Error fetching stock price: {e}")
        return None
    