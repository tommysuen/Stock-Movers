# Stock-Mover
The Stock Movers Application leverages AWS Cloud Services and Python to retrieve and maintain the top and worse performers a day. The results are then stored in DynamoDB to keep track of daily performance. Every day, the application will send a text message to all its subscribers a CSV file of all the data stored within DynamoDB with some analysis done.

Tools Used - AWS EC2, S3, DynamoDB, SSM, KMS and Python
