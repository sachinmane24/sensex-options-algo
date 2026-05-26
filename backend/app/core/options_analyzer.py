from typing import Any, Dict, List

import pandas as pd


class OptionsAnalyzer:
    """Analyze SENSEX option-chain data from Dhan.

    The normalizer is defensive because broker responses can change field names.
    """

    def analyze(self, raw_chain: Dict[str, Any], spot_price: float) -> Dict[str, Any]:
        chain_df = self._normalize_chain(raw_chain)
        if chain_df.empty:
            raise ValueError("Option chain is empty or invalid")

        ce = chain_df[chain_df["type"] == "CE"].copy()
        pe = chain_df[chain_df["type"] == "PE"].copy()

        total_call_oi = float(ce["oi"].sum())
        total_put_oi = float(pe["oi"].sum())
        pcr = total_put_oi / total_call_oi if total_call_oi else 0.0

        max_pain = self._calculate_max_pain(chain_df)
        atm_strike = float(chain_df.iloc[(chain_df["strike"] - spot_price).abs().argsort()[:1]]["strike"].iloc[0])

        atm_ce_iv = ce.iloc[(ce["strike"] - atm_strike).abs().argsort()[:1]]["iv"].mean() if not ce.empty else 0
        atm_pe_iv = pe.iloc[(pe["strike"] - atm_strike).abs().argsort()[:1]]["iv"].mean() if not pe.empty else 0
        iv_skew = float(atm_pe_iv - atm_ce_iv)

        liquid = chain_df[(chain_df["ltp"] > 0) & (chain_df["oi"] > 0) & (chain_df["volume"] >= 0)].copy()

        return {
            "chain_df": chain_df,
            "liquid_chain_df": liquid,
            "pcr": round(pcr, 2),
            "max_pain": max_pain,
            "max_pain_distance_pct": round(((spot_price - max_pain) / spot_price) * 100, 2) if spot_price else 0,
            "atm_strike": atm_strike,
            "iv_skew": round(iv_skew, 2),
            "iv_percentile": round(self._percentile(chain_df["iv"], chain_df["iv"].mean()), 2),
            "support_levels": pe.sort_values("oi", ascending=False).head(3)["strike"].tolist(),
            "resistance_levels": ce.sort_values("oi", ascending=False).head(3)["strike"].tolist(),
        }

    def _normalize_chain(self, raw: Dict[str, Any]) -> pd.DataFrame:
        data = raw.get("data", {}).get("oc", raw.get("oc", {}))
        rows: List[Dict[str, Any]] = []

        for strike_raw, item in data.items():
            strike = float(strike_raw)
            for key, opt_type in [("ce", "CE"), ("pe", "PE")]:
                leg = item.get(key, {}) or {}
                greeks = leg.get("greeks", {}) or {}
                if not leg:
                    continue

                rows.append({
                    "strike": strike,
                    "type": opt_type,
                    "security_id": leg.get("security_id"),
                    "ltp": float(leg.get("last_price", leg.get("ltp", 0)) or 0),
                    "oi": float(leg.get("oi", 0) or 0),
                    "prev_oi": float(leg.get("previous_oi", 0) or 0),
                    "volume": float(leg.get("volume", 0) or 0),
                    "iv": float(leg.get("implied_volatility", leg.get("iv", 0)) or 0),
                    "delta": float(greeks.get("delta", 0) or 0),
                    "gamma": float(greeks.get("gamma", 0) or 0),
                    "theta": float(greeks.get("theta", 0) or 0),
                    "vega": float(greeks.get("vega", 0) or 0),
                })

        return pd.DataFrame(rows)

    def _calculate_max_pain(self, df: pd.DataFrame) -> float:
        strikes = sorted(df["strike"].unique())
        pain = {}
        for expiry_price in strikes:
            total = 0.0
            for _, row in df.iterrows():
                if row["type"] == "CE":
                    total += max(0, expiry_price - row["strike"]) * row["oi"]
                else:
                    total += max(0, row["strike"] - expiry_price) * row["oi"]
            pain[expiry_price] = total
        return float(min(pain, key=pain.get))

    def _percentile(self, series: pd.Series, value: float) -> float:
        clean = series.dropna()
        if clean.empty:
            return 50.0
        return float((clean <= value).mean() * 100)
