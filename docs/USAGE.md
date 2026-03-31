# Usage Guide - MarketRisk Options Greeks Calculator

## Table of Contents

1. [Running as a Script](#running-as-a-script)
2. [Using as a Library](#using-as-a-library)
3. [API Reference](#api-reference)
4. [Examples](#examples)
5. [Advanced Usage](#advanced-usage)

## Running as a Script

### Interactive Calculator

Run the interactive command-line calculator:

```bash
python -m marketrisk.cli
```

Or if installed as a package:

```bash
marketrisk
```

### Input Prompts

When you run the calculator, you'll be prompted for:

1. **Ticker Symbol** (default: AAPL)
   - Examples: AAPL, MSFT, GOOGL, TSLA
   - Must be a valid stock ticker on Yahoo Finance

2. **Strike Price** (default: 180)
   - The exercise price of the option
   - Typically a positive number

3. **Expiry Date** (default: 2026-06-19)
   - Format: YYYY-MM-DD
   - Must be a future date

4. **Volatility** (default: 0.25)
   - Implied volatility as a decimal
   - Example: 0.25 means 25% volatility

5. **Risk-Free Rate** (default: 0.045)
   - Annual risk-free rate as a decimal
   - Example: 0.045 means 4.5% interest rate

6. **Option Type** (default: call)
   - Enter either 'call' or 'put'

### Example Run

```
Options Greeks Calculator & Plotter

Enter ticker symbol (default: AAPL): AAPL
Enter strike price (default: 180): 180
Enter expiry date in YYYY-MM-DD format (default: 2026-06-19): 2026-06-19
Enter volatility as decimal (default: 0.25): 0.25
Enter risk-free rate as decimal (default: 0.045): 0.045
Enter option type 'call' or 'put' (default: call): call

============================================================
Ticker: AAPL | Option Type: CALL
Strike: $180 | Expiry: 2026-06-19
============================================================
Spot:........................ 180.45
T_Years:.................... 0.23808
Price:....................... 12.3456
Delta:....................... 0.6234
Gamma:....................... 0.0123
Vega (1%):................... 0.4567
Theta:....................... -0.0123
============================================================

Plot saved as 'option_values_plot.png'
```

## Using as a Library

### Basic Usage

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

# Get the Greeks
greeks = calc.calculate_greeks()
print(greeks)
# Output: {
#     'Spot': 180.45,
#     'T_Years': 0.238082,
#     'Price': 12.3456,
#     'Delta': 0.6234,
#     'Gamma': 0.0123,
#     'Vega (1%)': 0.4567,
#     'Theta': -0.0123
# }
```

### Display Formatted Output

```python
calc.display_greeks()
```

### Generate a Plot

```python
calc.plot_option_values(days=10, num_points=50)
```

This saves a high-quality plot as `option_values_plot.png`.

## API Reference

### OptionsGreeksCalculator Class

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
- `ticker_symbol` (str): Stock ticker symbol (e.g., 'AAPL')
- `strike_price` (float): Strike price of the option
- `expiry_date` (str): Expiration date in 'YYYY-MM-DD' format
- `risk_free_rate` (float, optional): Annual risk-free rate (default: 0.045)
- `volatility` (float, optional): Implied volatility (default: 0.25)
- `option_type` (str, optional): 'call' or 'put' (default: 'call')

**Raises:**
- `ValueError`: If ticker data cannot be fetched

#### Methods

##### `calculate_greeks(spot_price=None, time_to_expiry=None)`

Calculate option price and Greeks using Black-Scholes model.

```python
greeks = calc.calculate_greeks()
greeks_custom = calc.calculate_greeks(spot_price=160, time_to_expiry=0.05)
```

**Parameters:**
- `spot_price` (float, optional): Override current spot price
- `time_to_expiry` (float, optional): Override time to expiry in years

**Returns:** Dictionary with keys:
- `Spot`: Current spot price
- `T_Years`: Time to expiry in years
- `Price`: Option price
- `Delta`: Delta value
- `Gamma`: Gamma value
- `Vega (1%)`: Vega for 1% volatility change
- `Theta`: Theta value (daily time decay)
- `Status`: 'Expired' (only if option has expired)

##### `calculate_time_to_expiry(date_str=None)`

Calculate time to expiration in years.

```python
T = calc.calculate_time_to_expiry()
T_custom = calc.calculate_time_to_expiry('2026-06-19')
```

**Parameters:**
- `date_str` (str, optional): Date in 'YYYY-MM-DD' format (uses expiry_date if None)

**Returns:** float - Time to expiry in years (minimum 0)

##### `display_greeks()`

Print formatted Greeks to console.

```python
calc.display_greeks()
```

##### `plot_option_values(days=10, num_points=50)`

Generate and save a plot of option values over time.

```python
calc.plot_option_values(days=10, num_points=50)
calc.plot_option_values(days=30, num_points=100)
```

**Parameters:**
- `days` (int, optional): Number of days to plot (default: 10)
- `num_points` (int, optional): Number of data points (default: 50)

**Output:** Saves plot as 'option_values_plot.png'

## Examples

### Example 1: Simple Call Option

```python
from marketrisk.calculator import OptionsGreeksCalculator

# Create calculator for AAPL call option
calc = OptionsGreeksCalculator(
    ticker_symbol='AAPL',
    strike_price=150,
    expiry_date='2026-06-19',
    option_type='call'
)

# Display Greeks
calc.display_greeks()

# Generate plot
calc.plot_option_values()
```

### Example 2: Put Option Comparison

```python
from marketrisk.calculator import OptionsGreeksCalculator

# Create put and call options with same parameters
call_calc = OptionsGreeksCalculator(
    ticker_symbol='MSFT',
    strike_price=350,
    expiry_date='2026-12-31',
    option_type='call'
)

put_calc = OptionsGreeksCalculator(
    ticker_symbol='MSFT',
    strike_price=350,
    expiry_date='2026-12-31',
    option_type='put'
)

# Compare Greeks
call_greeks = call_calc.calculate_greeks()
put_greeks = put_calc.calculate_greeks()

print(f"Call Delta: {call_greeks['Delta']}")
print(f"Put Delta:  {put_greeks['Delta']}")
print(f"Sum (Put-Call Parity): {call_greeks['Delta'] + put_greeks['Delta']}")
```

### Example 3: Sensitivity Analysis

```python
from marketrisk.calculator import OptionsGreeksCalculator

# Create a base calculator
calc = OptionsGreeksCalculator(
    ticker_symbol='GOOGL',
    strike_price=140,
    expiry_date='2026-09-30',
    option_type='call'
)

# Analyze sensitivity to spot price
base_price = calc.spot_price
greeks_low = calc.calculate_greeks(spot_price=base_price - 10)
greeks_base = calc.calculate_greeks(spot_price=base_price)
greeks_high = calc.calculate_greeks(spot_price=base_price + 10)

print(f"Price down 10:  {greeks_low['Price']}")
print(f"Base price:     {greeks_base['Price']}")
print(f"Price up 10:    {greeks_high['Price']}")
```

### Example 4: Volatility Impact

```python
from marketrisk.calculator import OptionsGreeksCalculator

# Compare different volatility levels
ticker = 'TSLA'
strike = 250
expiry = '2026-06-19'

for vol in [0.15, 0.25, 0.35, 0.50]:
    calc = OptionsGreeksCalculator(
        ticker_symbol=ticker,
        strike_price=strike,
        expiry_date=expiry,
        volatility=vol,
        option_type='call'
    )
    greeks = calc.calculate_greeks()
    print(f"Volatility {vol*100:.0f}% - Price: ${greeks['Price']:.4f}, Vega: {greeks['Vega (1%)']:.4f}")
```

## Advanced Usage

### Custom Spot Prices

```python
# Analyze what-if scenarios
calc = OptionsGreeksCalculator(
    ticker_symbol='AAPL',
    strike_price=150,
    expiry_date='2026-06-19'
)

# Get Greeks at different spot prices
for spot in [140, 145, 150, 155, 160]:
    greeks = calc.calculate_greeks(spot_price=spot)
    print(f"Spot ${spot}: Price=${greeks['Price']:.2f}, Delta={greeks['Delta']:.4f}")
```

### Custom Time to Expiry

```python
# Analyze theta decay
calc = OptionsGreeksCalculator(
    ticker_symbol='AAPL',
    strike_price=150,
    expiry_date='2026-06-19'
)

# Get Greeks at different times
for days in [30, 20, 10, 5, 1]:
    T = days / 365  # Convert days to years
    greeks = calc.calculate_greeks(time_to_expiry=T)
    print(f"{days} days to expiry: Price=${greeks['Price']:.2f}, Theta={greeks['Theta']:.4f}")
```

### Batch Processing

```python
# Analyze multiple options
tickers = ['AAPL', 'MSFT', 'GOOGL']
strike = 150
expiry = '2026-06-19'

results = {}
for ticker in tickers:
    calc = OptionsGreeksCalculator(
        ticker_symbol=ticker,
        strike_price=strike,
        expiry_date=expiry,
        option_type='call'
    )
    results[ticker] = calc.calculate_greeks()

# Print summary
for ticker, greeks in results.items():
    print(f"{ticker}: Price=${greeks['Price']:.2f}, Delta={greeks['Delta']:.4f}")
```

## Tips and Best Practices

1. **Always validate inputs**: Ensure ticker symbols are valid before creating calculators
2. **Handle errors gracefully**: Wrap calculator creation in try-except blocks
3. **Use virtual environments**: Keep your project dependencies isolated
4. **Update data regularly**: Real spot prices change; consider refreshing if needed
5. **Understand the limitations**: Black-Scholes assumes European options and constant volatility
6. **Save plots**: Always save generated plots for analysis
7. **Document your analysis**: Add comments explaining your calculations

## Getting Help

- Review the main [README.md](../README.md)
- Check [Installation Guide](INSTALL.md)
- Run unit tests for examples
- Refer to Black-Scholes theory resources online

