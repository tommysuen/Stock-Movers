import boto3
import pandas as pd
from datetime import datetime


class Database_Class:
	def __init__(self):
		self.client = boto3.client('dynamodb')
		self.today_unformatted = datetime.today()
		self.today = self.today_unformatted.strftime("%m_%d_%Y")
		self.dictionary = {'Stock_Name': [], 'Title': [], 'Date': [], 'Pre_Market_Change_Percent': [], 'Pre_Market_Change_Dollars': [],
					  'Regular_Market_Change_Percent': [], 'Regular_Market_Change_Dollars': [],
					  'Post_Market_Change_Percent': [], 'Post_Market_Change_Dollars': []}
		self.file_name = None
		pass

	def put_item(self, Stock_Name, title, RPC, RP, PRPC, PRP, PPC, PP):
		'''
			Puts an entry into DynamoDB
		'''
		item = self.build_item(Stock_Name, title, RPC, RP, PRPC, PRP, PPC, PP)
		response = self.client.put_item(
	    TableName='Stock_Database',
	    Item= item)
		self.update_item(Stock_Name, title)

	def update_item(self, Stock_Name, Title):
		'''
			Updates an existing entry in DynamoDB
		'''
		response = self.client.update_item(
		TableName= 'Stock_Database',
		Key={
			'Stock_Name': {'S': Stock_Name},
			'Title': {'S': Title}

		},
		UpdateExpression="set PPC=:r",
	    ExpressionAttributeValues={
	        ':r': {'N': '242'}
	    },
	    ReturnValues="UPDATED_NEW"
		)

	def build_item(self, Stock_Name, title, RPC, RP, PRPC, PRP, PPC, PP):
		'''
			Used to build the Item query for put item
		'''
		today_formatted = self.today_unformatted.strftime("%Y-%m-%d")
		if PRPC == 'None' and PPC == 'None':
			Item= {
		        'Stock_Name': {'S': Stock_Name},
		        'Title': {'S': title},
		        'Date': {'S': today_formatted},
		        'RPC': {'N': RPC},
		        'RP': {'N': RP}
		    }
		elif PRPC == 'None' and PPC != 'None':
			Item={
		        'Stock_Name': {'S': Stock_Name},
		        'Title': {'S': title},
		        'Date': {'S': today_formatted},
		        'PP': {'N': PP},
		        'PPC': {'N': PPC},
		        'RPC': {'N': RPC},
		        'RP': {'N': RP}

		        }

		elif PPC == 'None' and PRPC != 'None':
			Item={
		        'Stock_Name': {'S': Stock_Name},
		        'Title': {'S': title},
		        'Date': {'S': today_formatted},
		        'RPC': {'N': RPC},
		        'RP': {'N': RP},
		        'PRPC': {'N': PRPC},
		        'PRP': {'N': PRP}
		        }
		else:
			Item={
	        'Stock_Name': {'S': Stock_Name},
	        'Title': {'S': title},
	        'Date': {'S': today_formatted},
	        'RPC': {'N': RPC},
	        'RP': {'N': RP},
	        'PRPC': {'N': PRPC},
	        'PRP': {'N': PRP},
	        'PPC': {'N': PPC},
	        'PP': {'N': PP}
	    }
		return Item

	def put_series(self, series, title):
		'''
			Writes results as a series (batch) to DynamoDB
		'''
		print(series)
		for key,value in series.items():
			self.put_item(key, title, str(value['RPC']), str(value['RP']),
				str(value['PRPC']), str(value['PRP']),
				str(value['PPC']), str(value['PP']))


	def export_data(self, file_name):
		'''
			Pulls results from DynamoDB and exports the data into a CSV File
		'''
		response = self.client.scan(
			TableName = 'Stock_Database')

		for i in range(len(response['Items'])):
			self.dictionary['Stock_Name'].append(response['Items'][i]['Stock_Name']['S'])
			self.dictionary['Title'].append(response['Items'][i]['Title']['S'])
			self.dictionary['Date'].append(self.today)
			if 'PRPC' in response['Items'][i]:
				self.dictionary['Pre_Market_Change_Percent'].append(response['Items'][i]['PRPC']['N'])
			else:
				self.dictionary['Pre_Market_Change_Percent'].append(None)
			if 'PRP' in response['Items'][i]:
				self.dictionary['Pre_Market_Change_Dollars'].append(response['Items'][i]['PRP']['N'])
			else:
				self.dictionary['Pre_Market_Change_Dollars'].append(None)
			if 'RPC' in response['Items'][i]:
				self.dictionary['Regular_Market_Change_Percent'].append(response['Items'][i]['RPC']['N'])
			else:
				self.dictionary['Regular_Market_Change_Percent'].append(None)
			if 'RP' in response['Items'][i]:
				self.dictionary['Regular_Market_Change_Dollars'].append(response['Items'][i]['RP']['N'])
			else:
				self.dictionary['Regular_Market_Change_Dollars'].append(None)
			if 'PPC' in response['Items'][i]:
				self.dictionary['Post_Market_Change_Percent'].append(response['Items'][i]['PPC']['N'])
			else:
				self.dictionary['Post_Market_Change_Percent'].append(None)
			if 'PP' in response['Items'][i]:
				self.dictionary['Post_Market_Change_Dollars'].append(response['Items'][i]['PP']['N'])
			else:
				self.dictionary['Post_Market_Change_Dollars'].append(None)

		df = pd.DataFrame(self.dictionary)
		df.to_csv(file_name, index=False)

	def create_file(self):
		'''
			Creates the CSV File used to store data
		'''
		df = pd.DataFrame(self.dictionary)
		self.file_name = f'{self.today}_Stock_Data.csv'
		df.to_csv(f'Results/{self.file_name}', index=False)

		return self.file_name
