#!/usr/bin/env python
"""
Stock Analysis Application - Main Entry Point
Launches the stock analysis application GUI
"""
import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import StockAnalysisApp

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = StockAnalysisApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()