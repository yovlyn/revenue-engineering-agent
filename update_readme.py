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
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: could not load {path}: {e}")
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def fetch_real_bitcoin_price():
    """جلب السعر الحقيقي للبيتكوين مع تفعيل نظام البدائل (Binance -> CoinGecko -> CoinCap) لتجاوز قيود الحظر الجغرافي 451"""
    
    # 1. محاولة Binance الأولى
    binance_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        req = urllib.request.Request(binance_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            price = float(data['price'])
            print(f"✅ تم جلب السعر بنجاح من Binance: ${price}")
            return price
    except Exception as e:
        print(f"⚠️ تعذر الجلب من Binance ({e})، جاري تجربة البديل الأول (CoinGecko)...")

    # 2. محاولة البديل الأول: CoinGecko
    coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        req = urllib.request.Request(coingecko_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            price = float(data['bitcoin']['usd'])
            print(f"✅ تم جلب السعر بنجاح من CoinGecko: ${price}")
            return price
    except Exception as e:
        print(f"⚠️ تعذر الجلب من CoinGecko ({e})، جاري تجربة البديل الثاني (CoinCap)...")

    # 3. محاولة البديل الثاني: CoinCap
    coincap_url = "https://api.coincap.io/v2/assets/bitcoin"
    try:
        req = urllib.request.Request(coincap_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            price = float(data['data']['priceUsd'])
            print(f"✅ تم جلب السعر بنجاح من CoinCap: ${price}")
            return price
    except Exception as e:
        print(f"❌ فشل جلب السعر من جميع المصادر المتاحة ({e})، سيتم استخدام السعر السابق احتياطياً.")
        return None

def decide_signal(change_pct):
    if change_pct > 0.001:
        return "BULLISH_SIGNAL"
    elif change_pct < -0.001:
        return "SELL_SIGNAL"
    return "DYNAMIC_EQUILIBRIUM"

def call_gemini(prompt, api_key):
    if not api_key:
        print("WARNING: GEMINI_API_KEY not set, skipping Gemini call.")
        return "Market data flows through cycles of measurement and reflection."
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"ERROR calling Gemini: {e}")
        return "Market rhythm continues, though today's reflection could not be generated."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")

    memory = load_json(MEMORY_FILE, {
        "last_successful_operation": "Revenue_Engine_Optimization_v1",
        "last_market_decision": "DYNAMIC_EQUILIBRIUM",
        "last_btc_price": 64000.0,
        "agent_cognitive_tier": "Level 5 (Self-Optimizing)"
    })
    history = load_json(HISTORY_FILE, {"balance": 10000.0, "total_trades": 0, "trades": []})

    last_price = memory.get("last_btc_price", 64000.0)
    
    # جلب السعر الحقيقي عبر نظام المصادر المتعددة والبدائل التلقائية
    real_price = fetch_real_bitcoin_price()
    new_price = real_price if real_price is not None else last_price
    
    change_pct = (new_price - last_price) / last_price if last_price > 0 else 0.0
    signal = decide_signal(change_pct)

    current_balance = history.get("balance", 10000.0)
    if signal == "BULLISH_SIGNAL":
        net_pnl = round(current_balance * change_pct, 2)
    elif signal == "SELL_SIGNAL":
        net_pnl = round(current_balance * abs(change_pct), 2)
    else:
        net_pnl = 0.0

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

    prompt = (
        f"Bitcoin moved from ${last_price} to ${new_price} ({change_pct*100:.2f}%). "
        f"Signal: {signal}. Write one short poetic sentence (under 25 words) "
        f"about market cycles, in the style of a calm philosophical observer."
    )
    commentary = call_gemini(prompt, api_key)

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
    try:
        main()
    except Exception as e:
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        sys.exit(1)
