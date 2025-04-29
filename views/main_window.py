"""
Main window for the stock analysis application
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGroupBox, QLabel, QComboBox, QPushButton, QTabWidget,
    QSplitter, QMessageBox, QStatusBar
)
from PyQt5.QtCore import Qt

from views.analysis_tab import AnalysisTab
from views.charts_tab import ChartsTab
from views.indicators_tab import IndicatorsTab
from views.simulation_tab import SimulationTab
from controllers.data_controller import fetch_stock_data, get_period_mapping
from models.stock_analysis import StockAnalysis
from utils.styles import set_app_style

class StockAnalysisApp(QMainWindow):
    """Main application window for the stock analysis tool"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        # Application settings
        self.setWindowTitle("Enhanced Stock Analysis Tool")
        self.setGeometry(100, 100, 1200, 900)
        set_app_style("Fusion")  # Modern dark look
        
        # Data storage
        self.data = None
        self.ticker_history = []
        
        # Initialize UI
        self._init_ui()
        
        # Status bar for information
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main vertical layout
        main_layout = QVBoxLayout(self.central_widget)
        
        # Create input section at the top
        input_group = QGroupBox("Stock Selection")
        input_layout = QHBoxLayout()
        
        # Ticker input with history dropdown
        ticker_layout = QHBoxLayout()
        self.ticker_label = QLabel("Stock Ticker:")
        self.ticker_input = QComboBox()
        self.ticker_input.setEditable(True)
        self.ticker_input.setMinimumWidth(100)
        ticker_layout.addWidget(self.ticker_label)
        ticker_layout.addWidget(self.ticker_input)
        
        # Period selection
        period_layout = QHBoxLayout()
        self.period_label = QLabel("Time Period:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years", "Max"])
        self.period_combo.setCurrentIndex(3)  # Default to 1 Year
        period_layout.addWidget(self.period_label)
        period_layout.addWidget(self.period_combo)
        
        # Risk tolerance
        risk_layout = QHBoxLayout()
        self.risk_label = QLabel("Risk Tolerance:")
        self.risk_combo = QComboBox()
        self.risk_combo.addItems(["Low", "Moderate", "High"])
        self.risk_combo.setCurrentIndex(1)  # Default to Moderate
        risk_layout.addWidget(self.risk_label)
        risk_layout.addWidget(self.risk_combo)
        
        # Analyze button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setMinimumWidth(100)
        
        # Add all to input layout
        input_layout.addLayout(ticker_layout)
        input_layout.addLayout(period_layout)
        input_layout.addLayout(risk_layout)
        input_layout.addWidget(self.analyze_button)
        input_group.setLayout(input_layout)
        
        # Add input group to main layout
        main_layout.addWidget(input_group)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        
        # Create tabs for different views
        self.tabs = QTabWidget()
        
        # Create tab instances
        self.analysis_tab = AnalysisTab()
        self.charts_tab = ChartsTab()
        self.indicators_tab = IndicatorsTab() 
        self.simulation_tab = SimulationTab()
        
        # Add tabs to tab widget
        self.tabs.addTab(self.analysis_tab, "Analysis")
        self.tabs.addTab(self.charts_tab, "Price Charts")
        self.tabs.addTab(self.indicators_tab, "Technical Indicators")
        self.tabs.addTab(self.simulation_tab, "Investment Simulation")
        
        # Add tabs to splitter
        splitter.addWidget(self.tabs)
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Connect signals and slots
        self.analyze_button.clicked.connect(self.perform_analysis)
        self.charts_tab.apply_indicators_button.clicked.connect(self.update_charts)
        self.simulation_tab.simulate_button.clicked.connect(self.run_simulation)
        
        # Ensure the application has a reasonable minimum size
        self.setMinimumSize(800, 600)
    
    def perform_analysis(self):
        """Perform stock analysis when the analyze button is clicked"""
        ticker = self.ticker_input.currentText().strip().upper()
        if not ticker:
            self.show_message("Please enter a valid stock ticker.")
            return
        
        # Update status
        self.status_bar.showMessage(f"Fetching data for {ticker}...")
        
        # Get period from dropdown
        period_map = get_period_mapping()
        selected_period = self.period_combo.currentText()
        yf_period = period_map.get(selected_period, "1y")
        
        # Fetch data
        data = fetch_stock_data(ticker, period=yf_period)
        if data is None:
            self.show_message(f"No data found for ticker: {ticker}")
            return
        
        # Store the data and update ticker history
        self.data = data
        
        # Add to ticker history if not already there
        if ticker not in self.ticker_history:
            self.ticker_history.append(ticker)
            self.ticker_input.clear()
            self.ticker_input.addItems(self.ticker_history)
            self.ticker_input.setCurrentText(ticker)
        
        # Get risk tolerance
        risk_tolerance = self.risk_combo.currentText().lower()
        
        # Analyze data
        analysis = StockAnalysis(data, risk_tolerance=risk_tolerance)
        recommendation = analysis.generate_recommendation()
        summary = analysis.get_summary_statistics()
        
        # Update tabs with analysis data
        self.analysis_tab.update_analysis(ticker, recommendation, summary)
        self.charts_tab.update_charts(ticker, data, analysis)
        self.indicators_tab.update_indicators(data, analysis)
        self.simulation_tab.set_data(data)
        
        # Update status
        self.status_bar.showMessage(f"Analysis complete for {ticker}")
        
        # Set tab to analysis
        self.tabs.setCurrentIndex(0)
    
    def update_charts(self):
        """Update charts when indicators are changed"""
        if self.data is None:
            return
            
        ticker = self.ticker_input.currentText().strip().upper()
        risk_tolerance = self.risk_combo.currentText().lower()
        
        # Create analysis object
        analysis = StockAnalysis(self.data, risk_tolerance=risk_tolerance)
        
        # Update charts with selected indicators
        self.charts_tab.update_charts(ticker, self.data, analysis)
        
        # Set tab to charts
        self.tabs.setCurrentIndex(1)
    
    def run_simulation(self):
        """Run investment simulation"""
        # Pass control to the simulation tab
        if self.data is None:
            self.show_message("Please analyze a stock first before running a simulation.")
            return
        
        self.simulation_tab.run_simulation(self.data, self.ticker_input.currentText().strip().upper())
        self.tabs.setCurrentIndex(3)  # Switch to simulation tab
    
    def show_message(self, message):
        """Show a message dialog to the user"""
        QMessageBox.information(self, "Stock Analysis", message)