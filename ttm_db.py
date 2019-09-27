import pymongo

pyclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = pyclient['talktome']

