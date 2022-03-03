from django.shortcuts import render
from django.http import HttpResponse
from .utils import connect_mongo
# import pandas as pd

### Import database and collection information
try:
    from .credentials import mongodb_cred
    database = mongodb_cred['database'] # dbSNP
    collection = mongodb_cred['collection'] # dbSNP_coll
except ImportError:
    print("Database credentials must be first defined in credentials.py! Exiting.")

# Create a connection to the Mongo Database
client = connect_mongo()
db_handle = client[database]
collection_handle = db_handle[collection]


def index(request):
    return HttpResponse("Hello, world. You're at the index page.")


def home(request):
    data_list = []
    variant_records = collection_handle.find().limit(22)
    # Print on the terminal
    for i, r in enumerate(variant_records):
        # if i == 10: break
        data_list.append({
            'dbSNP_ID': r['name'],
            # 'refGen': r['mappings'][0]['assembly_name'],
            'chr': r['mappings'][0]['seq_region_name'],
            'start': r['mappings'][0]['start'],
            'end': r['mappings'][0]['end'],
            'ref': r['ancestral_allele'],
            'alt': r['minor_allele'],
            'MAF': r['MAF'],
            'var_class': r['var_class']
        })
    content_dict = {'variants': data_list}
    return render(request, "dbsnp_app/home.html", content_dict)

def filter(request):
    
    data_list = []

    # getting search query from home page
    user_chr = request.GET.get("chr")
    user_start = request.GET.get("start")
    user_end = request.GET.get("end")

    # converting to integer to search
    int_start = int(user_start)
    int_end = int(user_end)

    variant_records = collection_handle.find({"mappings.0.start": int_start,"mappings.0.end": int_end, "mappings.0.seq_region_name": user_chr}).limit(22)
    #variant_records = collection_handle.find({"mappings.0.start": int_start}).limit(22)
    # Print on the terminal
    for i, r in enumerate(variant_records):
        # if i == 10: break
        data_list.append({
            'dbSNP_ID': r['name'],
            # 'refGen': r['mappings'][0]['assembly_name'],
            'chr': r['mappings'][0]['seq_region_name'],
            'start': r['mappings'][0]['start'],
            'end': r['mappings'][0]['end'],
            'ref': r['ancestral_allele'],
            'alt': r['minor_allele'],
            'MAF': r['MAF'],
            'var_class': r['var_class']
        })
    content_dict = {'variants': data_list}

    number_variants = len(content_dict)

    #content = {'table': content_dict, 'number': number_variants}

    return render(request, "dbsnp_app/results.html", content_dict)



# Available fields based on the first 200 records
# {'_id': <class 'bson.objectid.ObjectId'>,
# 'MAF': <class 'str'>, 'ambiguity': <class 'str'>, 'ancestral_allele': <class 'str'>,
# 'minor_allele': <class 'str'>, 'most_severe_consequence': <class 'str'>,
# 'name': <class 'str'>, 'source': <class 'str'>, 'var_class': <class 'str'>, 'failed': <class 'str'>
# 'evidence': <class 'list of strings of length 0-3'>, 'synonyms': <class 'list of strings of length 1-6'>,
#  'mappings': <class 'list of length 1 containing a dict'>}

# ['mappings'][0] fields:
# {'location': <class 'str'>, 'assembly_name': <class 'str'>, 'end': <class 'int'>,
# 'seq_region_name': <class 'str'>, 'strand': <class 'int'>, 'coord_system': <class 'str'>,
# 'allele_string': <class 'str'>, 'start': <class 'int'>}

