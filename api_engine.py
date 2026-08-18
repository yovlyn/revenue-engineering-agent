import requests

def fetch_market_data(symbol="BTC"):
    """
    جلب بيانات حية من API عام (Binance).
    """
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['price'])
    except Exception as e:
        return f"API_Error: {str(e)}"
