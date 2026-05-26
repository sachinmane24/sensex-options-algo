from enum import Enum


class MarketRegime(str, Enum):
    STRONG_BULLISH = 'Strong Bullish'
    MODERATE_BULLISH = 'Moderate Bullish'
    SIDEWAYS = 'Sideways / Range-bound'
    MODERATE_BEARISH = 'Moderate Bearish'
    STRONG_BEARISH = 'Strong Bearish'
    HIGH_VOLATILITY = 'High Volatility'
    LOW_VOLATILITY = 'Low Volatility'
