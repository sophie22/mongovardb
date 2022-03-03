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


def query_db(search_dict, limit):
    data_list = []
    variant_records = collection_handle.find(search_dict).limit(limit)
    # Print on the terminal
    for i, record in enumerate(variant_records):
        # if i == 10: break
        if 'clinical_significance' not in record.keys():
            clinsig = None
        else:
            clinsig = ', '.join(record['clinical_significance'])

        data_list.append({
            'dbSNP_ID': record['name'],
            'refGen': record['mappings'][0]['assembly_name'],
            'chr': record['mappings'][0]['seq_region_name'],
            'start': record['mappings'][0]['start'],
            'end': record['mappings'][0]['end'],
            'ref': record['ancestral_allele'],
            'alt': record['minor_allele'],
            'MAF': record['MAF'],
            'var_class': record['var_class'],
            'clin_sig': clinsig,
            'consequence': record['most_severe_consequence'],
            'evidence': ', '.join(record['evidence']),
            'synonyms': record['synonyms']
        })
    return data_list


def home(request):
    search_dict = {}
    limit = 20

    data_list = query_db(search_dict, limit)
    content_dict = {'variants': data_list}
    return render(request, "dbsnp_app/home.html", content_dict)

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

