from django.shortcuts import render
from django.http import HttpResponse
from .utils import connect_mongo

# Create a connection to the Mongo Database
### Import database credentials and path to IR_json files
try:
    from .credentials import mongodb_cred
    database = mongodb_cred['database'] # dbSNP
    collection = mongodb_cred['collection'] # dbSNP_coll
except ImportError:
    print("Database credentials must be first defined in credentials.py! Exiting.")

client = connect_mongo()
db_handle = client[database]
collection_handle = db_handle[collection]

variant_records = collection_handle.find({})
# Print on the terminal
for i, r in enumerate(variant_records):
    if i == 2: break
    print(r.keys())



# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the index page.")