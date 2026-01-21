import requests

url = "http://127.0.0.1:5000/analyze"
data = {"description": "Volatility spike in equities due to economic report"}
try:
    response = requests.post(url, json=data, timeout=120)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)