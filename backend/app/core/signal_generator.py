from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .market_regime import MarketRegime


@dataclass
class TradeSignal:
    action: str
    strategy: str
    direction: str
    confidence: float
    reason: str
    legs: List[Dict[str, Any]]


class SignalGenerator:
    def generate(self, regime, options_analysis: Dict[str, Any], spot_price: float) -> Optional[TradeSignal]:
        liquid = options_analysis["liquid_chain_df"]
        if liquid.empty:
            return None

        atm = options_analysis["atm_strike"]

        if regime.regime in [MarketRegime.STRONG_BULLISH, MarketRegime.MODERATE_BULLISH]:
            ce = liquid[(liquid["type"] == "CE") & (liquid["strike"] >= atm)].head(1)
            if ce.empty:
                return None
            return TradeSignal(
                action="BUY",
                strategy="Long Call",
                direction="Bullish",
                confidence=regime.score,
                reason="Bullish regime detected",
                legs=[ce.iloc[0].to_dict()],
            )

        if regime.regime in [MarketRegime.STRONG_BEARISH, MarketRegime.MODERATE_BEARISH]:
            pe = liquid[(liquid["type"] == "PE") & (liquid["strike"] <= atm)].head(1)
            if pe.empty:
                return None
            return TradeSignal(
                action="BUY",
                strategy="Long Put",
                direction="Bearish",
                confidence=regime.score,
                reason="Bearish regime detected",
                legs=[pe.iloc[0].to_dict()],
            )

        return None
