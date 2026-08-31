import json
import urllib.request
import datetime
import sys
import os

MEMORY_FILE = "memory_bank.json"
HISTORY_FILE = "trading_history.json"
README_FILE = "README.md"

def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def fetch_real_bitcoin_price():
    urls = [
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
        "https://api.coincap.io/v2/assets/bitcoin"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if "price" in data:
                    return float(data['price'])
                elif "bitcoin" in data:
                    return float(data['bitcoin']['usd'])
                elif "data" in data and "priceUsd" in data['data']:
                    return float(data['data']['priceUsd'])
        except Exception:
            continue
    return None

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    memory = load_json(MEMORY_FILE, {"last_btc_price": 64000.0, "agent_cognitive_tier": "Level 5 (Self-Optimizing)"})
    history = load_json(HISTORY_FILE, {"balance": 10000.0, "total_trades": 0, "trades": []})

    last_price = memory.get("last_btc_price", 64000.0)
    real_price = fetch_real_bitcoin_price()
    new_price = real_price if real_price is not None else last_price
    
    change_pct = (new_price - last_price) / last_price if last_price > 0 else 0.0
    signal = "BULLISH_SIGNAL" if change_pct > 0.001 else ("SELL_SIGNAL" if change_pct < -0.001 else "DYNAMIC_EQUILIBRIUM")

    current_balance = history.get("balance", 10000.0)
    net_pnl = round(current_balance * change_pct, 2) if signal != "DYNAMIC_EQUILIBRIUM" else 0.0
    new_balance = round(current_balance + net_pnl, 2)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    trade = {
        "timestamp": timestamp,
        "entry_price": new_price,
        "signal": signal,
        "net_pnl": net_pnl,
        "new_balance": new_balance
    }

    history["trades"].append(trade)
    history["trades"] = history["trades"][-20:]  
    history["balance"] = new_balance
    history["total_trades"] = history.get("total_trades", 0) + 1

    memory["last_btc_price"] = new_price
    memory["last_market_decision"] = signal
    memory["last_successful_operation"] = f"Revenue_Engine_Optimization_v{history['total_trades']}"

    commentary = "Market data flows through cycles of measurement and reflection."
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"Bitcoin moved from ${last_price} to ${new_price} ({change_pct*100:.2f}%). Signal: {signal}. Write one short poetic sentence (under 25 words) about market cycles."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            commentary = response.text.strip()
        except Exception:
            pass

    recent_trades = list(reversed(history["trades"][-5:]))
    trades_table = "\n".join(
        f"| `{t['timestamp']}` | `${t['entry_price']}` | `{t['signal']}` | `${t['net_pnl']}` | `${t['new_balance']}` |"
        for t in recent_trades
    )

    readme_content = f"""# Revenue Engine - Autonomous AI Agent

🚀 **Live Market Telemetry & System Status**

- **Current Status:** Operational
- **Last Updated:** {timestamp} UTC
- **Last Successful Operation:** {memory['last_successful_operation']}
- **Live Bitcoin Price:** `${new_price}`
- **Market Decision / Signal:** `{signal}`
- **Agent Intelligence Tier:** {memory['agent_cognitive_tier']}

---

### 📊 Performance Metrics (Paper Trading)

| Metric | Value |
|---|---|
| **Current Portfolio Balance** | `${history['balance']}` |
| **Total Executed Trades** | `{history['total_trades']}` |

---

### 📈 Recent Trading & Execution History

| Timestamp (UTC) | Bitcoin Price | Decision / Signal | Net PnL | Portfolio Balance |
|---|---|---|---|---|
{trades_table}

---

### 🏛️ Market Insight

> *"{commentary}"*

---

*Autonomous agent powered by Python, GitHub Actions, and live market API. Not a live trading system.*
"""

    with open(README_FILE, "w") as f:
        f.write(readme_content)

    save_json(MEMORY_FILE, memory)
    save_json(HISTORY_FILE, history)
    print(f"Success: price={new_price}, signal={signal}, balance={history['balance']}")

if __name__ == "__main__":
    main()
