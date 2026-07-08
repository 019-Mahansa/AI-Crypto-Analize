import pandas as pd
import numpy as np
from typing import Optional, Dict, Any


def _find_column(df: pd.DataFrame, keywords):
    cols = list(df.columns)
    low = [c.lower() for c in cols]
    for kw in keywords:
        for i, c in enumerate(low):
            if kw in c:
                return cols[i]
    return None


def analyze_technical_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze a DataFrame with technical columns and return detected trigger-like signals.

    The function attempts to be robust to different column namings by searching
    for keywords. Returns a dict with raw detections and a concise English summary.
    """
    if df is None or df.empty:
        return {"summary": "No market data provided.", "signals": {}}

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    signals = {}

    # RSI
    rsi_col = _find_column(df, ["rsi"])
    if rsi_col:
        rsi_latest = float(latest[rsi_col])
        signals["rsi"] = {
            "column": rsi_col,
            "value": rsi_latest,
            "note": (
                "overbought" if rsi_latest >= 70 else
                "oversold" if rsi_latest <= 30 else
                "neutral"
            )
        }

    # EMA cross (prefer 20/50)
    ema_short_col = _find_column(df, ["ema_20", "ema20", "ema20"]) or _find_column(df, ["ema", "ema20"]) 
    ema_long_col = _find_column(df, ["ema_50", "ema50"]) or _find_column(df, ["ema", "ema50"]) 
    # fallback: look for any ema columns and pick relative lengths
    if not ema_short_col or not ema_long_col:
        ema_cols = [c for c in df.columns if "ema" in c.lower()]
        if len(ema_cols) >= 2:
            # try to choose by numeric length in name
            try:
                ema_sorted = sorted(ema_cols, key=lambda c: int(''.join(filter(str.isdigit, c)) or 0))
                ema_short_col, ema_long_col = ema_sorted[0], ema_sorted[-1]
            except Exception:
                ema_short_col, ema_long_col = ema_cols[0], ema_cols[-1]

    if ema_short_col and ema_long_col:
        e_short_latest = float(latest[ema_short_col])
        e_long_latest = float(latest[ema_long_col])
        e_short_prev = float(prev[ema_short_col])
        e_long_prev = float(prev[ema_long_col])
        crossover = None
        if e_short_prev <= e_long_prev and e_short_latest > e_long_latest:
            crossover = "bullish_cross_over (short crossed above long)"
        elif e_short_prev >= e_long_prev and e_short_latest < e_long_latest:
            crossover = "bearish_cross_under (short crossed below long)"
        signals["ema_cross"] = {
            "short": ema_short_col,
            "long": ema_long_col,
            "latest_short": e_short_latest,
            "latest_long": e_long_latest,
            "crossover": crossover,
        }

    # ATR spike (volatility)
    atr_col = _find_column(df, ["atr"])
    if atr_col:
        atr_series = df[atr_col].dropna()
        if not atr_series.empty:
            atr_latest = float(latest[atr_col])
            atr_mean = float(atr_series.tail(50).mean()) if len(atr_series) >= 5 else float(atr_series.mean())
            signals["atr"] = {
                "column": atr_col,
                "latest": atr_latest,
                "baseline_mean": round(atr_mean, 6),
                "spike": atr_latest > atr_mean * 1.5
            }

    # Bollinger Bands touches
    # Try common names: bbu / bb_upper / bbl / bb_lower
    bb_upper = _find_column(df, ["bbu", "upperband", "bb_u", "bbu", "bb_upper"])
    bb_lower = _find_column(df, ["bbl", "lowerband", "bb_l", "bbl", "bb_lower"])
    if bb_upper and bb_lower:
        close_col = _find_column(df, ["close"])
        if close_col:
            close_latest = float(latest[close_col])
            signals["bollinger"] = {
                "upper": float(latest[bb_upper]),
                "lower": float(latest[bb_lower]),
                "close": close_latest,
                "touch_upper": close_latest >= float(latest[bb_upper]),
                "touch_lower": close_latest <= float(latest[bb_lower])
            }

    # Stochastic (k/d)
    stoch_col_k = _find_column(df, ["stochk", "k_", "%k", "k"])
    stoch_col_d = _find_column(df, ["stochd", "d_", "%d", "d"])
    if stoch_col_k and stoch_col_d:
        k_latest = float(latest[stoch_col_k])
        d_latest = float(latest[stoch_col_d])
        signals["stochastic"] = {
            "k": k_latest,
            "d": d_latest,
            "note": (
                "overbought" if k_latest >= 80 and d_latest >= 80 else
                "oversold" if k_latest <= 20 and d_latest <= 20 else
                "neutral"
            )
        }

    # Compose a short English summary
    summary_lines = []
    if "rsi" in signals:
        s = signals["rsi"]
        summary_lines.append(f"RSI ({s['column']}) = {s['value']:.1f} ({s['note']}).")
    if "ema_cross" in signals:
        ec = signals["ema_cross"]
        if ec["crossover"]:
            summary_lines.append(f"EMA crossover detected: {ec['crossover']}.")
        else:
            trend = "bullish" if ec["latest_short"] > ec["latest_long"] else "bearish"
            summary_lines.append(f"EMA relationship: short({ec['short']}) is {trend} vs long({ec['long']}).")
    if "atr" in signals:
        a = signals["atr"]
        if a["spike"]:
            summary_lines.append("ATR spike detected (volatility increasing).")
    if "bollinger" in signals:
        b = signals["bollinger"]
        if b["touch_upper"]:
            summary_lines.append("Price touching or above upper Bollinger Band — extended/high volatility region.")
        if b["touch_lower"]:
            summary_lines.append("Price touching or below lower Bollinger Band — extended/low region.")
    if "stochastic" in signals:
        st = signals["stochastic"]
        summary_lines.append(f"Stochastic K/D = {st['k']:.0f}/{st['d']:.0f} ({st['note']}).")

    if not summary_lines:
        summary = "No recognizable technical indicators were found in the provided data."
    else:
        summary = " ".join(summary_lines)

    return {"summary": summary, "signals": signals}


def build_rag_prompt(fundamentals: Optional[str], market_df: Optional[pd.DataFrame], news: Optional[str]) -> str:
    """Build a Retrieval-Augmented Generation (RAG) prompt in English.

    The prompt includes the raw fundamentals, a concise technical summary produced by
    `analyze_technical_signals`, and recent news. It instructs the model to flag any
    indicators that have reached or passed critical trigger points for reversals or
    trend continuation, and to produce a short, actionable output.
    """
    analysis = analyze_technical_signals(market_df) if market_df is not None else {"summary": "No market data."}

    prompt_parts = [
        "You are a professional quantitative crypto analyst. Your task: read the provided data",
        "and identify any technical indicators that HAVE REACHED OR PASSED critical trigger levels",
        "that imply a likely reversal or reinforcement of the trend. Answer concisely in English.",
        "\n---\n",
        "MARKET TECHNICAL SUMMARY (automated):",
        analysis.get("summary", "No analysis available."),
        "\n---\n",
        "FUNDAMENTAL DATA:",
        fundamentals or "No fundamental data provided.",
        "\n---\n",
        "RECENT NEWS (last 7 days):",
        news or "No news provided.",
        "\n---\n",
        "INSTRUCTIONS (strict):",
        "1) List each indicator that is at or beyond a trigger threshold (e.g., RSI>=70, RSI<=30, EMA cross, price touching BB upper/lower, ATR spike, Stochastic >=80/<=20).",
        "2) For each, state: Indicator name; current value; whether it signals 'Possible Reversal' or 'Trend Continuation'; and a one-sentence rationale.",
        "3) Provide EXACTLY ONE short actionable sentence: Long / Short / Neutral with suggested entry, SL, TP levels if determinable from the latest close and bands (use brackets).",
        "4) Keep answer in English and no more than 6 bullet points.",
    ]

    return "\n".join(prompt_parts)


def prompt():
    """Compatibility wrapper: returns a default RAG instruction template in English."""
    return build_rag_prompt(None, None, None)


__all__ = ["analyze_technical_signals", "build_rag_prompt", "prompt"]