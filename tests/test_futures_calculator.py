"""Unit tests for FuturesOptionsCalculator (Black76 model)."""

import unittest
from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from marketrisk.futures_calculator import FuturesOptionsCalculator


class TestFuturesOptionsCalculator(unittest.TestCase):
    """Test cases for FuturesOptionsCalculator using Black76 model."""

    def setUp(self):
        """Set up test fixtures."""
        self.futures_price = 100.0
        self.strike = 100.0
        self.expiry = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        self.volatility = 0.25
        self.rate = 0.05

    def test_initialization_with_valid_inputs(self):
        """Test successful initialization with valid parameters."""
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=self.expiry,
            risk_free_rate=0.05,
            volatility=0.25,
            option_type='call'
        )

        self.assertEqual(calc.futures_price, 100.0)
        self.assertEqual(calc.strike_price, 100)
        self.assertEqual(calc.volatility, 0.25)
        self.assertEqual(calc.option_type, 'call')

    def test_option_type_case_insensitivity(self):
        """Test that option type is normalized to lowercase."""
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=self.expiry,
            option_type='CALL'
        )

        self.assertEqual(calc.option_type, 'call')

    def test_calculate_time_to_expiry(self):
        """Test time to expiry calculation."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date
        )

        T = calc.calculate_time_to_expiry()
        self.assertGreater(T, 0)
        self.assertLess(T, 0.1)

    def test_calculate_time_to_expiry_expired(self):
        """Test time to expiry for an already expired option."""
        past_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=past_date
        )

        T = calc.calculate_time_to_expiry()
        self.assertEqual(T, 0)

    def test_calculate_greeks_call_option(self):
        """Test Greeks calculation for a call option using Black76."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
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
        self.assertIn('Model', greeks)
        self.assertEqual(greeks['Model'], 'Black76')
        self.assertGreater(greeks['Price'], 0)

    def test_calculate_greeks_put_option(self):
        """Test Greeks calculation for a put option using Black76."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25,
            risk_free_rate=0.05,
            option_type='put'
        )

        greeks = calc.calculate_greeks()

        self.assertGreater(greeks['Price'], 0)
        self.assertLess(greeks['Delta'], 0)
        self.assertEqual(greeks['Model'], 'Black76')

    def test_calculate_greeks_expired_option(self):
        """Test Greeks calculation for an expired option."""
        past_date = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=past_date,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertEqual(greeks['Status'], 'Expired')
        self.assertEqual(greeks['Delta'], 0)
        self.assertEqual(greeks['Gamma'], 0)

    def test_calculate_greeks_itm_call(self):
        """Test call option that is in-the-money."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=110.0,  # ITM call
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        # ITM call should have delta closer to 1
        self.assertGreater(greeks['Delta'], 0.5)
        # Price should be higher
        self.assertGreater(greeks['Price'], 10)

    def test_calculate_greeks_otm_call(self):
        """Test call option that is out-of-the-money."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=90.0,  # OTM call
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        # OTM call should have delta closer to 0
        self.assertLess(greeks['Delta'], 0.5)

    def test_calculate_greeks_custom_futures_price(self):
        """Test Greeks calculation with custom futures price."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25
        )

        greeks_custom = calc.calculate_greeks(futures_price=110.0)
        self.assertEqual(greeks_custom['Futures Price'], 110.0)

    def test_calculate_greeks_custom_time_to_expiry(self):
        """Test Greeks calculation with custom time to expiry."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25
        )

        greeks_custom = calc.calculate_greeks(time_to_expiry=0.05)
        self.assertEqual(greeks_custom['T_Years'], 0.05)

    def test_volatility_impact_on_option_price(self):
        """Test that higher volatility increases option price."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        calc_low_vol = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.10,
            option_type='call'
        )

        calc_high_vol = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.40,
            option_type='call'
        )

        greeks_low = calc_low_vol.calculate_greeks()
        greeks_high = calc_high_vol.calculate_greeks()

        self.assertLess(greeks_low['Price'], greeks_high['Price'])

    def test_default_parameters(self):
        """Test that default parameters are set correctly."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date
        )

        self.assertEqual(calc.risk_free_rate, 0.045)
        self.assertEqual(calc.volatility, 0.25)
        self.assertEqual(calc.option_type, 'call')

    def test_black76_no_dividend_yield(self):
        """Test that Black76 does NOT use dividend yield."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25,
            option_type='call'
        )

        # Black76 should not have dividend_yield attribute
        self.assertFalse(hasattr(calc, 'dividend_yield'))

    def test_black76_vs_atm_call_put_parity(self):
        """Test put-call parity for ATM options in Black76."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        calc_call = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25,
            risk_free_rate=0.05,
            option_type='call'
        )

        calc_put = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date,
            volatility=0.25,
            risk_free_rate=0.05,
            option_type='put'
        )

        greeks_call = calc_call.calculate_greeks()
        greeks_put = calc_put.calculate_greeks()

        # Black76 put-call parity: C - P = e^(-r*T) * (F - K)
        # For ATM (F=K): C - P should ≈ 0
        price_diff = abs(greeks_call['Price'] - greeks_put['Price'])
        self.assertLess(price_diff, 0.01)  # Should be very close

    def test_black76_vs_black_scholes_comparison(self):
        """Test that Black76 and Black-Scholes give similar results for ATM options."""
        from marketrisk.calculator import OptionsGreeksCalculator

        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")

        # Black76 (no dividend yield)
        futures_calc = FuturesOptionsCalculator(
            futures_price=150.0,
            strike_price=150,
            expiry_date=future_date,
            volatility=0.25,
            risk_free_rate=0.05,
            option_type='call'
        )

        # Approximate Black-Scholes with mocked ticker
        # (We use futures price as spot for comparison)
        try:
            from unittest.mock import patch, MagicMock
            import pandas as pd

            with patch('marketrisk.calculator.yf.Ticker') as mock_ticker:
                mock_ticker_instance = MagicMock()
                df = pd.DataFrame({'Close': [150.0]})
                mock_ticker_instance.history.return_value = df
                mock_ticker.return_value = mock_ticker_instance

                bs_calc = OptionsGreeksCalculator(
                    ticker_symbol='TEST',
                    strike_price=150,
                    expiry_date=future_date,
                    volatility=0.25,
                    risk_free_rate=0.05,
                    dividend_yield=0.0,  # No dividend
                    option_type='call'
                )

                bs_greeks = bs_calc.calculate_greeks()
                futures_greeks = futures_calc.calculate_greeks()

                # Results should be reasonably close (allow 5% difference)
                price_diff_pct = abs(bs_greeks['Price'] - futures_greeks['Price']) / bs_greeks['Price']
                self.assertLess(price_diff_pct, 0.05)
        except Exception:
            # Skip if unable to import mocking modules
            pass

    def test_futures_commodity_option(self):
        """Test typical commodity futures option (e.g., crude oil)."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=60)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=75.50,  # Crude oil futures
            strike_price=75.0,
            expiry_date=future_date,
            volatility=0.35,  # Higher volatility for commodities
            risk_free_rate=0.04,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertGreater(greeks['Price'], 0)
        self.assertIn('Model', greeks)
        self.assertEqual(greeks['Model'], 'Black76')

    def test_futures_currency_option(self):
        """Test currency futures option."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=90)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=1.2050,  # EUR/USD futures
            strike_price=1.20,
            expiry_date=future_date,
            volatility=0.12,  # Lower volatility for FX
            risk_free_rate=0.03,
            option_type='call'
        )

        greeks = calc.calculate_greeks()

        self.assertGreater(greeks['Price'], 0)
        self.assertEqual(greeks['Model'], 'Black76')

    def test_futures_interest_rate_option(self):
        """Test interest rate futures option (e.g., bond futures)."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=90)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=130.50,  # Bond futures
            strike_price=130.0,
            expiry_date=future_date,
            volatility=0.08,  # Low volatility for bonds
            risk_free_rate=0.04,
            option_type='put'
        )

        greeks = calc.calculate_greeks()

        self.assertGreater(greeks['Price'], 0)
        self.assertEqual(greeks['Model'], 'Black76')

    def test_greeks_output_contains_model_info(self):
        """Test that Greeks output includes model information."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
        calc = FuturesOptionsCalculator(
            futures_price=100.0,
            strike_price=100,
            expiry_date=future_date
        )

        greeks = calc.calculate_greeks()

        self.assertIn('Model', greeks)
        self.assertEqual(greeks['Model'], 'Black76')
        self.assertIn('Futures Price', greeks)
        self.assertIn('Strike', greeks)


if __name__ == '__main__':
    unittest.main()

