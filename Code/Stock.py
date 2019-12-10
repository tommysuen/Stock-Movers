import API

class Stock_Class:
	def __init__(self):
		self.losers = {}
		self.winners = {}
		self.title = None
		self.reg_change_percent = None
		self.reg_change_dollars = None
		self.pre_change_percent = None
		self.pre_change_dollars = None
		self.post_change_percent = None
		self.post_change_dollars = None
	
	def get_top_losers(self, json_file):
		json_day_losers = json_file['finance']['result'][1]

		for i in json_day_losers['quotes']:
			symbol = i['symbol']
			response = self.get_stock_data(symbol)
			if response != False:
				self.losers[symbol] = {}
				self.losers[symbol]['RPC'] = self.reg_change_percent
				self.losers[symbol]['RP'] = self.reg_change_dollars
				self.losers[symbol]['PRPC'] = self.pre_change_percent
				self.losers[symbol]['PRP'] = self.pre_change_dollars
				self.losers[symbol]['PPC'] = self.post_change_percent
				self.losers[symbol]['PP'] = self.post_change_dollars

		return self.losers


	def get_top_winners(self, json_file):
		
		json_day_winners = json_file['finance']['result'][0]

		for i in json_day_winners['quotes']:
			symbol = i['symbol']
			response = self.get_stock_data(symbol)
			if response != False:
				self.winners[symbol] = {}
				self.winners[symbol]['RPC'] = self.reg_change_percent
				self.winners[symbol]['RP'] = self.reg_change_dollars
				self.winners[symbol]['PRPC'] = self.pre_change_percent
				self.winners[symbol]['PRP'] = self.pre_change_dollars
				self.winners[symbol]['PPC'] = self.post_change_percent
				self.winners[symbol]['PP'] = self.post_change_dollars
			

		return self.winners

	def get_stock_data(self, stock):
		print(f"Getting Stock Data for {stock}")
		stock_json_file = API.API_Class().call_quotes_api(stock)
		if stock_json_file != 'False':
			self.reg_change_percent = stock_json_file['quoteResponse']['result'][0]['regularMarketChangePercent']
			self.reg_change_dollars = stock_json_file['quoteResponse']['result'][0]['regularMarketPreviousClose']
			pre_results = self.validation('Pre', stock_json_file)
			post_results = self.validation('Post', stock_json_file)

			if pre_results == True:
				self.pre_change_percent = stock_json_file['quoteResponse']['result'][0]['preMarketChangePercent']
				self.pre_change_dollars = stock_json_file['quoteResponse']['result'][0]['preMarketChange']
			
			if post_results == True:
				self.post_change_percent = stock_json_file['quoteResponse']['result'][0]['postMarketChangePercent']
				self.post_change_dollars = stock_json_file['quoteResponse']['result'][0]['postMarketChange']
			return True
		else:
			return False
	def validation(self, condition, json_file):
		if condition == 'Pre':
			if 'preMarketChange' not in json_file['quoteResponse']['result'][0]:
				return False
			else:
				return True
		else:
			if 'postMarketChange' not in json_file['quoteResponse']['result'][0]:
				return False
			else:
				return True		

