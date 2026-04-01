"""Command-line interface for Options Greeks Calculator."""

import sys
from pathlib import Path

# Handle both relative imports (module) and direct script execution
try:
    from .calculator import OptionsGreeksCalculator
except ImportError:
    # Add parent directory to path for direct script execution
    sys.path.insert(0, str(Path(__file__).parent))
    from calculator import OptionsGreeksCalculator


def main() -> None:
    """Run the interactive Options Greeks Calculator."""
    print("Options Greeks Calculator & Plotter\n")
    
    # Get user input
    ticker = input("Enter ticker symbol (default: AAPL): ").strip().upper() or "AAPL"
    
    try:
        strike = float(input("Enter strike price (default: 180): ") or "180")
        expiry = (
            input("Enter expiry date in YYYY-MM-DD format (default: 2026-06-19): ")
            .strip() or "2026-06-19"
        )
        volatility = float(input("Enter volatility as decimal (default: 0.25): ") or "0.25")
        risk_free_rate = float(
            input("Enter risk-free rate as decimal (default: 0.045): ") or "0.045"
        )
        dividend_yield = float(
            input("Enter dividend yield as decimal (default: 0.0): ") or "0.0"
        )
        option_type = (
            input("Enter option type 'call' or 'put' (default: call): ").strip().lower()
            or "call"
        )
        
        calculator = OptionsGreeksCalculator(
            ticker_symbol=ticker,
            strike_price=strike,
            expiry_date=expiry,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            dividend_yield=dividend_yield,
            option_type=option_type
        )
        
        calculator.display_greeks()
        calculator.plot_option_values(days=10, num_points=50)
        
    except ValueError as e:
        print(f"Error: {e}. Please check your inputs.")
        return


if __name__ == "__main__":
    main()

