# Unit Testing the data controller
# Under normal circumstances, all tests should pass

# Import requirements
import unittest
from unittest.mock import patch
import pandas as pd
from data_controller import fetch_stock_data, get_period_mapping 

class TestStockDataController(unittest.TestCase):

    @patch('yfinance.download')
    def test_fetch_valid_ticker(self, mock_download):
        mock_data = pd.DataFrame({'Open': [100.0], 'High': [105.0], 'Low': [95.0], 'Close': [102.0], 'Volume': [1000]})
        mock_download.return_value = mock_data
        result = fetch_stock_data('AAPL')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    @patch('yfinance.download')
    def test_invalid_ticker(self, mock_download):
        mock_download.return_value = pd.DataFrame()
        result = fetch_stock_data('INVALID')
        self.assertIsNone(result)

    def test_get_period_mapping(self):
        expected = {
            "1 Month": "1mo", 
            "3 Months": "3mo", 
            "6 Months": "6mo",
            "1 Year": "1y", 
            "2 Years": "2y", 
            "5 Years": "5y", 
            "Max": "max"
        }
        self.assertDictEqual(get_period_mapping(), expected)

if __name__ == '__main__':
    unittest.main()