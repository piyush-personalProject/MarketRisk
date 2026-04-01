"""
MarketRisk - Options Greeks Calculator

A  Python library for calculating options Greeks using:
- Black-Scholes model for equities (EquityOptionsCalculator)
- Black76 model for futures (FuturesOptionsCalculator)
"""

__version__ = "1.1.0"
__author__ = "Piyush Jain"
__license__ = "MIT"

from .calculator import EquityOptionsCalculator
from .futures_calculator import FuturesOptionsCalculator

# Backward compatibility alias
OptionsGreeksCalculator = EquityOptionsCalculator

__all__ = ["EquityOptionsCalculator", "FuturesOptionsCalculator", "OptionsGreeksCalculator"]

