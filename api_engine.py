import requests

def fetch_market_data(symbol="BTC"):
    """
    جلب بيانات حية من API عام مع معالجة محسنة للاستجابة.
    """
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # التأكد من وجود مفتاح السعر في الرد
        if isinstance(data, dict) and "price" in data:
            return float(data['price'])
        elif isinstance(data, dict) and "symbol" in data:
            # طريقة بديلة في حال اختلاف الرد
            return data
        else:
            return f"API_Error_Format: {str(data)}"
    except Exception as e:
        return f"API_Error: {str(e)}"

if __name__ == "__main__":
    price = fetch_market_data("BTC")
    print(f"Current Price: {price}")
