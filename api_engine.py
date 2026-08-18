import requests

def fetch_market_data(symbol="BTC"):
    """
    جلب بيانات حية مع عدة مصادر بديلة لتجنب مشاكل الشبكة والـ DNS.
    """
    # المحاولة الأولى: استخدام Binance API المباشر
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url, timeout=5)
        data = response.json()
        if isinstance(data, dict) and "price" in data:
            return float(data['price'])
    except Exception:
        pass

    # المحاولة الثانية: استخدام CoinCap API كبديل أول
    try:
        url = "https://api.coincap.io/v2/assets/bitcoin"
        response = requests.get(url, timeout=5)
        data = response.json()
        if "data" in data and "priceUsd" in data["data"]:
            return float(data["data"]["priceUsd"])
    except Exception:
        pass

    # المحاولة الثالثة: استخدام بديل ثالث خفيف (CoinGecko)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        if "bitcoin" in data and "usd" in data["bitcoin"]:
            return float(data["bitcoin"]["usd"])
    except Exception as e:
        return f"API_Error: All fallback APIs failed ({str(e)})"

if __name__ == "__main__":
    price = fetch_market_data("BTC")
    print(f"Current Price: {price}")
