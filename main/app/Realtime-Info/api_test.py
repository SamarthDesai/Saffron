import requests

response = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GOOG&apikey=CQQP9ICGYM1YH0UT")

print(response.json())