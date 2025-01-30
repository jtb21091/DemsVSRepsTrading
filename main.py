import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from datetime import datetime

# Define stock tickers and colors
stocks = {"NANC": "blue", "KRUZ": "red"}

# Fetch full historical stock data (2 years)
historical_data = {}
for stock in stocks:
    ticker = yf.Ticker(stock)
    historical_data[stock] = ticker.history(period="2y")  # Fetch 2 years of historical data

# Extract historical prices and timestamps
price_data = {stock: list(historical_data[stock]["Close"].dropna()) for stock in stocks}
time_data = {stock: list(historical_data[stock].index) for stock in stocks}  # Keep datetime format

# Function to fetch latest stock prices
def fetch_prices():
    prices = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        current_price = ticker.history(period="1d")["Close"].iloc[-1]
        prices[stock] = current_price
    return prices

# Function to update the plot in real-time
def update(frame):
    global time_data, price_data
    
    prices = fetch_prices()
    current_time = datetime.now()

    for stock in stocks:
        price_data[stock].append(prices[stock])
        time_data[stock].append(current_time)

    # Clear and replot
    ax.clear()
    for stock, color in stocks.items():
        ax.plot(time_data[stock], price_data[stock], label=stock, color=color)

    # Formatting
    ax.set_title("Real-Time & Historical Stock Price Tracker")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    plt.grid(True)

    # Format x-axis to only show Month & Year (No timestamps)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))  # Format as 'Month Year'
    plt.xticks(rotation=45)  # Rotate for better readability

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Use animation to refresh every 5 seconds
ani = animation.FuncAnimation(fig, update, interval=5000, cache_frame_data=False)

plt.show()
