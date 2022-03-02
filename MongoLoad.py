import sys
import json
import pymongo

input_file = "variants.json" # sys.argv[1]

### Import database credentials and path to IR_json files
try:
    from dbSNP.dbsnp_app.credentials import mongodb_cred
    host = mongodb_cred['host']
    username = mongodb_cred['username']
    password = mongodb_cred['password']
    database = mongodb_cred['database'] # dbSNP
    collection = mongodb_cred['collection'] # dbSNP_coll
    db_url = f"mongodb+srv://{username}:{password}@{host}/{database}?retryWrites=true&w=majority"
except ImportError:
    print("Database credentials must be first defined in credentials.py! Exiting.")
    sys.exit(-1)

client = pymongo.MongoClient(db_url)
db = client[database]
collection = db[collection]

with open(input_file) as fh:
    for i, line in enumerate(fh):
        data = json.loads(line.strip())
        collection.update_one(data, {"$set": data}, upsert=True)

