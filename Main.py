import requests
import Keys

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-movers"

querystring = {"region":"US","lang":"en"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': Keys.API_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text.finance['results'][1])