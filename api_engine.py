import requests

def fetch_market_data(symbol="bitcoin"):
    """
    جلب بيانات حية من CoinCap API كبديل آمن لا يتأثر بالحظر الجغرافي.
    """
    try:
        # استخدام معرف العملة بالاسم الصريح مثل bitcoin
        url = f"https://api.coincap.io/v2/assets/{symbol.lower()}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # استخراج السعر من هيكل الاستجابة الخاص بـ CoinCap
        if "data" in data and "priceUsd" in data["data"]:
            return float(data["data"]["priceUsd"])
        else:
            return f"API_Error_Format: {str(data)}"
    except Exception as e:
        return f"API_Error: {str(e)}"

if __name__ == "__main__":
    price = fetch_market_data("bitcoin")
    print(f"Current Price: {price}")
