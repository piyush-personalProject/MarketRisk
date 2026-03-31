# MarketRisk - Options Greeks Calculator

A professional-grade Python library for calculating options Greeks (Delta, Gamma, Vega, Theta) using the Black-Scholes model. Fetches real-time stock data and visualizes option values over time.

## Features

- **Black-Scholes Pricing**: Accurate option pricing using the Black-Scholes model
- **Greeks Calculation**: Compute Delta, Gamma, Vega, and Theta for both call and put options
- **Real-Time Data**: Fetch current stock prices from Yahoo Finance
- **Visualization**: Generate professional plots of option values over time
- **Easy to Use**: Simple API with sensible defaults
- **Well Tested**: Comprehensive unit test suite with good coverage
- **Type Hints**: Full type hints for IDE support

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

4. **Verify installation**
   ```bash
   python -m pytest tests/ -v
   ```

## Usage

### As a Library

```python
from marketrisk.calculator import OptionsGreeksCalculator

# Create a calculator instance
calc = OptionsGreeksCalculator(
    ticker_symbol='AAPL',
    strike_price=150,
    expiry_date='2026-06-19',
    volatility=0.25,
    risk_free_rate=0.045,
    option_type='call'
)

# Calculate Greeks
greeks = calc.calculate_greeks()
print(greeks)

# Display formatted output
calc.display_greeks()

# Generate plot
calc.plot_option_values(days=10, num_points=50)
```

### As a Command-Line Tool

```bash
# Run interactive calculator
python -m marketrisk.cli

# Or if installed as a package:
marketrisk
```

When prompted, enter:
- **Ticker Symbol**: Stock ticker (e.g., AAPL, MSFT, GOOGL)
- **Strike Price**: Strike price of the option
- **Expiry Date**: Option expiration date (YYYY-MM-DD format)
- **Volatility**: Implied volatility as a decimal (default: 0.25 = 25%)
- **Risk-Free Rate**: Risk-free rate as a decimal (default: 0.045 = 4.5%)
- **Option Type**: 'call' or 'put'

## API Reference

### OptionsGreeksCalculator

#### Constructor

```python
OptionsGreeksCalculator(
    ticker_symbol: str,
    strike_price: float,
    expiry_date: str,
    risk_free_rate: float = 0.045,
    volatility: float = 0.25,
    option_type: str = 'call'
)
```

**Parameters:**
- `ticker_symbol`: Stock ticker symbol (e.g., 'AAPL')
- `strike_price`: Strike price of the option
- `expiry_date`: Expiration date in 'YYYY-MM-DD' format
- `risk_free_rate`: Annual risk-free rate (default: 0.045)
- `volatility`: Implied volatility (default: 0.25)
- `option_type`: 'call' or 'put' (default: 'call')

#### Methods

##### calculate_greeks(spot_price=None, time_to_expiry=None)

Calculate option price and Greeks.

**Returns:** Dictionary with keys:
- `Spot`: Current spot price
- `T_Years`: Time to expiry in years
- `Price`: Option price
- `Delta`: Delta value
- `Gamma`: Gamma value
- `Vega (1%)`: Vega for 1% volatility change
- `Theta`: Theta value (daily time decay)
- `Status`: 'Expired' if expired, otherwise not present

##### calculate_time_to_expiry(date_str=None)

Calculate time to expiration in years.

**Returns:** float (years to expiry, minimum 0)

##### display_greeks()

Print formatted Greeks to console.

##### plot_option_values(days=10, num_points=50)

Generate and save a plot of option values over time.

**Parameters:**
- `days`: Number of days to plot (default: 10)
- `num_points`: Number of data points (default: 50)

**Output:** Saves plot as 'option_values_plot.png'

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
- **yfinance** - Yahoo Finance data fetching
- **matplotlib** - Plotting and visualization
- **scipy** - Scientific computing (normal distribution)
- **pandas** - Data manipulation

### Development
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking

## Troubleshooting

### Issue: "yfinance connection error"
**Solution**: Check your internet connection and verify Yahoo Finance is accessible.

### Issue: "ValueError: Could not fetch data for TICKER"
**Solution**: Verify the ticker symbol is valid (e.g., AAPL, MSFT, GOOGL).

### Issue: Import errors
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
pip list
pip install -r requirements.txt --upgrade
```

### Issue: Tests failing
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
python -m pytest tests/ -v
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

# Install dev dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .
```

### Code quality checks

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Run tests with coverage
pytest tests/ --cov=src/marketrisk --cov-report=html
```

## Mathematical Background

### Black-Scholes Model

The calculator uses the Black-Scholes-Merton model for option pricing:

**Call Price**: C = S₀N(d₁) - Ke^(-rT)N(d₂)

**Put Price**: P = Ke^(-rT)N(-d₂) - S₀N(-d₁)

Where:
- d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)
- d₂ = d₁ - σ√T
- N(x) = Cumulative normal distribution

### Greeks Definitions

- **Delta**: Rate of change of option price with respect to spot price
- **Gamma**: Rate of change of delta with respect to spot price
- **Vega**: Sensitivity to volatility changes (per 1% change)
- **Theta**: Time decay (daily rate)
- **Rho**: Sensitivity to interest rate changes

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

