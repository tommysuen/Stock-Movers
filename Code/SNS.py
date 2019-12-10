import boto3
import Keys
from datetime import datetime

class SNS_Class:
	def __init__(self):
		self.client = boto3.client('sns')
		self.today = None
		
	def send_text(self, url):
		today_unformatted = datetime.today()
		self.today = today_unformatted.strftime("%m/%d/%Y")
		self.client.publish(
		TargetArn=Keys.SNS_PATH,
	    Message=f"Hey There,\n\nHere is today's ({self.today}) Top Movers Report\n----------\n{url}\n\nThanks,\nTommy"
    )

