from .market_regime import MarketRegime
from .signal_generator import SignalGenerator
from .risk_manager import RiskManager


class MainTradingEngine:
    def __init__(self):
        self.signal_generator = SignalGenerator()
        self.risk_manager = RiskManager()

    def run_cycle(self, regime, options_analysis, spot_price):
        signal = self.signal_generator.generate(regime, options_analysis, spot_price)
        return signal
