"""
Analysis tab for displaying stock analysis results
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class AnalysisTab(QWidget):
    """Tab for displaying stock analysis results"""
    
    def __init__(self):
        """Initialize the analysis tab"""
        super().__init__()
        
        # Setup layout
        self.layout = QVBoxLayout(self)
        
        # Analysis results in a nicely formatted text area
        self.analysis_text = QTextEdit()
        
        self.layout.addWidget(self.analysis_text)
    
    def update_analysis(self, ticker, recommendation, summary):
        """
        Update the analysis display with new results
        
        Args:
            ticker (str): Stock ticker symbol
            recommendation (dict): Recommendation data from StockAnalysis
            summary (dict): Summary statistics from StockAnalysis
        """
        # Create a formatted html output
        html_output = f"""
        <h2>Stock Analysis for {ticker}</h2>
        <div style="margin-top: 10px; margin-bottom: 10px;">
            <h3>Recommendation: 
                <span style="color: {'green' if recommendation['action'] == 'BUY' else 'red' if recommendation['action'] == 'SELL' else 'orange'}">
                    {recommendation['action']}
                </span> 
                ({recommendation['conviction']} conviction)
            </h3>
            
            <h4>Price Targets:</h4>
            <ul>
        """
        
        for key, value in recommendation['price_targets'].items():
            html_output += f"<li><b>{key.replace('_', ' ').title()}:</b> ${value}</li>"
        
        html_output += """
            </ul>
            
            <h4>Technical Indicators:</h4>
            <ul>
        """
        
        if 'indicators' in recommendation:
            for key, value in recommendation['indicators'].items():
                if key != 'error':
                    html_output += f"<li><b>{key.upper()}:</b> {value}</li>"
        
        html_output += """
            </ul>
            
            <h3>Summary Statistics:</h3>
            <table border="0" cellpadding="3" style="width: 100%;">
                <tr>
                    <td><b>Current Price:</b></td>
                    <td>${summary['current_price']}</td>
                    <td><b>Trading Days:</b></td>
                    <td>{summary['trading_days']}</td>
                </tr>
        """
        
        if 'volatility' in summary and summary['volatility'] is not None:
            html_output += f"""
                <tr>
                    <td><b>Volatility (Annualized):</b></td>
                    <td>{summary['volatility']}%</td>
                    <td></td>
                    <td></td>
                </tr>
            """
        
        if '52w_high' in summary:
            html_output += f"""
                <tr>
                    <td><b>52-Week High:</b></td>
                    <td>${summary['52w_high']}</td>
                    <td><b>52-Week Low:</b></td>
                    <td>${summary['52w_low']}</td>
                </tr>
                <tr>
                    <td><b>% From 52-Week High:</b></td>
                    <td>{summary['from_52w_high']}%</td>
                    <td><b>% From 52-Week Low:</b></td>
                    <td>{summary['from_52w_low']}%</td>
                </tr>
            """
        
        if 'returns' in summary:
            html_output += """
                <tr>
                    <td colspan="4"><b>Performance:</b></td>
                </tr>
            """
            
            for period, value in summary['returns'].items():
                if value is not None:
                    color = 'green' if value > 0 else 'red' if value < 0 else 'black'
                    html_output += f"""
                        <tr>
                            <td><b>{period.upper()} Return:</b></td>
                            <td style="color: {color};">{value}%</td>
                            <td></td>
                            <td></td>
                        </tr>
                    """
        
        html_output += """
            </table>
        </div>
        
        <div style="margin-top: 20px;">
            <h3>Analysis Explanation:</h3>
            <p>
        """
        
        # Add explanation based on recommendation
        if recommendation['action'] == 'BUY':
            html_output += f"""
                The analysis suggests a <b>BUY</b> recommendation with {recommendation['conviction']} conviction based on technical indicators.
                There were {recommendation['signals']['buy_signals']} buy signals versus {recommendation['signals']['sell_signals']} sell signals.
                Key factors include favorable moving average alignment and momentum indicators.
            """
        elif recommendation['action'] == 'SELL':
            html_output += f"""
                The analysis suggests a <b>SELL</b> recommendation with {recommendation['conviction']} conviction based on technical indicators.
                There were {recommendation['signals']['sell_signals']} sell signals versus {recommendation['signals']['buy_signals']} buy signals.
                Key factors include unfavorable moving average alignment and momentum indicators.
            """
        else:
            html_output += f"""
                The analysis suggests a <b>HOLD</b> recommendation with {recommendation['conviction']} conviction.
                Technical indicators are currently mixed with {recommendation['signals']['buy_signals']} buy signals and {recommendation['signals']['sell_signals']} sell signals.
                Consider waiting for a clearer trend to emerge before taking action.
            """
        
        html_output += """
            </p>
            <p><i>Disclaimer: This analysis is for informational purposes only and should not be considered financial advice. Always conduct your own research before making investment decisions.</i></p>
        </div>
        """
        
        self.analysis_text.setHtml(html_output)