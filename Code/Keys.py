import boto3

'''
	Configuration File used to store variables pulled from AWS SSM
'''
client = boto3.client('ssm', region_name = 'us-east-1')
API_response = client.get_parameter(Name = 'API_KEY', WithDecryption=True)
SNS_PATH_RESPONSE = client.get_parameter(Name='SNS_PATH', WithDecryption=True)
BUCKET_RESPONSE = client.get_parameter(Name='BUCKET', WithDecryption = True)

BUCKET = BUCKET_RESPONSE['Parameter']['Value']
SNS_PATH = SNS_PATH_RESPONSE['Parameter']['Value']
API_KEY = API_response['Parameter']['Value']

URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/"
querystring = {"region":"US","lang":"en"}

headers = {'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
		    'x-rapidapi-key': API_KEY}