"""
Investment simulation tab for backtesting strategies
"""
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QDateEdit,
    QComboBox, QDoubleSpinBox, QPushButton, QTextEdit
)
from PyQt5.QtCore import QDate
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from utils.charting import MplCanvas
from controllers.simulation import run_strategy_simulation

class SimulationTab(QWidget):
    """Tab for running investment simulations"""
    
    def __init__(self):
        """Initialize the simulation tab"""
        super().__init__()
        
        # Data storage
        self.data = None
        
        # Setup layout
        self.layout = QVBoxLayout(self)
        
        # Create a form layout for simulation parameters
        sim_form = QGridLayout()
        
        # Date inputs with calendar picker
        self.start_date_label = QLabel("Start Date:")
        self.start_date_picker = QDateEdit()
        self.start_date_picker.setCalendarPopup(True)
        self.start_date_picker.setDate(QDate.currentDate().addMonths(-6))
        
        self.end_date_label = QLabel("End Date:")
        self.end_date_picker = QDateEdit()
        self.end_date_picker.setCalendarPopup(True)
        self.end_date_picker.setDate(QDate.currentDate())
        
        # Investment amount with spinner
        self.investment_label = QLabel("Investment Amount ($):")
        self.investment_input = QDoubleSpinBox()
        self.investment_input.setRange(100, 1000000)
        self.investment_input.setValue(10000)
        self.investment_input.setPrefix("$")
        self.investment_input.setSingleStep(1000)
        
        # Strategy selection
        self.strategy_label = QLabel("Strategy:")
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["Buy and Hold", "Moving Average Crossover", "RSI Strategy"])
        
        # Add widgets to form
        sim_form.addWidget(self.start_date_label, 0, 0)
        sim_form.addWidget(self.start_date_picker, 0, 1)
        sim_form.addWidget(self.end_date_label, 0, 2)
        sim_form.addWidget(self.end_date_picker, 0, 3)
        sim_form.addWidget(self.investment_label, 1, 0)
        sim_form.addWidget(self.investment_input, 1, 1)
        sim_form.addWidget(self.strategy_label, 1, 2)
        sim_form.addWidget(self.strategy_combo, 1, 3)
        
        # Simulate button
        self.simulate_button = QPushButton("Run Simulation")
        sim_form.addWidget(self.simulate_button, 2, 3)
        
        # Add form to layout
        self.layout.addLayout(sim_form)
        
        # Results area
        self.simulation_results = QTextEdit()
        self.simulation_results.setReadOnly(True)
        self.layout.addWidget(self.simulation_results)
        
        # Simulation chart
        self.simulation_canvas = MplCanvas(self, width=8, height=4, dpi=100)
        self.simulation_toolbar = NavigationToolbar(self.simulation_canvas, self)
        self.layout.addWidget(self.simulation_toolbar)
        self.layout.addWidget(self.simulation_canvas)
    
    def set_data(self, data):
        """Set the stock data for simulation"""
        self.data = data
        
        # Update date pickers to match data range if possible
        if len(data) > 0:
            start_date = data.index[0].to_pydatetime().date()
            end_date = data.index[-1].to_pydatetime().date()
            
            # Set date ranges
            self.start_date_picker.setMinimumDate(QDate(start_date))
            self.start_date_picker.setMaximumDate(QDate(end_date))
            self.end_date_picker.setMinimumDate(QDate(start_date))
            self.end_date_picker.setMaximumDate(QDate(end_date))
            
            # Set default selections - start from 6 months ago if possible
            six_months_ago = QDate(end_date).addMonths(-6)
            if six_months_ago >= QDate(start_date):
                self.start_date_picker.setDate(six_months_ago)
            else:
                self.start_date_picker.setDate(QDate(start_date))
                
            self.end_date_picker.setDate(QDate(end_date))
    
    def run_simulation(self, data, ticker):
        """Run an investment simulation based on user inputs"""
        if data is None or len(data) == 0:
            return
        
        # Get simulation parameters
        start_date = self.start_date_picker.date().toPyDate()
        end_date = self.end_date_picker.date().toPyDate()
        investment = self.investment_input.value()
        strategy = self.strategy_combo.currentText()
        
        # Convert dates to pandas datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Filter data for simulation period
        mask = (data.index >= start_date) & (data.index <= end_date)
        sim_data = data.loc[mask].copy()
        
        if sim_data.empty:
            self.simulation_results.setHtml("<p>No data available for the selected date range.</p>")
            return
        
        # Run simulation
        sim_result = run_strategy_simulation(sim_data, investment, strategy)
        
        # Display results
        self._display_simulation_results(sim_result, strategy, ticker)
    
    def _display_simulation_results(self, result, strategy, ticker):
        """Display the simulation results in the UI"""
        # Clear previous results
        self.simulation_results.clear()
        
        # Format the trade history
        trade_history = ""
        for trade in result['trades']:
            date_str = trade['date'].strftime('%Y-%m-%d')
            trade_history += (f"{date_str}: {trade['action']} at ${trade['price']:.2f} - "
                             f"{trade['shares']:.2f} shares (${trade['value']:.2f})\n")
        
        # Create HTML content for the results
        html_output = f"""
        <h2>Investment Simulation Results for {ticker}</h2>
        <h3>Strategy: {result['strategy']}</h3>
        
        <div style="margin-top: 10px; margin-bottom: 10px;">
            <table border="0" cellpadding="3" style="width: 100%;">
                <tr>
                    <td><b>Initial Investment:</b></td>
                    <td>${result['initial_investment']:.2f}</td>
                    <td><b>Final Value:</b></td>
                    <td>${result['final_value']:.2f}</td>
                </tr>
                <tr>
                    <td><b>Total Return:</b></td>
                    <td style="color: {'green' if result['return_pct'] > 0 else 'red'};">
                        {result['return_pct']:.2f}%
                    </td>
                    <td><b>Buy & Hold Return:</b></td>
                    <td style="color: {'green' if result['buy_hold_return'] > 0 else 'red'};">
                        {result['buy_hold_return']:.2f}%
                    </td>
                </tr>
                <tr>
                    <td><b>Annualized Return:</b></td>
                    <td style="color: {'green' if result['annualized_return'] > 0 else 'red'};">
                        {result['annualized_return']:.2f}%
                    </td>
                    <td><b>Period:</b></td>
                    <td>{result['start_date'].strftime('%Y-%m-%d')} to {result['end_date'].strftime('%Y-%m-%d')}</td>
                </tr>
                <tr>
                    <td><b>Number of Trades:</b></td>
                    <td>{len(result['trades'])}</td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
        </div>
        
        <h3>Performance Comparison</h3>
        <p>
            {'Strategy outperformed Buy & Hold by ' if result['return_pct'] > result['buy_hold_return'] else 'Strategy underperformed Buy & Hold by '}
            <span style="font-weight: bold; color: {'green' if result['return_pct'] > result['buy_hold_return'] else 'red'};">
                {abs(result['return_pct'] - result['buy_hold_return']):.2f}%
            </span>
        </p>
        """
        
        # Add trade history if there are trades
        if result['trades']:
            html_output += """
            <h3>Trade History:</h3>
            <pre style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-family: monospace;">
            """
            html_output += trade_history
            html_output += "</pre>"
        
        # Add disclaimer
        html_output += """
        <p><i>Disclaimer: Past performance does not guarantee future results. This simulation is for informational purposes only.</i></p>
        """
        
        # Set the HTML content
        self.simulation_results.setHtml(html_output)
        
        # Plot performance chart
        self._plot_simulation_chart(result, ticker)
    
    def _plot_simulation_chart(self, result, ticker):
        """Plot the portfolio value over time"""
        self.simulation_canvas.ax.clear()
        
        # Plot portfolio value
        self.simulation_canvas.ax.plot(result['dates'], result['portfolio_values'], 
                                      label=f"{result['strategy']} Strategy", color='blue', linewidth=2)
        
        # Plot buy & hold for comparison (normalize to same starting value)
        if 'buy_hold_return' in result:
            # Calculate buy & hold portfolio values
            initial_investment = result['initial_investment']
            buy_hold_values = []
            
            # Filter original data to match simulation period
            mask = (self.data.index >= result['start_date']) & (self.data.index <= result['end_date'])
            price_data = self.data.loc[mask]
            
            if not price_data.empty:
                start_price = price_data['Close'].iloc[0]
                shares = initial_investment / start_price
                
                for date, row in price_data.iterrows():
                    buy_hold_values.append(shares * row['Close'])
                
                # Plot buy & hold line
                self.simulation_canvas.ax.plot(price_data.index, buy_hold_values, 
                                            label="Buy & Hold", color='green', linestyle='--', linewidth=2)
        
        # Add markers for trades
        for trade in result['trades']:
            if trade['action'] == 'BUY':
                self.simulation_canvas.ax.scatter(trade['date'], trade['value'], 
                                                color='green', marker='^', s=100, zorder=5)
            else:  # SELL
                self.simulation_canvas.ax.scatter(trade['date'], trade['value'], 
                                                color='red', marker='v', s=100, zorder=5)
        
        # Set title and labels
        self.simulation_canvas.ax.set_title(f"Portfolio Performance: {ticker} - {result['strategy']}", fontsize=16)
        self.simulation_canvas.ax.set_xlabel("Date", fontsize=12)
        self.simulation_canvas.ax.set_ylabel("Portfolio Value ($)", fontsize=12)
        self.simulation_canvas.ax.grid(True, alpha=0.3)
        self.simulation_canvas.ax.legend()
        
        # Format the date axis
        self.simulation_canvas.fig.autofmt_xdate()
        
        # Update the canvas
        self.simulation_canvas.draw()