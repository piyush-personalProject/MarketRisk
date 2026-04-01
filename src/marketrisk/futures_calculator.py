"""Futures Options Greeks Calculator using Black76 model."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime, timedelta, timezone


class FuturesOptionsCalculator:
    """Calculate Greeks for futures options using Black76 model.

    Black76 model is used for pricing options on futures contracts.
    Unlike Black-Scholes which uses spot price, Black76 uses the futures price.
    """

    def __init__(
        self,
        futures_price: float,
        strike_price: float,
        expiry_date: str,
        risk_free_rate: float = 0.045,
        volatility: float = 0.25,
        option_type: str = 'call'
    ):
        """
        Initialize the futures options calculator with Black76 model.

        Args:
            futures_price: Current futures contract price (F)
            strike_price: Strike price of the option (K)
            expiry_date: Expiry date in format 'YYYY-MM-DD'
            risk_free_rate: Risk-free rate (default 0.045 = 4.5%)
            volatility: Implied volatility (default 0.25 = 25%)
            option_type: 'call' or 'put' (default: 'call')

        Note:
            - Black76 does NOT use dividend yield (already embedded in futures price)
            - Works for commodity futures, interest rate futures, currency futures
        """
        self.futures_price = futures_price
        self.strike_price = strike_price
        self.expiry_date = expiry_date
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.option_type = option_type.lower()

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
        futures_price: float = None,
        time_to_expiry: float = None
    ) -> dict:
        """
        Calculate option price and Greeks using Black76 model.

        The Black76 model formulas:
        d1 = [ln(F/K) + (σ²/2)*T] / (σ*√T)
        d2 = d1 - σ*√T

        Call Price: C = e^(-r*T) * [F*N(d1) - K*N(d2)]
        Put Price:  P = e^(-r*T) * [K*N(-d2) - F*N(-d1)]

        Args:
            futures_price: Futures price (uses self.futures_price if None)
            time_to_expiry: Time to expiry in years (calculated if None)

        Returns:
            Dictionary with option price and Greeks:
            - Futures Price: Current futures price
            - Strike: Strike price
            - T_Years: Time to expiry in years
            - Price: Option price
            - Delta: Delta value
            - Gamma: Gamma value
            - Vega (1%): Vega for 1% volatility change
            - Theta: Theta value (daily time decay)
            - Model: 'Black76'
        """
        F = futures_price or self.futures_price
        K = self.strike_price
        T = time_to_expiry if time_to_expiry is not None else self.calculate_time_to_expiry()
        r = self.risk_free_rate
        sigma = self.volatility

        # Handle expired options
        if T <= 0:
            price = max(F - K, 0.0) if self.option_type == 'call' else max(K - F, 0.0)
            return {
                "Futures Price": round(F, 2),
                "Strike": round(K, 2),
                "T_Years": 0,
                "Price": price,
                "Delta": 0,
                "Gamma": 0,
                "Vega (1%)": 0,
                "Theta": 0,
                "Model": "Black76",
                "Status": "Expired"
            }

        # Black76 calculations
        # d1 = [ln(F/K) + (σ²/2)*T] / (σ*√T)
        d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Discount factor
        discount = np.exp(-r * T)

        # Calculate price and delta based on option type
        if self.option_type == 'call':
            # Call: C = e^(-r*T) * [F*N(d1) - K*N(d2)]
            price = discount * (F * norm.cdf(d1) - K * norm.cdf(d2))
            # Call Delta: Δ = e^(-r*T) * N(d1)
            delta = discount * norm.cdf(d1)
        else:
            # Put: P = e^(-r*T) * [K*N(-d2) - F*N(-d1)]
            price = discount * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
            # Put Delta: Δ = -e^(-r*T) * N(-d1)
            delta = -discount * norm.cdf(-d1)

        # Greeks (all discounted by e^(-r*T))
        # Gamma: Γ = e^(-r*T) * N'(d1) / (F * σ * √T)
        gamma = discount * norm.pdf(d1) / (F * sigma * np.sqrt(T))

        # Vega: ν = e^(-r*T) * F * N'(d1) * √T (for 1% change)
        vega = discount * F * norm.pdf(d1) * np.sqrt(T)

        # Theta (per day)
        if self.option_type == 'call':
            theta = (-discount * F * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) +
                    r * discount * F * norm.cdf(d1) -
                    r * discount * K * norm.cdf(d2)) / 365
        else:
            theta = (-discount * F * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) -
                    r * discount * F * norm.cdf(-d1) +
                    r * discount * K * norm.cdf(-d2)) / 365

        return {
            "Futures Price": round(F, 2),
            "Strike": round(K, 2),
            "T_Years": round(T, 6),
            "Price": round(price, 4),
            "Delta": round(delta, 4),
            "Gamma": round(gamma, 4),
            "Vega (1%)": round(vega / 100, 4),
            "Theta": round(theta, 4),
            "Model": "Black76"
        }

    def display_greeks(self) -> None:
        """Display current Greeks for the futures option."""
        greeks = self.calculate_greeks()
        print(f"\n{'='*60}")
        print(f"Futures Options Calculator - Black76 Model")
        print(f"Futures Price: {self.futures_price} | Strike: {self.strike_price}")
        print(f"Option Type: {self.option_type.upper()} | Expiry: {self.expiry_date}")
        print(f"{'='*60}")
        for key, value in greeks.items():
            if key != "Model":
                print(f"{key:.<25} {value}")
        print(f"{'='*60}\n")

    def plot_option_values(self, days: int = 10, num_points: int = 50) -> None:
        """
        Plot futures option values over time.

        Args:
            days: Number of days to plot (default: 10)
            num_points: Number of data points (default: 50)

        Creates and saves a plot as 'futures_option_values_plot.png'
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
            color='green',
            label=f'{self.option_type.upper()} Option (Black76)'
        )
        plt.xlabel('Days from Today', fontsize=12)
        plt.ylabel('Option Price', fontsize=12)
        plt.title(
            f'Futures {self.option_type.upper()} Option Value Over {days} Days\n'
            f'Futures: {self.futures_price} | Strike: {self.strike_price} | '
            f'Volatility: {self.volatility*100:.1f}%',
            fontsize=13,
            fontweight='bold'
        )
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('futures_option_values_plot.png', dpi=300)
        print(f"\nPlot saved as 'futures_option_values_plot.png'")
        plt.show()

