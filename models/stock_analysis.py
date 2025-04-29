# Stock Analysis model for technical analysis and trading signals

# Import requirements
import numpy as np
import ta  # Technical Analysis library

class StockAnalysis:
    """
    Enhanced Stock Analysis class with multiple indicators
    Analyzes stock data and generates recommendations
    """
    def __init__(self, data, risk_tolerance='moderate'):
        """
        Initialize the StockAnalysis with historical price data
        
        Args:
            data (pandas.DataFrame): Historical price data with OHLCV columns
            risk_tolerance (str): 'low', 'moderate', or 'high'
        """
        self.data = data.copy()
        self.risk_tolerance = risk_tolerance.lower()
        
        # Calculate common technical indicators
        self._calculate_indicators()
    
    def _calculate_indicators(self):
        """Calculate technical indicators for analysis"""
        # Moving averages
        self.data['MA20'] = self.data['Close'].rolling(window=20).mean()
        self.data['MA50'] = self.data['Close'].rolling(window=50).mean()
        self.data['MA200'] = self.data['Close'].rolling(window=200).mean()
        
        # Add RSI
        self.data['RSI'] = ta.momentum.RSIIndicator(self.data['Close']).rsi()
        
        # Add MACD
        macd = ta.trend.MACD(self.data['Close'])
        self.data['MACD'] = macd.macd()
        self.data['MACD_Signal'] = macd.macd_signal()
        self.data['MACD_Hist'] = macd.macd_diff()
        
        # Add Bollinger Bands
        bollinger = ta.volatility.BollingerBands(self.data['Close'])
        self.data['BB_Upper'] = bollinger.bollinger_hband()
        self.data['BB_Lower'] = bollinger.bollinger_lband()
        self.data['BB_Mid'] = bollinger.bollinger_mavg()
        
        # Volatility
        if len(self.data) > 1:
            self.data['Daily_Return'] = self.data['Close'].pct_change()
            self.data['Volatility'] = self.data['Daily_Return'].rolling(window=20).std() * np.sqrt(252)
    
    def generate_recommendation(self):
        """
        Generate trading recommendation based on technical indicators
        
        Returns:
            dict: Dictionary containing recommendation details
        """
        try:
            # Extract data for analysis
            last_price = self.data['Close'].iloc[-1].item()
            ma20 = self.data['MA20'].iloc[-1].item()
            ma50 = self.data['MA50'].iloc[-1].item()
            rsi = self.data['RSI'].iloc[-1].item()
            
            # More sophisticated recommendation system
            buy_signals = 0
            sell_signals = 0
            
            # MA signals
            if last_price > ma20 and ma20 > ma50:
                buy_signals += 1
            elif last_price < ma20 and ma20 < ma50:
                sell_signals += 1
            
            # RSI signals
            if rsi < 30:  # Oversold
                buy_signals += 1
            elif rsi > 70:  # Overbought
                sell_signals += 1
            
            # MACD signals
            if (self.data['MACD'].iloc[-1] > self.data['MACD_Signal'].iloc[-1] and 
                self.data['MACD'].iloc[-2] <= self.data['MACD_Signal'].iloc[-2]):
                buy_signals += 1
            elif (self.data['MACD'].iloc[-1] < self.data['MACD_Signal'].iloc[-1] and 
                  self.data['MACD'].iloc[-2] >= self.data['MACD_Signal'].iloc[-2]):
                sell_signals += 1
            
            # Generate final recommendation based on signals
            if buy_signals > sell_signals and buy_signals >= 2:
                action = "BUY"
                conviction = "HIGH" if buy_signals >= 3 else "MEDIUM"
                stop_loss_pct = 0.95 if self.risk_tolerance == 'high' else 0.97
                target_pct = 1.10 if self.risk_tolerance == 'high' else 1.05
            elif sell_signals > buy_signals and sell_signals >= 2:
                action = "SELL"
                conviction = "HIGH" if sell_signals >= 3 else "MEDIUM"
                stop_loss_pct = 1.05 if self.risk_tolerance == 'high' else 1.03
                target_pct = 0.90 if self.risk_tolerance == 'high' else 0.95
            else:
                action = "HOLD"
                conviction = "MEDIUM"
                stop_loss_pct = 0.97
                target_pct = 1.03
            
            recommendation = {
                'action': action,
                'conviction': conviction,
                'signals': {
                    'buy_signals': buy_signals,
                    'sell_signals': sell_signals
                },
                'price_targets': {
                    'entry': round(last_price, 2),
                    'stop_loss': round(last_price * stop_loss_pct, 2),
                    'target': round(last_price * target_pct, 2)
                },
                'indicators': {
                    'ma20': round(ma20, 2),
                    'ma50': round(ma50, 2),
                    'rsi': round(rsi, 2),
                    'macd': round(self.data['MACD'].iloc[-1], 2),
                    'macd_signal': round(self.data['MACD_Signal'].iloc[-1], 2)
                }
            }
        except Exception as e:
            # Fallback with simple recommendation if technical analysis fails
            last_price = self.data['Close'].iloc[-1].item()
            recommendation = {
                'action': "HOLD",
                'conviction': "LOW",
                'signals': {
                    'buy_signals': 0,
                    'sell_signals': 0
                },
                'price_targets': {
                    'entry': round(last_price, 2)
                },
                'indicators': {
                    'error': str(e)
                }
            }
        
        return recommendation

    def get_summary_statistics(self):
        """
        Calculate summary statistics for the stock
        
        Returns:
            dict: Dictionary containing summary statistics
        """
        # Calculating more comprehensive statistics
        try:
            last_price = self.data['Close'].iloc[-1].item()
            
            # Calculate returns over different time periods
            returns = {}
            periods = {
                '1w': 5,
                '1m': 21,
                '3m': 63,
                '6m': 126,
                '1y': 252
            }
            
            for period_name, days in periods.items():
                if len(self.data) > days:
                    period_return = (last_price / self.data['Close'].iloc[-min(days, len(self.data))]) - 1
                    returns[period_name] = round(period_return * 100, 2)
                else:
                    returns[period_name] = None
            
            # Calculate volatility
            if 'Volatility' in self.data.columns and not self.data['Volatility'].iloc[-1] is None:
                volatility = self.data['Volatility'].iloc[-1].item() * 100
            else:
                volatility = None
            
            # 52-week high/low
            if len(self.data) >= 252:
                year_data = self.data.iloc[-252:]
                high_52w = year_data['High'].max().item()
                low_52w = year_data['Low'].min().item()
                from_high = (last_price / high_52w - 1) * 100
                from_low = (last_price / low_52w - 1) * 100
            else:
                high_52w = self.data['High'].max().item()
                low_52w = self.data['Low'].min().item()
                from_high = (last_price / high_52w - 1) * 100
                from_low = (last_price / low_52w - 1) * 100
            
            summary = {
                'current_price': round(last_price, 2),
                'trading_days': len(self.data),
                'returns': returns,
                'volatility': round(volatility, 2) if volatility is not None else None,
                '52w_high': round(high_52w, 2),
                '52w_low': round(low_52w, 2),
                'from_52w_high': round(from_high, 2),
                'from_52w_low': round(from_low, 2)
            }
            
        except Exception as e:
            # Simple fallback if statistics calculation fails
            last_price = self.data['Close'].iloc[-1].item()
            summary = {
                'current_price': round(last_price, 2),
                'trading_days': len(self.data),
                'error': str(e)
            }
            
        return summary