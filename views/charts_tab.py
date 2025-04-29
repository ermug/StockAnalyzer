"""
Charts tab for displaying stock price charts
"""
import matplotlib
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import mplfinance as mpf

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QCheckBox, QPushButton
)

from utils.charting import MplCanvas, add_selected_indicators

class ChartsTab(QWidget):
    """Tab for displaying stock price charts"""
    
    def __init__(self):
        """Initialize the charts tab"""
        super().__init__()
        
        # Setup layout
        self.layout = QVBoxLayout(self)
        
        # Line chart
        self.line_canvas = MplCanvas(self, width=8, height=3, dpi=100)
        self.line_toolbar = NavigationToolbar(self.line_canvas, self)
        self.layout.addWidget(self.line_toolbar)
        self.layout.addWidget(self.line_canvas)
        
        # Add indicator selection
        indicator_group = QGroupBox("Technical Indicators")
        indicator_layout = QHBoxLayout()
        
        self.show_ma20 = QCheckBox("20-day MA")
        self.show_ma50 = QCheckBox("50-day MA")
        self.show_ma200 = QCheckBox("200-day MA")
        self.show_bollinger = QCheckBox("Bollinger Bands")
        
        self.show_ma20.setChecked(True)
        self.show_ma50.setChecked(True)
        
        indicator_layout.addWidget(self.show_ma20)
        indicator_layout.addWidget(self.show_ma50)
        indicator_layout.addWidget(self.show_ma200)
        indicator_layout.addWidget(self.show_bollinger)
        indicator_layout.addStretch()
        
        # Add apply button
        self.apply_indicators_button = QPushButton("Apply")
        indicator_layout.addWidget(self.apply_indicators_button)
        
        indicator_group.setLayout(indicator_layout)
        self.layout.addWidget(indicator_group)
        
        # Candlestick chart
        self.candle_canvas = MplCanvas(self, width=8, height=4, dpi=100)
        self.candle_toolbar = NavigationToolbar(self.candle_canvas, self)
        self.layout.addWidget(self.candle_toolbar)
        self.layout.addWidget(self.candle_canvas)
    
    def update_charts(self, ticker, data, analysis):
        """
        Update the charts with new data
        
        Args:
            ticker (str): Stock ticker symbol
            data (pandas.DataFrame): Stock price data
            analysis (StockAnalysis): Stock analysis instance
        """
        # Plot the line chart for closing prices with selected indicators
        self.line_canvas.ax.clear()
        
        # Plot the main price line
        self.line_canvas.ax.plot(data.index, data['Close'], label="Close Price", color='blue', linewidth=2)
        
        # Add volume as a bar chart at the bottom (with a separate y-axis)
        volume_ax = self.line_canvas.ax.twinx()
        volume_ax.bar(data.index, data['Volume'], alpha=0.3, color='gray', label='Volume')
        volume_ax.set_ylabel('Volume')
        
        # Format y-axis to be more readable for volume
        volume_ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )
        
        # Add selected indicators
        add_selected_indicators(
            self.line_canvas.ax, 
            analysis.data,
            self.show_ma20.isChecked(),
            self.show_ma50.isChecked(),
            self.show_ma200.isChecked(),
            self.show_bollinger.isChecked()
        )
        
        # Set title and labels
        self.line_canvas.ax.set_title(f"{ticker} Price Chart", fontsize=16)
        self.line_canvas.ax.set_xlabel("Date", fontsize=12)
        self.line_canvas.ax.set_ylabel("Price ($)", fontsize=12)
        self.line_canvas.ax.grid(True, alpha=0.3)
        self.line_canvas.ax.legend()
        
        # Format the date axis
        self.line_canvas.fig.autofmt_xdate()
        
        # Update the canvas
        self.line_canvas.draw()
        
        # Plot the candlestick chart
        self.candle_canvas.ax.clear()
        
        # Create a subplot for volume
        ax_vol = self.candle_canvas.ax.twinx()
        
        # Plot the candlestick chart with mplfinance
        mpf.plot(data, type='candle', ax=self.candle_canvas.ax, style='yahoo',
                 datetime_format='%Y-%m-%d', volume=ax_vol, show_nontrading=False)
        
        # Add selected indicators if available
        if hasattr(analysis.data, 'MA20') and self.show_ma20.isChecked():
            self.candle_canvas.ax.plot(data.index, analysis.data['MA20'], color='blue', 
                                     linestyle='--', linewidth=1, label='MA20')
        
        if hasattr(analysis.data, 'MA50') and self.show_ma50.isChecked():
            self.candle_canvas.ax.plot(data.index, analysis.data['MA50'], color='red', 
                                     linestyle='--', linewidth=1, label='MA50')
        
        if hasattr(analysis.data, 'MA200') and self.show_ma200.isChecked():
            self.candle_canvas.ax.plot(data.index, analysis.data['MA200'], color='purple', 
                                     linestyle='--', linewidth=1, label='MA200')
        
        # Add legend and title
        self.candle_canvas.ax.set_title(f"{ticker} Candlestick Chart", fontsize=16)
        self.candle_canvas.ax.legend()
        self.candle_canvas.fig.autofmt_xdate()
        self.candle_canvas.draw()