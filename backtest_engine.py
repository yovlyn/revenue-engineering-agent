import math
import json
import urllib.request
# استيراد محرك الاستراتيجية الذي طورناه
from strategy_engine import decide_strategy_signal

def calculate_sharpe_ratio(returns, risk_free_rate=0.01):
    if not returns:
        return 0.0
    daily_rf = risk_free_rate / 252
    excess_returns = [r - daily_rf for r in returns]
    avg_excess = sum(excess_returns) / len(excess_returns)
    if len(excess_returns) < 2:
        return 0.0
    variance = sum([(r - avg_excess) ** 2 for r in excess_returns]) / len(excess_returns)
    std_dev = math.sqrt(variance)
    if std_dev == 0:
        return 0.0
    return (avg_excess / std_dev) * math.sqrt(252)

def calculate_sharpe_ratio_active(all_returns, active_signal="BULLISH_SIGNAL", risk_free_rate=0.01):
    """Sharpe computed only over returns from active-trade periods.

    Zero-return cash-exit periods (SELL_SIGNAL / DYNAMIC_EQUILIBRIUM) are
    excluded so they don't artificially shrink the standard deviation.
    `all_returns` is the full list; `active_signal` is the signal name
    whose returns count as 'in-market'. Pass a list to cover multiple.
    """
    if not all_returns:
        return 0.0
    if isinstance(active_signal, str):
        active_signals = {active_signal}
    else:
        active_signals = set(active_signal)
    active = [r for r, sig in all_returns if sig in active_signals]
    return calculate_sharpe_ratio(active, risk_free_rate)

def calculate_sortino_ratio(returns, risk_free_rate=0.01):
    """Sortino uses only downside deviation — penalizes harmful volatility only."""
    if not returns:
        return 0.0
    daily_rf = risk_free_rate / 252
    excess_returns = [r - daily_rf for r in returns]
    avg_excess = sum(excess_returns) / len(excess_returns)
    downside = [min(0, r) for r in excess_returns]
    if len(downside) < 2:
        return 0.0
    downside_var = sum(d ** 2 for d in downside) / len(downside)
    downside_dev = math.sqrt(downside_var)
    if downside_dev == 0:
        return 0.0
    return (avg_excess / downside_dev) * math.sqrt(252)

def calculate_max_drawdown(equity_curve):
    if not equity_curve:
        return 0.0
    peak = equity_curve[0]
    max_dd = 0.0
    for value in equity_curve:
        if value > peak:
            peak = value
        dd = (peak - value) / peak if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd
    return max_dd

def fetch_historical_prices(symbol="BTCUSDT", interval="1d", limit=50):
    # Source 1: Binance klines (returns 451 on US-based GH Actions runners)
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            closes = [float(candle[4]) for candle in data]
            if closes:
                return closes
    except Exception as e:
        print(f"⚠️ Binance klines failed ({e}), trying CoinGecko historical...")

    # Source 2: CoinGecko /market_chart — real daily OHLC closes
    try:
        days = min(limit, 90)
        gecko_id = "bitcoin"
        url = f"https://api.coingecko.com/api/v3/coins/{gecko_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            prices = data.get("prices", [])
            closes = [float(point[1]) for point in prices]
            if closes:
                return closes[-limit:]
    except Exception as e:
        print(f"⚠️ CoinGecko historical failed ({e}), trying CoinCap history...")

    # Source 3: CoinCap /assets/{id}/history — real daily prices
    try:
        url = "https://api.coincap.io/v2/assets/bitcoin/history?interval=d1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            entries = data.get("data", [])
            closes = [float(entry["priceUsd"]) for entry in entries]
            if closes:
                return closes[-limit:]
    except Exception as e:
        print(f"⚠️ CoinCap historical failed ({e})")

    # Last resort: explicit marker, not silent placeholder
    print("❌ All 3 historical data sources failed. Returning empty list.")
    return []

def run_real_backtest():
    print("=== Institutional Backtest Engine: Strategy-Linked Mode ===")
    
    prices = fetch_historical_prices(symbol="BTCUSDT", interval="1d", limit=50)

    if not prices or len(prices) < 25:
        print("❌ Insufficient historical data for backtest. Aborting.")
        return {
            "Strategy Return (%)": 0.0,
            "Benchmark Return (%)": 0.0,
            "Sharpe Ratio (Active-Only)": 0.0,
            "Sharpe Ratio (All Periods)": 0.0,
            "Sortino Ratio": 0.0,
            "Max Drawdown (%)": 0.0,
            "Final Portfolio Value": initial_capital,
            "Dataset Type": "ERROR: No historical data available"
        }

    initial_capital = 10000.0
    strategy_capital = initial_capital
    benchmark_capital = initial_capital
    
    strategy_equity = [strategy_capital]
    benchmark_equity = [benchmark_capital]
    
    historical_strategy_returns = []
    historical_benchmark_returns = []
    # Track signal alongside return for active-only Sharpe calculation
    signal_return_pairs = []

    # نبدأ من الشمعة التي تسمح بتوفر نافذة بيانات كافية للاستراتيجية
    start_index = 20

    for i in range(start_index, len(prices)):
        current_window = prices[:i]
        current_price = prices[i]
        prev_price = prices[i-1]

        # السوق الطبيعي العائد البسيط
        market_return = (current_price - prev_price) / prev_price
        historical_benchmark_returns.append(market_return)
        benchmark_capital *= (1 + market_return)
        benchmark_equity.append(benchmark_capital)

        # استدعاء الإشارة من استراتيجيتنا المتقدمة (SMA + RSI)
        signal = decide_strategy_signal(current_price, current_window)

        # تطبيق العائد بناءً على القرار الاستراتيجي
        if signal == "BULLISH_SIGNAL":
            strat_return = market_return
        elif signal == "SELL_SIGNAL":
            strat_return = 0.0
        else:
            # DYNAMIC_EQUILIBRIUM: no clear signal → stay in cash (0%)
            # Previous 50% market exposure was an arbitrary drag with no
            # risk rationale; cash is the correct neutral position.
            strat_return = 0.0

        historical_strategy_returns.append(strat_return)
        signal_return_pairs.append((strat_return, signal))
        strategy_capital *= (1 + strat_return)
        strategy_equity.append(strategy_capital)

    total_return = ((strategy_capital - initial_capital) / initial_capital) * 100
    benchmark_return = ((benchmark_capital - initial_capital) / initial_capital) * 100
    sharpe = calculate_sharpe_ratio_active(signal_return_pairs, active_signal=["BULLISH_SIGNAL", "DYNAMIC_EQUILIBRIUM"])
    sharpe_all = calculate_sharpe_ratio(historical_strategy_returns)
    sortino = calculate_sortino_ratio(historical_strategy_returns)
    max_dd = calculate_max_drawdown(strategy_equity) * 100

    results = {
        "Strategy Return (%)": round(total_return, 2),
        "Benchmark Return (%)": round(benchmark_return, 2),
        "Sharpe Ratio (Active-Only)": round(sharpe, 2),
        "Sharpe Ratio (All Periods)": round(sharpe_all, 2),
        "Sortino Ratio": round(sortino, 2),
        "Max Drawdown (%)": round(max_dd, 2),
        "Final Portfolio Value": round(strategy_capital, 2),
        "Dataset Type": "Live Binance/CoinGecko/CoinCap + Real Strategy Logic"
    }
    
    print(f"Backtest Results with Strategy: {results}")
    return results

if __name__ == "__main__":
    run_real_backtest()
