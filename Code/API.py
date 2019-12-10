import requests
import Keys

class API_Class:
	def __init__(self):
		self.URL = Keys.URL
		self.querystring = Keys.querystring
		self.headers = Keys.headers

	def call_movers_api(self):
		print('Calling Movers API')

		url = self.URL + 'get-movers'
		response = requests.request("GET", url, headers=self.headers, params=self.querystring)
		response_status = response.status_code
		if response_status == 200:
			response_body = response.json()
			return response_body

		return False

	def call_quotes_api(self, stock):
		print('Calling Quotes API')

		url = self.URL + 'get-quotes'
		querystring = {"region":"US","lang":"en","symbols": stock}
		response = requests.request("GET", url, headers=self.headers, params= querystring)
		response_status = response.status_code
		if response_status == 200:
			response_body = response.json()
			return response_body

		return False