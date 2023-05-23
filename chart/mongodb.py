import pymongo
import pandas as pd
from urllib import parse

class Mongo_DB:
    def __init__(self, mongo_uri, account, passwd):
        self.mongo_uri = mongo_uri
        self.account = account
        self.passwd= passwd
        url = 'mongodb://%s:%s@%s:27017/?authSource=admin' % (self.account, parse.quote_plus(self.passwd), self.mongo_uri)
        client = pymongo.MongoClient(url)
        self.db = client['wanted']
        
conn = Mongo_DB('165.132.172.93','thwhd1','thwhd1')
cursor = conn.db['wanted'].find({})
df = pd.DataFrame(list(cursor))
print(df)