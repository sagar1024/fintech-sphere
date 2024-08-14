from django.shortcuts import render
from .forms import TickerForm
from .utils import fetch_news, analyze_sentiment
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64
from decimal import Decimal

# def news_analysis_view(request):
#     news_data = []
#     form = TickerForm()
#     graph = None  #Initializing graph to None
    
#     if request.method == 'POST':
#         form = TickerForm(request.POST)
#         if form.is_valid():
#             stock_symbol = form.cleaned_data['ticker']
#             news_feed = fetch_news(stock_symbol)
#             for news in news_feed:
#                 headline = news['title']
#                 published_at = datetime.strptime(news['time_published'], '%Y%m%dT%H%M%S')
#                 if published_at >= datetime.now() - timedelta(days=10):  # Filter news within the last 10 days
#                     sentiment = analyze_sentiment(headline)
#                     impact = Decimal('0.05') if sentiment == 'Positive' else Decimal('-0.05') if sentiment == 'Negative' else Decimal('0.00')
#                     news_data.append({
#                         'headline': headline,
#                         'published_at': published_at,
#                         'sentiment': sentiment,
#                         'impact_on_stock': impact
#                     })
#             #Generating a stock price graph with impact
#             graph = generate_stock_price_graph(stock_symbol, news_data)

#     return render(request, 'news/news.html', {'form': form, 'news_data': news_data, 'graph': graph})

def news_analysis_view(request):
    news_data = []
    form = TickerForm()
    graph = None  #Initializing graph to None
    
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            stock_symbol = form.cleaned_data['ticker']
            news_feed = fetch_news(stock_symbol)
            
            #Limit to 5 news items
            news_count = 0
            for news in news_feed:
                if news_count >= 10:
                    break
                
                headline = news['title']
                published_at = datetime.strptime(news['time_published'], '%Y%m%dT%H%M%S')
                if published_at >= datetime.now() - timedelta(days=10):  # Filter news within the last 10 days
                    sentiment = analyze_sentiment(headline)
                    impact = Decimal('0.05') if sentiment == 'Positive' else Decimal('-0.05') if sentiment == 'Negative' else Decimal('0.00')
                    news_data.append({
                        'headline': headline,
                        'published_at': published_at,
                        'sentiment': sentiment,
                        'impact_on_stock': impact
                    })
                    news_count += 1

            #Generating a stock price graph with impact
            graph = generate_stock_price_graph(stock_symbol, news_data)

    return render(request, 'news/news.html', {'form': form, 'news_data': news_data, 'graph': graph})

def generate_stock_price_graph(stock_symbol, news_data):
    #Mocking stock prices for demonstration (replace with real data)
    dates = [datetime.now() - timedelta(days=i) for i in range(10, 0, -1)]
    prices = [100 + (i * 0.5) for i in range(10)]  # Mock prices

    #Applying the sentiment impact to the stock prices
    for news in news_data:
        for i, date in enumerate(dates):
            if date.date() == news['published_at'].date():
                impact_on_stock = float(news['impact_on_stock'])
                prices[i] += prices[i] * impact_on_stock

    #Predict future prices
    future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 11)]
    last_price = prices[-1]
    future_prices = [last_price * (1 + 0.01 * i) for i in range(1, 11)]  # Simple prediction model

    #Combining past and future data
    all_dates = dates + future_dates
    all_prices = prices + future_prices

    #Plotting the graph
    plt.figure(figsize=(8, 5))
    plt.plot(all_dates, all_prices, marker='o', linestyle='-', linewidth=2, markersize=8, color='red')
    
    #Highlight the predicted part
    plt.plot(future_dates, future_prices, marker='o', linestyle='--', linewidth=2, markersize=8, color='black', label='Predicted')

    plt.title(f"Stock Price Prediction for {stock_symbol} Over Next 10 Days", fontsize=16, fontweight='bold', color='black')
    plt.xlabel("Date", fontsize=14, fontweight='bold', color='black')
    plt.ylabel("Stock Price", fontsize=14, fontweight='bold', color='black')
    plt.xticks(rotation=45, fontsize=12, color='black')
    plt.yticks(fontsize=12, color='black')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper left', fontsize=12)
    plt.tight_layout()

    #Adding a background color to the plot
    plt.gcf().set_facecolor('white')
    plt.gca().set_facecolor('lightgray')
    
    #Converting plot to image for displaying in the template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graph = base64.b64encode(image_png).decode('utf-8')
    return graph
