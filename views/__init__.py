"""
Views package for stock analysis application
"""
from views.main_window import StockAnalysisApp
from views.analysis_tab import AnalysisTab
from views.charts_tab import ChartsTab
from views.indicators_tab import IndicatorsTab
from views.simulation_tab import SimulationTab

__all__ = [
    'StockAnalysisApp',
    'AnalysisTab',
    'ChartsTab',
    'IndicatorsTab',
    'SimulationTab'
]