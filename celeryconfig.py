import os
broker=os.environ['CLOUDAMQP_URL'],
backend='rpc://',
include=['tasks']