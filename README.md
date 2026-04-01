# MarketRisk - Options Greeks Calculator

A professional-grade Python library for calculating options Greeks (Delta, Gamma, Vega, Theta) using industry-standard models:
- **Black-Scholes Model** for equity and stock options
- **Black76 Model** for futures and forward contracts

Features real-time stock data, comprehensive Greeks calculation, and professional visualization.

## Features

### Equity Options (Black-Scholes)
- ✅ **Black-Scholes Pricing**: Accurate pricing for stocks and equities
- ✅ **Dividend Support**: Handles continuous dividend yields
- ✅ **Real-Time Data**: Fetches current stock prices from Yahoo Finance
- ✅ **All Greeks**: Delta, Gamma, Vega, Theta calculations

### Futures Options (Black76)
- ✅ **Black76 Pricing**: Industry-standard model for futures
- ✅ **Multiple Assets**: Commodity, Interest Rate, Currency, Index futures
- ✅ **Direct Price Input**: No need for real-time data fetch
- ✅ **All Greeks**: Properly discounted for futures

### General Features
- **Visualization**: Generate professional plots of option values over time
- **Easy to Use**: Simple API with sensible defaults
- **Dual CLI**: Menu-driven command-line interface for both models
- **Well Tested**: 45+ unit tests with comprehensive coverage
- **Type Hints**: Full type hints for IDE support
- **Production Ready**: Industry-standard implementations

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**
   ```bash
   cd MarketRisk
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows:
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux:
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install as package** (recommended)
   ```bash
   pip install -e .
   ```

5. **Verify installation**
   ```bash
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

## Quick Start

### Equity Options - Using Real Stock Data

```python
from marketrisk import EquityOptionsCalculator

# Apple call option with dividend
calc = EquityOptionsCalculator(
    ticker_symbol='AAPL',
    strike_price=150,
    expiry_date='2026-06-19',
    volatility=0.25,
    dividend_yield=0.005,  # 0.5% dividend
    option_type='call'
)

# Calculate and display Greeks
greeks = calc.calculate_greeks()
calc.display_greeks()
calc.plot_option_values(days=30)
```

### Futures Options - Direct Price Input

```python
from marketrisk import FuturesOptionsCalculator

# Crude oil futures call option
calc = FuturesOptionsCalculator(
    futures_price=75.50,
    strike_price=75.0,
    expiry_date='2026-06-19',
    volatility=0.35,  # Typical commodity volatility
    option_type='call'
)

greeks = calc.calculate_greeks()
calc.display_greeks()
calc.plot_option_values(days=30)
```

### Command-Line Interface

```bash
# Interactive menu
python -m marketrisk.cli
# or
marketrisk

# Menu:
# 1. Equity/Stock Options (Black-Scholes)
# 2. Futures Options (Black76)
# 0. Exit
```

## API Reference

### EquityOptionsCalculator (Black-Scholes)

For pricing equity and stock options with real-time data.

#### Constructor

```python
from marketrisk import EquityOptionsCalculator

EquityOptionsCalculator(
    ticker_symbol: str,
    strike_price: float,
    expiry_date: str,
    risk_free_rate: float = 0.045,
    volatility: float = 0.25,
    option_type: str = 'call',
    dividend_yield: float = 0.0
)
```

**Parameters:**
- `ticker_symbol`: Stock ticker symbol (e.g., 'AAPL', 'IBM')
- `strike_price`: Strike price of the option
- `expiry_date`: Expiration date in 'YYYY-MM-DD' format
- `risk_free_rate`: Annual risk-free rate (default: 0.045 = 4.5%)
- `volatility`: Implied volatility (default: 0.25 = 25%)
- `option_type`: 'call' or 'put' (default: 'call')
- `dividend_yield`: Continuous dividend yield (default: 0.0 = no dividend)

#### Methods

##### calculate_greeks(spot_price=None, time_to_expiry=None, dividend_yield=None)

Calculate option price and Greeks using Black-Scholes model.

**Returns:** Dictionary with:
- `Spot`: Current spot price
- `T_Years`: Time to expiry in years
- `Price`: Option price
- `Delta`: Delta value (-1 to 1)
- `Gamma`: Gamma value (curvature)
- `Vega (1%)`: Vega for 1% volatility change
- `Theta`: Theta value (daily time decay)
- `Dividend Yield`: Applied dividend yield
- `Status`: 'Expired' if expired

##### display_greeks()

Print formatted Greeks to console.

##### plot_option_values(days=10, num_points=50)

Generate and save a plot of option values over time.

**Output:** Saves as 'option_values_plot.png'

---

### FuturesOptionsCalculator (Black76)

For pricing futures and forward contract options.

#### Constructor

```python
from marketrisk import FuturesOptionsCalculator

FuturesOptionsCalculator(
    futures_price: float,
    strike_price: float,
    expiry_date: str,
    risk_free_rate: float = 0.045,
    volatility: float = 0.25,
    option_type: str = 'call'
)
```

**Parameters:**
- `futures_price`: Current futures contract price
- `strike_price`: Strike price of the option
- `expiry_date`: Expiration date in 'YYYY-MM-DD' format
- `risk_free_rate`: Annual risk-free rate (default: 0.045 = 4.5%)
- `volatility`: Implied volatility (default: 0.25 = 25%)
- `option_type`: 'call' or 'put' (default: 'call')

**Note:** Black76 does NOT use dividend yield (already embedded in futures price)

#### Methods

##### calculate_greeks(futures_price=None, time_to_expiry=None)

Calculate option price and Greeks using Black76 model.

**Returns:** Dictionary with:
- `Futures Price`: Current futures price
- `Strike`: Strike price
- `T_Years`: Time to expiry in years
- `Price`: Option price
- `Delta`: Delta value
- `Gamma`: Gamma value
- `Vega (1%)`: Vega for 1% volatility change
- `Theta`: Theta value (daily time decay)
- `Model`: 'Black76' identifier

##### display_greeks()

Print formatted Greeks to console.

##### plot_option_values(days=10, num_points=50)

Generate and save a plot of option values over time.

**Output:** Saves as 'futures_option_values_plot.png'

---

## Backward Compatibility

The old class name `OptionsGreeksCalculator` is still available as an alias:

```python
# Old import (still works)
from marketrisk import OptionsGreeksCalculator

# New explicit import (recommended)
from marketrisk import EquityOptionsCalculator
```

Both work identically - use whichever you prefer.

## Testing

Run the test suite:

```bash
# Using unittest (built-in)
python -m unittest discover -s tests -p "test_*.py" -v

# Using pytest (if installed)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/marketrisk --cov-report=html
```

## Project Structure

```
MarketRisk/
├── src/
│   └── marketrisk/
│       ├── __init__.py
│       ├── calculator.py          # Main calculator class
│       ├── cli.py                 # Command-line interface
│       └── utils.py               # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py         # Calculator unit tests
│   └── fixtures/                  # Test fixtures and data
├── docs/
│   ├── INSTALL.md                 # Installation guide
│   ├── USAGE.md                   # Detailed usage guide
│   └── API.md                     # API documentation
├── README.md                       # This file
├── CHANGELOG.md                    # Version history
├── setup.py                        # Package configuration
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
└── .gitignore                      # Git ignore rules
```

## Dependencies

### Production
- **numpy** - Numerical computing
- **scipy** - Scientific computing (normal distribution)
- **yfinance** - Yahoo Finance data (for equity options only)
- **matplotlib** - Plotting and visualization
- **pandas** - Data manipulation

### Development
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **sphinx** - Documentation generation

## Models Comparison

| Feature | Black-Scholes (Equity) | Black76 (Futures) |
|---------|---|---|
| **Use For** | Stocks, equities | Futures, forwards |
| **Input** | Ticker symbol | Futures price |
| **Real-Time Data** | Yes (Yahoo Finance) | No (direct input) |
| **Dividend Yield** | ✓ Supported | ✗ Not used |
| **Cost of Carry** | Manual (dividend) | Built-in |
| **Class** | EquityOptionsCalculator | FuturesOptionsCalculator |
| **Asset Classes** | Stocks | Commodities, FX, Bonds, Indices |

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'marketrisk'"
**Solution**: Install the package in development mode:
```bash
pip install -e .
```

### Issue: "yfinance connection error" (Equity options only)
**Solution**: Check internet connection and verify Yahoo Finance is accessible.

### Issue: "ValueError: Could not fetch data for TICKER"
**Solution**: Verify the ticker symbol is valid (e.g., AAPL, MSFT, GOOGL).

### Issue: Tests failing
**Solution**: Install all dependencies and run tests:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

## Development

### Setting up development environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all dependencies (production + dev)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

### Code quality checks

```bash
# Format code with Black
black src/ tests/

# Check code style with Flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/

# Run tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run tests with coverage report
pytest tests/ --cov=src/marketrisk --cov-report=html
```

## Mathematical Models

### Black-Scholes Model (Equity Options)

For pricing European options on dividend-paying stocks:

**Call Price**: C = S*e^(-q*T)*N(d₁) - K*e^(-r*T)*N(d₂)
**Put Price**: P = K*e^(-r*T)*N(-d₂) - S*e^(-q*T)*N(-d₁)

Where:
- S = Spot price
- K = Strike price
- r = Risk-free rate
- q = Dividend yield
- T = Time to expiry
- σ = Volatility
- d₁ = [ln(S/K) + (r - q + σ²/2)*T] / (σ*√T)
- d₂ = d₁ - σ*√T
- N(x) = Cumulative normal distribution

### Black76 Model (Futures Options)

For pricing options on futures and forward contracts:

**Call Price**: C = e^(-r*T) * [F*N(d₁) - K*N(d₂)]
**Put Price**: P = e^(-r*T) * [K*N(-d₂) - F*N(-d₁)]

Where:
- F = Futures price
- K = Strike price
- r = Risk-free rate
- T = Time to expiry
- σ = Volatility
- d₁ = [ln(F/K) + (σ²/2)*T] / (σ*√T)
- d₂ = d₁ - σ*√T
- N(x) = Cumulative normal distribution

### Greeks Definitions

- **Delta (Δ)**: Sensitivity of option price to spot/futures price changes (-1 to 1)
- **Gamma (Γ)**: Rate of change of delta (curvature of price curve)
- **Vega (ν)**: Sensitivity to volatility changes (per 1% volatility change)
- **Theta (Θ)**: Time decay (daily rate, typically negative for long options)
- **Rho (ρ)**: Sensitivity to interest rate changes

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guide
4. Add tests for new features
5. Submit a pull request

## Support

For issues or questions:
1. Check the [Issues](https://github.com/yourusername/marketrisk/issues) page
2. Review the documentation in `docs/`
3. Contact the project maintainer

## Changelog

### Version 1.0.0
- Initial release
- Black-Scholes option pricing
- Greeks calculation
- Real-time data fetching
- Visualization support
- Comprehensive test suite

