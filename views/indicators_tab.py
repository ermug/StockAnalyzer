"""
Technical indicators tab for displaying MACD, RSI, etc.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from utils.charting import MplCanvas

class IndicatorsTab(QWidget):
    """Tab for displaying technical indicators"""


    def __init__(self):
        """Initialize the indicators tab"""
        super().__init__()
        
        # Setup layout
        self.layout = QVBoxLayout(self)
        
        # MACD Chart
        self.macd_canvas = MplCanvas(self, width=8, height=3, dpi=100)
        self.layout.addWidget(self.macd_canvas)
        
        # RSI Chart
        self.rsi_canvas = MplCanvas(self, width=8, height=3, dpi=100)
        self.layout.addWidget(self.rsi_canvas)
    
    def update_indicators(self, data, analysis):
        """
        Update the technical indicator charts
        
        Args:
            data (pandas.DataFrame): Stock price data
            analysis (StockAnalysis): Stock analysis instance
        """
        # Plot MACD
        self.macd_canvas.ax.clear()
        if 'MACD' in analysis.data.columns and 'MACD_Signal' in analysis.data.columns:
            self.macd_canvas.ax.plot(data.index, analysis.data['MACD'], color='blue', label='MACD')
            self.macd_canvas.ax.plot(data.index, analysis.data['MACD_Signal'], color='red', label='Signal')
            
            # Plot histogram as bar chart
            if 'MACD_Hist' in analysis.data.columns:
                hist = analysis.data['MACD_Hist']
                self.macd_canvas.ax.bar(data.index, hist, color=['green' if x >= 0 else 'red' for x in hist], 
                                       label='Histogram', alpha=0.5, width=1)
        
        self.macd_canvas.ax.set_title('MACD Indicator', fontsize=14)
        self.macd_canvas.ax.legend()
        self.macd_canvas.ax.grid(True, alpha=0.3)
        self.macd_canvas.fig.autofmt_xdate()
        self.macd_canvas.draw()
        
        # Plot RSI
        self.rsi_canvas.ax.clear()
        if 'RSI' in analysis.data.columns:
            self.rsi_canvas.ax.plot(data.index, analysis.data['RSI'], color='blue', label='RSI')
            
            # Add overbought/oversold lines
            self.rsi_canvas.ax.axhline(y=70, color='r', linestyle='--', alpha=0.5)
            self.rsi_canvas.ax.axhline(y=30, color='g', linestyle='--', alpha=0.5)
            self.rsi_canvas.ax.fill_between(data.index, 70, 100, alpha=0.1, color='red')
            self.rsi_canvas.ax.fill_between(data.index, 0, 30, alpha=0.1, color='green')
            
            # Set y-axis limits for RSI
            self.rsi_canvas.ax.set_ylim(0, 100)
        
        self.rsi_canvas.ax.set_title('Relative Strength Index (RSI)', fontsize=14)
        self.rsi_canvas.ax.legend()
        self.rsi_canvas.ax.grid(True, alpha=0.3)
        self.rsi_canvas.fig.autofmt_xdate()
        self.rsi_canvas.draw()
