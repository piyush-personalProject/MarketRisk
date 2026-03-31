"""Unit tests for OptionsGreeksCalculator."""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from marketrisk.calculator import OptionsGreeksCalculator


def create_mock_ticker(spot_price=150.0):
    """Helper function to create a properly mocked ticker."""
    mock_ticker = MagicMock()
    df = pd.DataFrame({'Close': [spot_price]})
    mock_ticker.history.return_value = df
    return mock_ticker


class TestOptionsGreeksCalculator(unittest.TestCase):
    """Test cases for OptionsGreeksCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.ticker = 'AAPL'
        self.strike = 150.0
        self.expiry = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        self.volatility = 0.25
        self.rate = 0.05

    @patch('marketrisk.calculator.yf.Ticker')
    def test_initialization_with_valid_inputs(self, mock_ticker_class):
        """Test successful initialization with valid parameters."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=self.expiry,
            risk_free_rate=0.05,
            volatility=0.25,
            option_type='call'
        )

        self.assertEqual(calc.ticker_symbol, 'AAPL')
        self.assertEqual(calc.strike_price, 150)
        self.assertEqual(calc.volatility, 0.25)
        self.assertEqual(calc.option_type, 'call')
        self.assertEqual(calc.spot_price, 150.0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_initialization_with_invalid_ticker(self, mock_ticker_class):
        """Test initialization with invalid ticker that returns no data."""
        empty_df = pd.DataFrame()
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = empty_df
        mock_ticker_class.return_value = mock_ticker

        with self.assertRaises(ValueError):
            OptionsGreeksCalculator(
                ticker_symbol='INVALID',
                strike_price=150,
                expiry_date=self.expiry
            )

    @patch('marketrisk.calculator.yf.Ticker')
    def test_option_type_case_insensitivity(self, mock_ticker_class):
        """Test that option type is normalized to lowercase."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=self.expiry,
            option_type='CALL'
        )

        self.assertEqual(calc.option_type, 'call')

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_time_to_expiry(self, mock_ticker_class):
        """Test time to expiry calculation."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date
        )

        T = calc.calculate_time_to_expiry()
        self.assertGreater(T, 0)
        self.assertLess(T, 0.1)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_time_to_expiry_expired(self, mock_ticker_class):
        """Test time to expiry for an already expired option."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        past_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=past_date
        )

        T = calc.calculate_time_to_expiry()
        self.assertEqual(T, 0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_call_option(self, mock_ticker_class):
        """Test Greeks calculation for a call option."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            risk_free_rate=0.05,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertIn('Price', greeks)
        self.assertIn('Delta', greeks)
        self.assertIn('Gamma', greeks)
        self.assertIn('Vega (1%)', greeks)
        self.assertIn('Theta', greeks)
        self.assertGreater(greeks['Price'], 0)
        self.assertGreaterEqual(greeks['Delta'], 0)
        self.assertLessEqual(greeks['Delta'], 1)
        self.assertGreater(greeks['Gamma'], 0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_put_option(self, mock_ticker_class):
        """Test Greeks calculation for a put option."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            risk_free_rate=0.05,
            option_type='put'
        )

        greeks = calc.calculate_greeks()

        self.assertGreater(greeks['Price'], 0)
        self.assertLessEqual(greeks['Delta'], 0)
        self.assertGreaterEqual(greeks['Delta'], -1)
        self.assertGreater(greeks['Gamma'], 0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_expired_option(self, mock_ticker_class):
        """Test Greeks calculation for an expired option."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        past_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=past_date,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertEqual(greeks['Status'], 'Expired')
        self.assertEqual(greeks['Delta'], 0)
        self.assertEqual(greeks['Gamma'], 0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_in_the_money_call(self, mock_ticker_class):
        """Test call option that is in-the-money."""
        mock_ticker_class.return_value = create_mock_ticker(160.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        # ITM call should have delta closer to 1
        self.assertGreater(greeks['Delta'], 0.5)
        # Intrinsic value should be at least spot - strike
        self.assertGreater(greeks['Price'], 10)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_out_of_the_money_call(self, mock_ticker_class):
        """Test call option that is out-of-the-money."""
        mock_ticker_class.return_value = create_mock_ticker(140.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        # OTM call should have delta closer to 0
        self.assertLess(greeks['Delta'], 0.5)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_custom_spot_price(self, mock_ticker_class):
        """Test Greeks calculation with custom spot price."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25
        )

        greeks_custom = calc.calculate_greeks(spot_price=160.0)
        self.assertEqual(greeks_custom['Spot'], 160.0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_custom_time_to_expiry(self, mock_ticker_class):
        """Test Greeks calculation with custom time to expiry."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25
        )

        greeks_custom = calc.calculate_greeks(time_to_expiry=0.05)
        self.assertEqual(greeks_custom['T_Years'], 0.05)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_volatility_impact_on_option_price(self, mock_ticker_class):
        """Test that higher volatility increases option price."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        calc_low_vol = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.10,
            option_type='call'
        )

        calc_high_vol = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.40,
            option_type='call'
        )

        greeks_low = calc_low_vol.calculate_greeks()
        greeks_high = calc_high_vol.calculate_greeks()

        self.assertLess(greeks_low['Price'], greeks_high['Price'])

    @patch('marketrisk.calculator.plt.show')
    @patch('marketrisk.calculator.plt.savefig')
    @patch('marketrisk.calculator.yf.Ticker')
    def test_plot_option_values(self, mock_ticker_class, mock_savefig, mock_show):
        """Test plotting functionality."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25
        )

        # Should not raise an exception
        calc.plot_option_values(days=10, num_points=20)

        # Verify savefig was called
        mock_savefig.assert_called_once()
        mock_show.assert_called_once()

    @patch('marketrisk.calculator.yf.Ticker')
    def test_default_parameters(self, mock_ticker_class):
        """Test that default parameters are set correctly."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = OptionsGreeksCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date
        )

        self.assertEqual(calc.risk_free_rate, 0.045)
        self.assertEqual(calc.volatility, 0.25)
        self.assertEqual(calc.option_type, 'call')


if __name__ == '__main__':
    unittest.main()

