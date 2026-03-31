"""Utility functions for MarketRisk package."""

from datetime import datetime, timezone
from typing import Tuple


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string in format 'YYYY-MM-DD' to datetime object.
    
    Args:
        date_str: Date string in format 'YYYY-MM-DD'
        
    Returns:
        datetime object with UTC timezone
        
    Raises:
        ValueError: If date string is not in correct format
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"Date must be in YYYY-MM-DD format, got: {date_str}")


def validate_option_type(option_type: str) -> str:
    """
    Validate and normalize option type.
    
    Args:
        option_type: Option type ('call', 'put', or case variations)
        
    Returns:
        Normalized option type (lowercase)
        
    Raises:
        ValueError: If option type is not 'call' or 'put'
    """
    normalized = option_type.lower().strip()
    if normalized not in ['call', 'put']:
        raise ValueError(f"Option type must be 'call' or 'put', got: {option_type}")
    return normalized


def validate_positive(value: float, name: str) -> float:
    """
    Validate that a value is positive.
    
    Args:
        value: The value to validate
        name: Name of the parameter (for error messages)
        
    Returns:
        The validated value
        
    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got: {value}")
    return value


def round_to_decimals(value: float, decimals: int = 4) -> float:
    """
    Round a value to specified number of decimal places.
    
    Args:
        value: The value to round
        decimals: Number of decimal places (default: 4)
        
    Returns:
        Rounded value
    """
    return round(value, decimals)

