# Quick Start Guide

## For Users (Running the Calculator)

### 1. Setup (One-time)

```bash
# Navigate to project
cd MarketRisk

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### 2. Run Interactive Calculator

```bash
python -m marketrisk.cli
```

Or if you prefer (after installation):
```bash
marketrisk
```

Then answer the prompts:
```
Enter ticker symbol (default: AAPL): AAPL
Enter strike price (default: 180): 150
Enter expiry date in YYYY-MM-DD format (default: 2026-06-19): 2026-06-19
Enter volatility as decimal (default: 0.25): 0.25
Enter risk-free rate as decimal (default: 0.045): 0.045
Enter option type 'call' or 'put' (default: call): call
```

The calculator will:
- Display Greeks (Delta, Gamma, Vega, Theta)
- Generate a plot saved as `option_values_plot.png`

### 3. Use as a Library

```python
from marketrisk.calculator import OptionsGreeksCalculator

# Create calculator
calc = OptionsGreeksCalculator(
    ticker_symbol='AAPL',
    strike_price=150,
    expiry_date='2026-06-19',
    volatility=0.25,
    option_type='call'
)

# Calculate Greeks
greeks = calc.calculate_greeks()
print(greeks)

# Or display formatted
calc.display_greeks()

# Generate plot
calc.plot_option_values(days=10, num_points=50)
```

---

## For Developers (Contributing Code)

### 1. Setup Development Environment

```bash
cd MarketRisk

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install ALL dependencies (including dev tools)
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### 2. Run Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Or using pytest (if preferred)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/marketrisk --cov-report=html
```

### 3. Code Quality

```bash
# Format code with Black
black src/ tests/

# Check for linting issues
flake8 src/ tests/

# Type checking
mypy src/

# All in one
black src/ tests/ && flake8 src/ tests/ && mypy src/
```

### 4. Make Changes

Edit files in `src/marketrisk/`:
- `calculator.py` - Main calculator logic
- `cli.py` - Command-line interface
- `utils.py` - Helper functions

Add tests to `tests/test_calculator.py`

### 5. Test Your Changes

```bash
# Run tests
python -m unittest discover -s tests -p "test_*.py" -v

# Format code
black src/ tests/

# Check quality
flake8 src/ tests/
```

### 6. Update Documentation

- Edit `docs/USAGE.md` for usage examples
- Edit `docs/INSTALL.md` for setup instructions
- Add to `CHANGELOG.md` for version updates
- Update `README.md` if adding features

---

## Project Structure Reference

### Where to Find Things

| What | Where | File(s) |
|------|-------|---------|
| **Main Code** | `src/marketrisk/` | `calculator.py`, `cli.py`, `utils.py` |
| **Tests** | `tests/` | `test_calculator.py` |
| **Docs** | `docs/` | `INSTALL.md`, `USAGE.md` |
| **Config** | Root | `setup.py`, `pyproject.toml`, `requirements.txt` |
| **README** | Root | `README.md`, `CHANGELOG.md` |

### Running Tests

```bash
# Basic unittest (built-in)
python -m unittest discover -s tests -p "test_*.py" -v

# With pytest (if installed)
pytest tests/ -v -s

# With coverage
pytest tests/ --cov=src/marketrisk --cov-report=term-missing
```

### Installing from Scratch

```bash
# Production only
pip install .

# Development mode (editable)
pip install -e .

# With dev tools
pip install -e ".[dev]"
```

---

## Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate                          # Windows
source venv/bin/activate                       # macOS/Linux

# Install dependencies
pip install -r requirements.txt                # Production
pip install -r requirements-dev.txt            # Development

# Run tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run calculator interactively
python -m marketrisk.cli

# Format code
black src/ tests/

# Check code quality
flake8 src/ tests/

# Type check
mypy src/

# Generate documentation
sphinx-build -b html docs/ docs/_build/
```

---

## Troubleshooting

### "No module named 'marketrisk'"
- Ensure you've run `pip install -e .`
- Check virtual environment is activated

### "Could not fetch data for TICKER"
- Check ticker symbol is valid (AAPL, MSFT, GOOGL, etc.)
- Check internet connection
- Yahoo Finance might be temporarily unavailable

### Tests not found
- Make sure you're in the project root: `cd MarketRisk`
- Files must start with `test_` in `tests/` directory

### Import errors in tests
- Delete `tests/__pycache__` folder
- Reinstall package: `pip install -e .`

---

## File Changes

### Key New Files
- ✅ `setup.py` - Package configuration
- ✅ `pyproject.toml` - Tool configuration
- ✅ `requirements-dev.txt` - Dev dependencies
- ✅ `src/marketrisk/calculator.py` - Main code (moved)
- ✅ `tests/test_calculator.py` - Tests (moved)
- ✅ `docs/INSTALL.md` - Installation guide
- ✅ `docs/USAGE.md` - Usage guide

### Still Available (Old Files)
- ℹ️ `OptionsGreeksCalculator.py` - Original
- ℹ️ `OptionsGreeksCalculatorTest.py` - Original
- ℹ️ `run_tests.py` - Original

---

## Next Steps

1. **First Time?**
   → Follow "Setup (One-time)" section above

2. **Want to Run Calculations?**
   → Go to "Run Interactive Calculator"

3. **Want to Use in Code?**
   → Check "Use as a Library" example

4. **Want to Contribute?**
   → Follow "For Developers" section

5. **Need Help?**
   → Read `docs/USAGE.md` or `README.md`

---

## Support

- **Installation Issues**: See `docs/INSTALL.md`
- **Usage Examples**: See `docs/USAGE.md`
- **API Reference**: See `README.md`
- **Version History**: See `CHANGELOG.md`
- **Restructuring**: See `RESTRUCTURING.md`
- **Project Layout**: See `PROJECT_STRUCTURE.md`

---

**Status**: ✅ Your project is ready to use!

All functionality works the same, just better organized following industry best practices.

