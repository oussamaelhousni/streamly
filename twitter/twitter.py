import requests

payload = {
    "api_key": "d1d32d8239779f39aa47aef8e13be219",
    "query": "emergent diseases",
    "num": 10,
}

response = requests.get(
    " https://api.scraperapi.com/structured/twitter/search", params=payload
)
data = response.json()
