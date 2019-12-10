import requests
import Keys
import Stock
import API
from SNS import SNS_Class
from Database import Database_Class
from S3 import S3_Class
import functools
import time

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

@timer
def main():
	'''
		Calls the Movers API and uses that file to retrieve the top movers
		and top losers of the day.
		The data is then stored in DynamoDB and generates a CSV based on
		those results. Those results are then sent to end users via text.
	'''
	print("Main Function Triggered")
	Database = Database_Class()
	S3 = S3_Class()
	Messenger = SNS_Class()
	movers_json = API.API_Class().call_movers_api()
	top_winners = Stock.Stock_Class().get_top_winners(movers_json)
	top_losers = Stock.Stock_Class().get_top_losers(movers_json)
	# Sample Values
	# top_winners = {'STNE': {'RPC': 20.49491, 'RP': 34.35, 'PRPC': 24.1, 'PRP': 2.1000023, 'PPC': 24, 'PP': 0.060001373}}
	Database.put_series(top_winners, 'Winners')
	Database.put_series(top_losers, 'Losers')
	file_name = Database.create_file()
	Database.export_data(f'Results/{file_name}')
	object_url = S3.upload_file(f'{file_name}')
	Messenger.send_text(object_url)

if __name__ == '__main__':
	main()
