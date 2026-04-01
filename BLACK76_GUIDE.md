# Black76 Model for Futures Options

## Overview

The Black76 model (also known as Black's model) is used to price options on **futures contracts** and forward contracts. It's an extension of the Black-Scholes model adapted for futures and forwards.

---

## Key Differences: Black-Scholes vs Black76

### Black-Scholes (Equity Options)
```
Input: Spot Price (S)
Formula: C = S*e^(-q*T)*N(d1) - K*e^(-r*T)*N(d2)
Underlying: Stock with dividend yield
```

### Black76 (Futures Options)
```
Input: Futures Price (F)
Formula: C = e^(-r*T) * [F*N(d1) - K*N(d2)]
Underlying: Futures contract (no dividend yield)
```

---

## Mathematical Model

### Black76 Formula

```
d1 = [ln(F/K) + (σ²/2)*T] / (σ*√T)
d2 = d1 - σ*√T

Call Price:  C = e^(-r*T) * [F*N(d1) - K*N(d2)]
Put Price:   P = e^(-r*T) * [K*N(-d2) - F*N(-d1)]
```

Where:
- **F** = Futures price
- **K** = Strike price
- **T** = Time to expiry (in years)
- **r** = Risk-free rate
- **σ** = Volatility
- **N(x)** = Cumulative normal distribution

### Greeks in Black76

```
Delta (Call):  Δ = e^(-r*T) * N(d1)
Delta (Put):   Δ = -e^(-r*T) * N(-d1)

Gamma:  Γ = e^(-r*T) * N'(d1) / (F * σ * √T)
Vega:   ν = e^(-r*T) * F * N'(d1) * √T
Theta:  Θ = [Discount factor effects on d1, d2]
```

---

## When to Use Black76

### ✅ Perfect For:
1. **Commodity Futures**
   - Crude oil futures options
   - Natural gas futures
   - Agricultural futures (corn, wheat, soybeans)
   - Gold/silver futures

2. **Interest Rate Futures**
   - Bond futures options
   - Treasury futures
   - Eurodollar futures

3. **Currency Futures**
   - FX futures options
   - Cross-currency futures

4. **Index Futures**
   - Stock index futures options
   - Equity index derivatives

5. **Forward Contracts**
   - Options on forwards
   - Contingent forward agreements

### ❌ NOT for:
- Stock options (use Black-Scholes)
- Options on stocks with dividends

---

## Implementation Examples

### Example 1: Crude Oil Futures Option

```python
from marketrisk import FuturesOptionsCalculator

# Crude oil futures trading at $75.50, Call on $75 strike
calc = FuturesOptionsCalculator(
    futures_price=75.50,
    strike_price=75.0,
    expiry_date='2026-06-19',
    volatility=0.35,      # 35% volatility (typical for commodities)
    risk_free_rate=0.04,
    option_type='call'
)

greeks = calc.calculate_greeks()
print(f"Call Price: ${greeks['Price']:.4f}")
print(f"Delta: {greeks['Delta']:.4f}")
print(f"Vega: {greeks['Vega (1%)']:.4f}")
```

### Example 2: Bond Futures Option

```python
# Treasury bond futures at 130.50, Put on 130 strike
calc = FuturesOptionsCalculator(
    futures_price=130.50,
    strike_price=130.0,
    expiry_date='2026-09-30',
    volatility=0.08,       # 8% volatility (lower for bonds)
    risk_free_rate=0.04,
    option_type='put'
)

greeks = calc.calculate_greeks()
calc.display_greeks()
```

### Example 3: FX Futures Option

```python
# EUR/USD futures at 1.2050, Call on 1.20 strike
calc = FuturesOptionsCalculator(
    futures_price=1.2050,
    strike_price=1.20,
    expiry_date='2026-06-30',
    volatility=0.12,       # 12% volatility (FX)
    risk_free_rate=0.03,
    option_type='call'
)

greeks = calc.calculate_greeks()
```

---

## Key Advantages of Black76

1. **No Dividend Handling**: Dividend yield already embedded in futures price
2. **Forward Contracts**: Works for forwards and futures
3. **Simplicity**: Fewer parameters than Black-Scholes
4. **Accuracy**: Better suited for commodity and interest rate derivatives
5. **Consistency**: Standard in industry for derivatives pricing

---

## Comparison: Black76 vs Black-Scholes for Equities

### When Futures Price = Spot Price (with no dividend)

```python
# Spot price scenario
spot_option_price = 2.50    # Black-Scholes
futures_option_price = 2.47 # Black76

# Results should be very similar (accounting for discounting)
```

The main difference is in discounting and handling of the underlying.

---

## Greeks Behavior in Black76

### Delta
- **Call**: Ranges from 0 to e^(-r*T) (max of discounted 1)
- **Put**: Ranges from -e^(-r*T) to 0
- Changes based on moneyness and time decay

### Gamma
- Always positive for both calls and puts
- Peaks at ATM options
- Decreases as option goes deeper ITM/OTM

### Vega
- Positive for both calls and puts
- Measures sensitivity to 1% volatility change
- Peaks at ATM options

### Theta
- **Calls**: Generally negative (time decay)
- **Puts**: Can be positive or negative
- Depends on moneyness and discounting

---

## Volatility Considerations

### Typical Volatility Ranges by Asset Class

| Asset Class | Typical Volatility | Range |
|------------|-------------------|-------|
| Crude Oil | 30-40% | 20-50% |
| Natural Gas | 40-60% | 30-80% |
| Gold | 15-25% | 10-40% |
| Bonds (Futures) | 5-15% | 2-20% |
| Currencies | 8-15% | 5-20% |
| Equity Index Futures | 15-25% | 10-40% |

---

## API Reference

### FuturesOptionsCalculator Class

```python
calc = FuturesOptionsCalculator(
    futures_price: float,      # Current futures contract price
    strike_price: float,       # Strike price
    expiry_date: str,         # 'YYYY-MM-DD' format
    risk_free_rate: float = 0.045,  # Annual rate
    volatility: float = 0.25,       # As decimal (0.25 = 25%)
    option_type: str = 'call'       # 'call' or 'put'
)
```

### Methods

```python
# Calculate Greeks
greeks = calc.calculate_greeks(
    futures_price=None,    # Override current price
    time_to_expiry=None    # Override time
)

# Display formatted output
calc.display_greeks()

# Plot option values over time
calc.plot_option_values(days=10, num_points=50)
```

### Output Dictionary

```python
{
    'Futures Price': 75.50,      # Current futures price
    'Strike': 75.0,              # Strike price
    'T_Years': 0.102,            # Time to expiry
    'Price': 2.3456,             # Option price
    'Delta': 0.5234,             # Delta
    'Gamma': 0.0145,             # Gamma
    'Vega (1%)': 0.3456,         # Vega per 1% volatility
    'Theta': -0.0234,            # Theta (daily decay)
    'Model': 'Black76'           # Model identifier
}
```

---

## Important Notes

### 1. NO Dividend Yield in Black76
- Black76 does NOT have dividend_yield parameter
- Dividend yield is already embedded in futures price
- Use Black-Scholes for dividend-paying stocks

### 2. Futures Price Already Includes:
- Cost of carry
- Storage costs
- Convenience yield
- Interest rates
- Dividends

### 3. Interest Rate Effects
- Black76 discounts by e^(-r*T)
- Fully accounts for time value
- Risk-free rate is critical for pricing

### 4. Practical Considerations
- Use market futures prices (not spot + carry calculation)
- Volatility should be historically calibrated
- Consider bid-ask spreads in real trading

---

## Testing Coverage

The implementation includes comprehensive tests for:
- ✓ ATM, ITM, OTM options
- ✓ Call and put options
- ✓ Expired options
- ✓ Custom spot price and time
- ✓ Volatility impact
- ✓ Put-call parity validation
- ✓ Commodity, FX, and interest rate futures
- ✓ Comparison with Black-Scholes

---

## Files

- **src/marketrisk/futures_calculator.py** - Implementation
- **tests/test_futures_calculator.py** - Test suite
- **src/marketrisk/__init__.py** - Public API

---

## Usage Examples in Code

```python
from marketrisk import FuturesOptionsCalculator

# Example: Crude oil call option
calc = FuturesOptionsCalculator(
    futures_price=75.50,
    strike_price=75.0,
    expiry_date='2026-06-19',
    volatility=0.35,
    option_type='call'
)

greeks = calc.calculate_greeks()
calc.display_greeks()
calc.plot_option_values(days=30, num_points=100)
```

---

## Summary

Black76 is the **standard model for futures and forward options**:
- ✅ No dividend complications
- ✅ Simpler than Black-Scholes for futures
- ✅ Works for all liquid futures contracts
- ✅ Industry standard
- ✅ Well-tested and validated

Use **Black76** for futures, **Black-Scholes** for stocks! 🚀

