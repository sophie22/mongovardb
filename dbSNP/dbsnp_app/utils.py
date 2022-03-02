from pymongo import MongoClient
# from django.conf import settings

### Import database credentials and path to IR_json files
try:
    from .credentials import mongodb_cred
    host = mongodb_cred['host']
    username = mongodb_cred['username'] # dbms
    password = mongodb_cred['password']
    database = mongodb_cred['database'] # dbSNP
    db_url = f"mongodb+srv://{username}:{password}@{host}/{database}?retryWrites=true&w=majority"
    # "mongodb://mango-shard-00-00.btppp.mongodb.net:27017,mango-shard-00-01.btppp.mongodb.net:27017,mango-shard-00-02.btppp.mongodb.net:27017/myFirstDatabase?replicaSet=atlas-p04wl5-shard-0"
except ImportError:
    print("Database credentials must be first defined in credentials.py! Exiting.")


def connect_mongo():
    global db_url
    client = MongoClient(db_url)
    return client