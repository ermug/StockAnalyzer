
# Stock Analysis Tool

A powerful desktop application built with Python and PyQt5 for performing technical stock analysis and investment strategy simulations. It utilizes real-time market data, financial indicators, and visualization tools to offer recommendations and backtest investment strategies.

## Features

- Real-Time Stock Analysis with support for MA, RSI, MACD, and Bollinger Bands
- Investment Recommendations based on technical signals and risk tolerance
- Interactive UI with multiple tabs for charts, indicators, and simulation
- Strategy Backtesting (Buy & Hold, MA Crossover, RSI Strategy)
- Candlestick & Line Charts using Matplotlib and mplfinance
- Custom Date Ranges and simulation parameters
- Risk Profile Settings (Low, Moderate, High)
- Historical Ticker Management

## Project Structure

```
stock_analysis/
│
├── main.py                  # Entry point - launches the PyQt5 app
├── requirements.txt         # Required Python packages
│
├── models/
│   ├── __init__.py
│   └── stock_analysis.py    # Stock data processing and analysis logic
│
├── views/
│   ├── __init__.py
│   ├── main_window.py       # Main application window
│   ├── analysis_tab.py      # Recommendation & summary tab
│   ├── charts_tab.py        # Candlestick and line chart tab
│   ├── indicators_tab.py    # RSI, MACD visualization tab
│   └── simulation_tab.py    # Investment simulation tools
│
├── controllers/
│   ├── __init__.py
│   ├── data_controller.py   # Data download and preprocessing
│   └── simulation.py        # Backtesting logic for investment strategies
│
└── utils/
    ├── __init__.py
    ├── charting.py          # Chart rendering utilities
    └── styles.py            # UI themes and palette settings
```

## Installation

1. Clone the Repository
   ```bash
   git clone (insert repo)
   cd stock_analysis
   ```

2. Create a Virtual Environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install Requirements
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Application
   ```bash
   python main.py
   ```

## Requirements

- Python 3.8+
- PyQt5
- matplotlib
- yfinance
- pandas
- numpy
- mplfinance
- ta (Technical Analysis library)