# Simulation controller for running investment strategies

# Import requirements
import pandas as pd
import ta

def run_strategy_simulation(data: pd.DataFrame, initial_investment: float, strategy: str) -> dict:
    """
    Run different investment strategies simulation
    
    Args:
        data (pandas.DataFrame): Stock price data
        initial_investment (float): Initial investment amount
        strategy (str): Strategy name to simulate
        
    Returns:
        dict: Dictionary containing simulation results
    """
    required_columns = ['Close']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Data missing required columns: {required_columns}")
        
    valid_strategies = ["Buy and Hold", "Moving Average Crossover", "RSI Strategy"]
    if strategy not in valid_strategies:
        raise ValueError(f"Invalid strategy. Choose from: {valid_strategies}")
    
    df = data.copy()

    results = {
        'strategy': strategy,
        'initial_investment': initial_investment,
        'start_date': df.index[0],
        'end_date': df.index[-1],
        'final_value': 0,
        'return_pct': 0,
        'annualized_return': 0,
        'buy_hold_return': 0,
        'trades': [],
        'portfolio_values': [],
        'dates': []
    }

    cash = initial_investment
    shares = 0.0
    portfolio_values = []
    dates = []
    trades = []
    
    if strategy == "Buy and Hold":
        start_price = df['Close'].iloc[0]
        shares = cash / start_price
        cash = 0
        
        trades.append({
            'date': df.index[0],
            'action': 'BUY',
            'price': start_price,
            'shares': shares,
            'value': shares * start_price
        })
        
        for date, row in df.iterrows():
            portfolio_value = shares * row['Close']
            portfolio_values.append(portfolio_value)
            dates.append(date)
        
        end_price = df['Close'].iloc[-1]
        trades.append({
            'date': df.index[-1],
            'action': 'SELL',
            'price': end_price,
            'shares': shares,
            'value': shares * end_price
        })

    elif strategy == "Moving Average Crossover":
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        for i, (date, row) in enumerate(df.iterrows()):
            if i < 50:
                portfolio_values.append(cash)
                dates.append(date)
                continue
            
            if row['MA20'] > row['MA50'] and cash > 0:
                shares = cash / row['Close']
                cash = 0
                trades.append({
                    'date': date,
                    'action': 'BUY',
                    'price': row['Close'],
                    'shares': shares,
                    'value': shares * row['Close']
                })
                
            elif row['MA20'] < row['MA50'] and shares > 0:
                cash = shares * row['Close']
                shares = 0
                trades.append({
                    'date': date,
                    'action': 'SELL',
                    'price': row['Close'],
                    'shares': shares,
                    'value': cash
                })
            
            portfolio_values.append(cash + shares * row['Close'])
            dates.append(date)

    elif strategy == "RSI Strategy":
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        
        for i, (date, row) in enumerate(df.iterrows()):
            if i < 14 or pd.isna(row['RSI']):
                portfolio_values.append(cash)
                dates.append(date)
                continue
            
            if row['RSI'] < 30 and cash > 0:
                shares = cash / row['Close']
                cash = 0
                trades.append({
                    'date': date,
                    'action': 'BUY',
                    'price': row['Close'],
                    'shares': shares,
                    'value': shares * row['Close']
                })
                
            elif row['RSI'] > 70 and shares > 0:
                cash = shares * row['Close']
                shares = 0
                trades.append({
                    'date': date,
                    'action': 'SELL',
                    'price': row['Close'],
                    'shares': shares,
                    'value': cash
                })
            
            portfolio_values.append(cash + shares * row['Close'])
            dates.append(date)

    final_value = cash + shares * df['Close'].iloc[-1]
    initial_price = df['Close'].iloc[0]
    final_price = df['Close'].iloc[-1]
    
    results.update({
        'final_value': final_value,
        'return_pct': ((final_value / initial_investment) - 1) * 100,
        'buy_hold_return': ((final_price / initial_price) - 1) * 100,
        'trades': trades,
        'portfolio_values': portfolio_values,
        'dates': dates
    })

    total_days = (df.index[-1] - df.index[0]).days
    if total_days > 0:
        years = total_days / 365.25
        annualized = ((final_value / initial_investment) ** (1/years) - 1) * 100
        results['annualized_return'] = round(annualized, 2)
    
    return results