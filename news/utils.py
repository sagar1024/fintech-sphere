import requests
from requests.exceptions import RequestException
from nltk.sentiment import SentimentIntensityAnalyzer
from decimal import Decimal
import datetime

api_key = "OWSXIPKVLK7APWRW"

def fetch_news(stock_symbol):
    """Fetch financial news for a given stock symbol using Alpha Vantage API."""
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock_symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('feed', [])
    except (RequestException, ValueError) as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_sentiment(headline):
    """Analyze sentiment of the news headline using NLTK's VADER sentiment analyzer."""
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(headline)
    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
    