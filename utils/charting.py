# Charting utilities for the stock analysis application

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):
    """
    A custom matplotlib canvas for embedding charts in the PyQt5 app
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """
        Initialize a new matplotlib figure canvas
        
        Args:
            parent: Parent widget
            width: Width in inches
            height: Height in inches
            dpi: Dots per inch
        """
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        
def add_selected_indicators(ax, data, show_ma20=False, show_ma50=False, 
                           show_ma200=False, show_bollinger=False):
    """
    Add selected technical indicators to the chart
    
    Args:
        ax: Matplotlib axis
        data: Pandas DataFrame with indicator columns
        show_ma20: Whether to show 20-day moving average
        show_ma50: Whether to show 50-day moving average
        show_ma200: Whether to show 200-day moving average
        show_bollinger: Whether to show Bollinger Bands
    """
    if data is None:
        return
        
    # Add the selected indicators
    if show_ma20 and 'MA20' in data.columns:
        ax.plot(data.index, data['MA20'], color='blue', linestyle='--', label='MA20')
        
    if show_ma50 and 'MA50' in data.columns:
        ax.plot(data.index, data['MA50'], color='red', linestyle='--', label='MA50')
        
    if show_ma200 and 'MA200' in data.columns:
        ax.plot(data.index, data['MA200'], color='purple', linestyle='--', label='MA200')
        
    if show_bollinger and 'BB_Upper' in data.columns:
        ax.plot(data.index, data['BB_Upper'], color='green', linestyle=':', label='BB Upper')
        ax.plot(data.index, data['BB_Mid'], color='green', linestyle='-', alpha=0.5, label='BB Mid')
        ax.plot(data.index, data['BB_Lower'], color='green', linestyle=':', label='BB Lower')
        ax.fill_between(data.index, data['BB_Upper'], data['BB_Lower'], alpha=0.1, color='green')