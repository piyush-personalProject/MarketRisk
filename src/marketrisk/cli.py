"""Command-line interface for Options Greeks Calculator.

Supports both:
- EquityOptionsCalculator (Black-Scholes for stocks)
- FuturesOptionsCalculator (Black76 for futures)
"""

import sys
from pathlib import Path

# Handle both relative imports (module) and direct script execution
try:
    from .calculator import EquityOptionsCalculator
    from .futures_calculator import FuturesOptionsCalculator
except ImportError:
    # Add parent directory to path for direct script execution
    sys.path.insert(0, str(Path(__file__).parent))
    from calculator import EquityOptionsCalculator
    from futures_calculator import FuturesOptionsCalculator


def main_equity_options() -> None:
    """Run the interactive Equity Options Greeks Calculator."""
    print("\n" + "="*60)
    print("EQUITY OPTIONS CALCULATOR - Black-Scholes Model")
    print("="*60 + "\n")

    # Get user input
    ticker = input("Enter ticker symbol (default: AAPL): ").strip().upper() or "AAPL"
    
    try:
        strike = float(input("Enter strike price (default: 150): ") or "150")
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
        
        calculator = EquityOptionsCalculator(
            ticker_symbol=ticker,
            strike_price=strike,
            expiry_date=expiry,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            dividend_yield=dividend_yield,
            option_type=option_type
        )
        
        calculator.display_greeks()

        plot_choice = input("\nGenerate plot? (y/n, default: y): ").strip().lower() or "y"
        if plot_choice == 'y':
            calculator.plot_option_values(days=10, num_points=50)

    except ValueError as e:
        print(f"\n✗ Error: {e}. Please check your inputs.")
        return


def main_futures_options() -> None:
    """Run the interactive Futures Options Greeks Calculator."""
    print("\n" + "="*60)
    print("FUTURES OPTIONS CALCULATOR - Black76 Model")
    print("="*60 + "\n")

    print("Supported: Commodity, Interest Rate, Currency, Index Futures\n")

    # Get user input
    try:
        futures_price = float(input("Enter futures contract price (e.g., 75.50): "))
        strike = float(input("Enter strike price (e.g., 75.0): "))
        expiry = (
            input("Enter expiry date in YYYY-MM-DD format (default: 2026-06-19): ")
            .strip() or "2026-06-19"
        )
        volatility = float(input("Enter volatility as decimal (default: 0.25): ") or "0.25")
        risk_free_rate = float(
            input("Enter risk-free rate as decimal (default: 0.045): ") or "0.045"
        )
        option_type = (
            input("Enter option type 'call' or 'put' (default: call): ").strip().lower()
            or "call"
        )

        calculator = FuturesOptionsCalculator(
            futures_price=futures_price,
            strike_price=strike,
            expiry_date=expiry,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            option_type=option_type
        )

        calculator.display_greeks()

        plot_choice = input("\nGenerate plot? (y/n, default: y): ").strip().lower() or "y"
        if plot_choice == 'y':
            calculator.plot_option_values(days=10, num_points=50)

    except ValueError as e:
        print(f"\n✗ Error: {e}. Please check your inputs.")
        return


def main() -> None:
    """Main menu for selecting calculator type."""
    print("\n" + "="*60)
    print("MARKETRISK - OPTIONS GREEKS CALCULATOR")
    print("="*60)
    print("\nSelect option type:")
    print("  1. Equity/Stock Options (Black-Scholes)")
    print("  2. Futures Options (Black76)")
    print("  0. Exit")
    print("-"*60)

    choice = input("\nEnter choice (1, 2, or 0): ").strip()

    if choice == "1":
        main_equity_options()
    elif choice == "2":
        main_futures_options()
    elif choice == "0":
        print("\nGoodbye! 👋\n")
        return
    else:
        print("\n✗ Invalid choice. Please enter 1, 2, or 0.")
        main()  # Recursive call to retry


if __name__ == "__main__":
    main()

