import boto3
from datetime import datetime
import Keys

class S3_Class:
	def __init__(self):
		self.client = boto3.client('s3')
		self.object_path = None
		

	def upload_file(self, file_name):
		'''
			Uploads a file into AWS S3
		'''
		bucket = Keys.BUCKET
		self.object_path = f'Stock_Results/{file_name}'
		self.client.upload_file(f'Results/{file_name}', bucket, self.object_path, ExtraArgs={'ACL': 'public-read'})
		object_url = f'https://{bucket}.s3.amazonaws.com/{self.object_path}'
		
		return object_url

	def delete_obect(self, object_path):
		'''
			Removes an object from S3.
		'''
		response = self.client.delete_object(
		    Bucket=Keys.BUCKET,
		    Key=object_path
		)
		
