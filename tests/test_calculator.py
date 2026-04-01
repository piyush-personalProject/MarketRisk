"""Unit tests for EquityOptionsCalculator."""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from marketrisk.calculator import EquityOptionsCalculator


def create_mock_ticker(spot_price=150.0):
    """Helper function to create a properly mocked ticker."""
    mock_ticker = MagicMock()
    df = pd.DataFrame({'Close': [spot_price]})
    mock_ticker.history.return_value = df
    return mock_ticker


class TestEquityOptionsCalculator(unittest.TestCase):
    """Test cases for EquityOptionsCalculator class."""

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

        calc = EquityOptionsCalculator(
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
            EquityOptionsCalculator(
                ticker_symbol='INVALID',
                strike_price=150,
                expiry_date=self.expiry
            )

    @patch('marketrisk.calculator.yf.Ticker')
    def test_option_type_case_insensitivity(self, mock_ticker_class):
        """Test that option type is normalized to lowercase."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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

        calc_low_vol = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.10,
            option_type='call'
        )

        calc_high_vol = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
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
        calc = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date
        )

        self.assertEqual(calc.risk_free_rate, 0.045)
        self.assertEqual(calc.volatility, 0.25)
        self.assertEqual(calc.option_type, 'call')

    @patch('marketrisk.calculator.yf.Ticker')
    def test_initialization_with_dividend_yield(self, mock_ticker_class):
        """Test initialization with dividend yield parameter."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        calc = EquityOptionsCalculator(
            ticker_symbol='IBM',
            strike_price=150,
            expiry_date=self.expiry,
            dividend_yield=0.02
        )

        self.assertEqual(calc.dividend_yield, 0.02)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_yield_default_value(self, mock_ticker_class):
        """Test that dividend yield defaults to 0.0."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        calc = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=self.expiry
        )

        self.assertEqual(calc.dividend_yield, 0.0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_calculate_greeks_with_dividend_yield(self, mock_ticker_class):
        """Test Greeks calculation with dividend yield."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = EquityOptionsCalculator(
            ticker_symbol='IBM',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.02,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertIn('Dividend Yield', greeks)
        self.assertEqual(greeks['Dividend Yield'], 0.02)
        self.assertGreater(greeks['Price'], 0)
        self.assertIn('Delta', greeks)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_impact_on_call_price(self, mock_ticker_class):
        """Test that dividend yield reduces call option price."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        # Call without dividend
        calc_no_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call',
            dividend_yield=0.0
        )

        # Call with dividend
        calc_with_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call',
            dividend_yield=0.02
        )

        greeks_no_div = calc_no_div.calculate_greeks()
        greeks_with_div = calc_with_div.calculate_greeks()

        # Call price should be lower with dividend
        self.assertGreater(greeks_no_div['Price'], greeks_with_div['Price'])

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_impact_on_put_price(self, mock_ticker_class):
        """Test that dividend yield increases put option price."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        # Put without dividend
        calc_no_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='put',
            dividend_yield=0.0
        )

        # Put with dividend
        calc_with_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='put',
            dividend_yield=0.02
        )

        greeks_no_div = calc_no_div.calculate_greeks()
        greeks_with_div = calc_with_div.calculate_greeks()

        # Put price should be higher with dividend
        self.assertLess(greeks_no_div['Price'], greeks_with_div['Price'])

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_impact_on_call_delta(self, mock_ticker_class):
        """Test that dividend yield reduces call delta."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        # Call without dividend
        calc_no_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call',
            dividend_yield=0.0
        )

        # Call with dividend
        calc_with_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call',
            dividend_yield=0.02
        )

        greeks_no_div = calc_no_div.calculate_greeks()
        greeks_with_div = calc_with_div.calculate_greeks()

        # Call delta should be lower with dividend
        self.assertGreater(greeks_no_div['Delta'], greeks_with_div['Delta'])

    @patch('marketrisk.calculator.yf.Ticker')
    def test_override_dividend_in_calculate_greeks(self, mock_ticker_class):
        """Test overriding dividend yield in calculate_greeks method."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.01
        )

        # Override dividend
        greeks = calc.calculate_greeks(dividend_yield=0.03)

        self.assertEqual(greeks['Dividend Yield'], 0.03)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_high_dividend_yield(self, mock_ticker_class):
        """Test calculation with high dividend yield (5%)."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = EquityOptionsCalculator(
            ticker_symbol='REIT',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.05,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertEqual(greeks['Dividend Yield'], 0.05)
        self.assertGreater(greeks['Price'], 0)
        self.assertIn('Delta', greeks)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_yield_zero_vs_not_specified(self, mock_ticker_class):
        """Test that zero dividend yield gives same result as default."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        # Without specifying dividend (uses default 0.0)
        calc1 = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25
        )

        # Explicitly set to 0.0
        calc2 = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.0
        )

        greeks1 = calc1.calculate_greeks()
        greeks2 = calc2.calculate_greeks()

        self.assertEqual(greeks1['Price'], greeks2['Price'])
        self.assertEqual(greeks1['Delta'], greeks2['Delta'])

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_and_custom_spot_price(self, mock_ticker_class):
        """Test dividend yield with custom spot price."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.02,
            option_type='call'
        )

        greeks = calc.calculate_greeks(spot_price=160.0)

        self.assertEqual(greeks['Spot'], 160.0)
        self.assertEqual(greeks['Dividend Yield'], 0.02)
        self.assertGreater(greeks['Price'], 0)

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_with_put_option_itm(self, mock_ticker_class):
        """Test put option with dividend that is in-the-money."""
        mock_ticker_class.return_value = create_mock_ticker(140.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.02,
            option_type='put'
        )

        greeks = calc.calculate_greeks()

        # ITM put should have negative delta (close to -1)
        self.assertLess(greeks['Delta'], 0)
        self.assertGreater(greeks['Price'], 10)  # At least intrinsic value

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_affects_all_greeks(self, mock_ticker_class):
        """Test that dividend yield affects all Greeks calculations."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        # Use longer time and higher dividend to see meaningful differences
        future_date = (datetime.now(timezone.utc) + timedelta(days=180)).strftime("%Y-%m-%d")

        calc_no_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.0
        )

        calc_with_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.05  # Higher dividend for more noticeable effect
        )

        greeks_no_div = calc_no_div.calculate_greeks()
        greeks_with_div = calc_with_div.calculate_greeks()

        # Check that Delta differs significantly (dividend has larger effect on delta)
        self.assertNotEqual(greeks_no_div['Delta'], greeks_with_div['Delta'])

        # Vega should also differ
        self.assertNotEqual(greeks_no_div['Vega (1%)'], greeks_with_div['Vega (1%)'])

    @patch('marketrisk.calculator.yf.Ticker')
    def test_dividend_impact_on_delta_and_vega(self, mock_ticker_class):
        """Test dividend impact on Delta and Vega specifically."""
        mock_ticker_class.return_value = create_mock_ticker(150.0)

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        # No dividend
        calc_no_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.0,
            option_type='call'
        )

        # With 3% dividend
        calc_with_div = EquityOptionsCalculator(
            ticker_symbol='AAPL',
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            dividend_yield=0.03,
            option_type='call'
        )

        greeks_no_div = calc_no_div.calculate_greeks()
        greeks_with_div = calc_with_div.calculate_greeks()

        # Delta should definitely be lower with dividend
        self.assertGreater(greeks_no_div['Delta'], greeks_with_div['Delta'],
                          "Dividend should reduce call delta")


if __name__ == '__main__':
    unittest.main()

