from django.http import JsonResponse
from pymongo import MongoClient

def db_name():
    return 'db_javapro'

def mongod():
    client = MongoClient(host='localhost',port=int(27017),username='*',password='*')
    db_handle = client[db_name()]
    return db_handle

def api(request,data,method):
    return JsonResponse(data,json_dumps_params={'indent': 4},safe=False) if request.method == method else JsonResponse({"data":[]},json_dumps_params={'indent': 4},safe=False)

def api_e(request,data,method):
    return JsonResponse(data,json_dumps_params={'indent': 4},safe=False) if request.method == method else JsonResponse({"success":False},json_dumps_params={'indent': 4},safe=False)
