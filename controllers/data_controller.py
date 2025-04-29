# Data controller for fetching and processing stock data

# Import requirements
import pandas as pd
import yfinance as yf

def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch historical stock data from Yahoo Finance
    Args:
        ticker (str): Stock ticker symbol
        period (str): Time period to fetch (e.g., '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        interval (str): Data interval (e.g., '1d', '1wk', '1mo')
        
    Returns:
        pandas.DataFrame: Historical stock data or None if fetch fails
        fetches may fail on invalid or delisted tickers
    """
    try:
        # Fetch historical stock data
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            return None
        # Ensure the index is a DatetimeIndex
        data.index = pd.to_datetime(data.index)
        # Process the data
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        # Clean data
        data = data.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'])
        data = data.astype({'Open': 'float64', 'High': 'float64', 
                            'Low': 'float64', 'Close': 'float64', 'Volume': 'float64'})
        return data
    # Usually throws this on invalid/delisted tickers
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def get_period_mapping():
    """
    Get mapping from UI display text to yfinance period strings
    Returns:
        dict: Mapping from display text to yfinance period string
    """
    return {
        "1 Month": "1mo", 
        "3 Months": "3mo", 
        "6 Months": "6mo", 
        "1 Year": "1y", 
        "2 Years": "2y", 
        "5 Years": "5y", 
        "Max": "max"
    }