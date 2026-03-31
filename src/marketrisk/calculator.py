"""Options Greeks Calculator using Black-Scholes model."""

import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime, timedelta, timezone


class OptionsGreeksCalculator:
    """Calculate Greeks and plot option values over time using Black-Scholes model."""

    def __init__(
        self,
        ticker_symbol: str,
        strike_price: float,
        expiry_date: str,
        risk_free_rate: float = 0.045,
        volatility: float = 0.25,
        option_type: str = 'call'
    ):
        """
        Initialize the options calculator with market and option parameters.

        Args:
            ticker_symbol: Stock ticker (e.g., 'AAPL')
            strike_price: Strike price of the option
            expiry_date: Expiry date in format 'YYYY-MM-DD'
            risk_free_rate: Risk-free rate (default 0.045 = 4.5%)
            volatility: Implied volatility (default 0.25 = 25%)
            option_type: 'call' or 'put'

        Raises:
            ValueError: If ticker data cannot be fetched
        """
        self.ticker_symbol = ticker_symbol
        self.strike_price = strike_price
        self.expiry_date = expiry_date
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.option_type = option_type.lower()
        self.spot_price = None
        self.fetch_spot_price()

    def fetch_spot_price(self) -> None:
        """
        Fetch current spot price from Yahoo Finance.

        Raises:
            ValueError: If unable to fetch data for the ticker symbol
        """
        ticker = yf.Ticker(self.ticker_symbol)
        todays_data = ticker.history(period='1d')
        if todays_data.empty:
            raise ValueError(f"Could not fetch data for {self.ticker_symbol}")
        self.spot_price = todays_data['Close'].iloc[-1]

    def calculate_time_to_expiry(self, date_str: str = None) -> float:
        """
        Calculate time to expiry in years.

        Args:
            date_str: Date string in format 'YYYY-MM-DD' (uses expiry_date if None)

        Returns:
            Time to expiry in years (minimum 0)
        """
        now = datetime.now(timezone.utc)
        expiry = datetime.strptime(
            date_str or self.expiry_date,
            "%Y-%m-%d"
        ).replace(tzinfo=timezone.utc)
        seconds_to_expiry = (expiry - now).total_seconds()
        return max(0, seconds_to_expiry / (365 * 24 * 3600))

    def calculate_greeks(
        self,
        spot_price: float = None,
        time_to_expiry: float = None
    ) -> dict:
        """
        Calculate option price and Greeks using Black-Scholes model.

        Args:
            spot_price: Current spot price (uses self.spot_price if None)
            time_to_expiry: Time to expiry in years (calculated if None)

        Returns:
            Dictionary with option price and Greeks:
            - Spot: Current spot price
            - T_Years: Time to expiry in years
            - Price: Option price
            - Delta: Delta value
            - Gamma: Gamma value
            - Vega (1%): Vega for 1% volatility change
            - Theta: Theta value (daily time decay)
            - Status: 'Expired' if expired (optional)
        """
        S = spot_price or self.spot_price
        K = self.strike_price
        T = time_to_expiry if time_to_expiry is not None else self.calculate_time_to_expiry()
        r = self.risk_free_rate
        sigma = self.volatility

        # Handle expired options
        if T <= 0:
            price = max(S - K, 0.0) if self.option_type == 'call' else max(K - S, 0.0)
            return {
                "Spot": round(S, 2),
                "T_Years": 0,
                "Price": price,
                "Delta": 0,
                "Gamma": 0,
                "Vega (1%)": 0,
                "Status": "Expired"
            }

        # Black-Scholes calculations
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Calculate price and delta based on option type
        if self.option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
            delta = norm.cdf(d1)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
            delta = norm.cdf(d1) - 1

        # Calculate Greeks
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))

        return {
            "Spot": round(S, 2),
            "T_Years": round(T, 6),
            "Price": round(price, 4),
            "Delta": round(delta, 4),
            "Gamma": round(gamma, 4),
            "Vega (1%)": round(vega / 100, 4),
            "Theta": round(theta, 4)
        }

    def plot_option_values(self, days: int = 10, num_points: int = 50) -> None:
        """
        Plot option values over the next specified days.

        Args:
            days: Number of days to plot (default: 10)
            num_points: Number of data points (default: 50)

        Creates and saves a plot as 'option_values_plot.png'
        """
        current_date = datetime.now(timezone.utc)
        dates = [
            current_date + timedelta(days=i)
            for i in np.linspace(0, days, num_points)
        ]
        prices = []

        for date in dates:
            T = self.calculate_time_to_expiry(date.strftime("%Y-%m-%d"))
            greeks = self.calculate_greeks(time_to_expiry=T)
            prices.append(greeks["Price"])

        plt.figure(figsize=(12, 6))
        plt.plot(
            range(len(dates)),
            prices,
            linewidth=2,
            color='blue',
            label=f'{self.option_type.upper()} Option'
        )
        plt.xlabel('Days from Today', fontsize=12)
        plt.ylabel('Option Price ($)', fontsize=12)
        plt.title(
            f'{self.ticker_symbol} {self.option_type.upper()} Option Value Over {days} Days\n'
            f'Strike: ${self.strike_price} | Spot: ${self.spot_price:.2f} | '
            f'Volatility: {self.volatility*100:.1f}%',
            fontsize=13,
            fontweight='bold'
        )
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('option_values_plot.png', dpi=300)
        print(f"\nPlot saved as 'option_values_plot.png'")
        plt.show()

    def display_greeks(self) -> None:
        """Display current Greeks for the option."""
        greeks = self.calculate_greeks()
        print(f"\n{'='*60}")
        print(f"Ticker: {self.ticker_symbol} | Option Type: {self.option_type.upper()}")
        print(f"Strike: ${self.strike_price} | Expiry: {self.expiry_date}")
        print(f"{'='*60}")
        for key, value in greeks.items():
            print(f"{key:.<20} {value}")
        print(f"{'='*60}\n")

