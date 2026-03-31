# Installation Guide - MarketRisk Options Greeks Calculator

## Overview

MarketRisk is a **Black-Scholes Options Greeks Calculator** that computes option prices and Greeks (Delta, Gamma, Vega, Theta) for call and put options. It fetches real-time stock data and visualizes option values over time.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Quick Start

### 1. Clone or Download the Project

```bash
cd MarketRisk
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Run the test suite to ensure everything is properly installed:

```bash
# Using unittest
python -m unittest discover -s tests -p "test_*.py" -v

# Or using pytest (if installed)
pytest tests/ -v
```

## Installation Variants

### Development Installation

If you want to contribute or modify the code:

```bash
# Install with development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Package Installation

To install from the project directory:

```bash
# Standard installation
pip install .

# Or in editable mode
pip install -e .
```

## Dependencies

### Production Dependencies

The project requires the following Python packages:

- **numpy** (>=1.21.0) - Numerical computing library
- **yfinance** (>=0.1.70) - Fetches real-time stock data from Yahoo Finance
- **matplotlib** (>=3.4.0) - Plotting and visualization
- **scipy** (>=1.7.0) - Scientific computing (normal distribution functions)
- **pandas** (>=1.3.0) - Data manipulation and analysis

### Development Dependencies

For development and testing:

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking

## Troubleshooting

### Issue: "Module not found" or "Import error"

**Solution**: Ensure virtual environment is activated and all dependencies are installed:

```bash
# Check installed packages
pip list

# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

### Issue: "yfinance connection error"

**Solution**: Check your internet connection and ensure Yahoo Finance is accessible.

- This typically indicates a network issue
- Try again after checking your connection

### Issue: "ValueError: Could not fetch data for TICKER"

**Solution**: Verify the ticker symbol is valid:

- Use valid stock tickers (e.g., AAPL, MSFT, GOOGL)
- Make sure the ticker exists on Yahoo Finance
- Check your internet connection

### Issue: Tests failing

**Solution**: Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

### Issue: Python version error

**Solution**: Ensure you're using Python 3.7 or higher:

```bash
python --version
```

If using Python 2 or Python 3.6, upgrade your Python installation.

## Uninstall/Cleanup

To remove the virtual environment:

```bash
# Deactivate the virtual environment
deactivate

# Remove the virtual environment folder
# On Windows:
rmdir /s /q venv

# On macOS/Linux:
rm -rf venv
```

## Next Steps

After installation, refer to the [README.md](../README.md) for usage instructions and examples.

