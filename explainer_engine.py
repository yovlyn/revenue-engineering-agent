# explainer_engine.py

def generate_decision_explanation(signal, btc_price, metrics, risk_tier="Medium"):
    """
    يقوم بتوليد تحليل منطقي ومبسط يشرح سبب اتخاذ الوكيل لهذا القرار المالي.
    """
    sharpe = metrics.get("Sharpe Ratio", 0)
    strategy_return = metrics.get("Strategy Return (%)", 0)
    
    explanation = f"Analysis for Signal [{signal}] at Bitcoin Price ${btc_price}:\n"
    
    if signal == "BULLISH_SIGNAL":
        explanation += (
            f"- Market Momentum: Positive upward pressure detected.\n"
            f"- Historical Performance Backing: Strategy return is strong at {strategy_return}% "
            f"with a healthy Sharpe ratio of {sharpe}.\n"
            f"- Risk Assessment ({risk_tier}): Volatility is within acceptable risk boundaries."
        )
    elif signal == "SELL_SIGNAL":
        explanation += (
            f"- Market Momentum: Resistance level reached or downward correction anticipated.\n"
            f"- Risk Mitigation: Protecting capital as Sharpe ratio ({sharpe}) dictates caution.\n"
            f"- Risk Assessment ({risk_tier}): Capital preservation prioritized under current conditions."
        )
    else:
        explanation += (
            f"- Market Momentum: Neutral equilibrium state (Sideways market).\n"
            f"- Action: Holding position to avoid unnecessary transaction fees.\n"
            f"- Risk Assessment ({risk_tier}): Stable operations."
            
        )
    return explanation

if __name__ == "__main__":
    sample_metrics = {"Sharpe Ratio": 6.34, "Strategy Return (%)": 22.14}
    print(generate_decision_explanation("BULLISH_SIGNAL", 64000.0, sample_metrics))
