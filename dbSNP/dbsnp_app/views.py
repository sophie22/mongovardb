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


def results(request):
    search_dict = {}
    filter_str = ""

    if request.GET.get('exact'):
        try:
            if request.GET['chrom'] is not None:
                search_dict.update({"mappings.seq_region_name": request.GET['chrom']})
                filter_str += "chromosome: " + request.GET['chrom'] + ", "
        except: pass
        if request.GET['start'] is not None and request.GET['start'] != "":
            search_dict.update({"mappings.start": int(request.GET['start'])})
            filter_str += "start position: " + request.GET['start'] + ", "
        if request.GET['end'] is not None and request.GET['end'] != "":
            search_dict.update({"mappings.end": int(request.GET['end'])})
            filter_str += "end position: " + request.GET['end'] + ", "
        try:
            if request.GET['vartype'] is not None:
                search_dict.update({"var_class": request.GET['vartype']})
                filter_str += "variant type: " + request.GET['vartype'] + ", "
        except: pass
        try:
            if request.GET['conseq'] is not None:
                search_dict.update({"most_severe_consequence": request.GET['conseq']})
                filter_str += "consequence: " + request.GET['conseq'] + ", "
        except: pass
        try:
            if request.GET['clinsig'] is not None:
                search_dict.update({"clinical_significance": request.GET['clinsig']})
                filter_str += "clinical significance: " + request.GET['clinsig'] + ", "
        except: pass

    elif request.GET.get('range'):
        try:
            if request.GET['range_chr'] is not None:
                search_dict.update({"mappings.0.seq_region_name": request.GET['range_chr']})
                filter_str += "chromosome: " + request.GET['range_chr'] + ", "
        except: pass
        if request.GET['range_start'] is not None and request.GET['range_start'] != "" and \
            request.GET['range_end'] is not None and request.GET['range_end'] != "":
            search_dict.update({"mappings.start": { "$gte": int(request.GET['range_start'])},
            "mappings.end": { "$lte": int(request.GET['range_end'])}})
            filter_str += "starting from: " + request.GET['range_start'] + ", "
            filter_str += "ending until: " + request.GET['range_end'] + ", "
        try: # MAF value is a string, so this does not actually work!!
            if request.GET['MAF'] is not None:
                low = request.GET['MAF'].split("-")[0]
                high = request.GET['MAF'].split("-")[1]
                search_dict.update({"minor_allele_frequency": { "$gte": low , "$lte": high}})
                filter_str += "MAF between: " + request.GET['MAF'] + ", "
        except: pass

    try:
        if request.GET['limit'] is not None and request.GET['limit'] != "":
            limit = int(request.GET['limit'])
    except:
        limit = 20

    data_list = query_db(search_dict, limit)
    content_dict = {'filters': filter_str, 'variants': data_list}
    return render(request, "dbsnp_app/results.html", content_dict)
