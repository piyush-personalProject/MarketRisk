"""Command-line interface for Options Greeks Calculator."""

from .calculator import OptionsGreeksCalculator


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
            option_type=option_type
        )
        
        calculator.display_greeks()
        calculator.plot_option_values(days=10, num_points=50)
        
    except ValueError as e:
        print(f"Error: {e}. Please check your inputs.")
        return


if __name__ == "__main__":
    main()

