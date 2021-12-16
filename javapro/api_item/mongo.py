import json
from pymongo import ReturnDocument
from bson.objectid import ObjectId
from django.http import JsonResponse, QueryDict, multipartparser
from .database import mongod, api, api_e

# Create your views here.
def Get(request):
    # GET REQUEST
    col = mongod().item
    res = list(col.aggregate([
        {'$lookup':{
            'from':'config',
            'pipeline':[
                {'$match':{'type':'pajak'}},
                {'$unwind':'$data'},
                {'$project':{
                    '_id'   : 0,
                    'id'    : {'$toString':'$data.id'},
                    'nama'  : '$data.nama',
                    'rate'  : {'$concat':[{'$toString':'$data.rate'},'%']}
                }}
            ],
            'as':'pajak'
        }},
        {'$project':{
            '_id'   : 0,
            'data'  : {
                'id'    : {'$toString': '$_id'},
                'nama'  : '$nama',
                'pajak' : '$pajak'
            }
        }},
        {'$group':{
            '_id'   : 0,
            'data'  : {'$push':'$data'}
        }},
        {'$project':{
            '_id'   : 0,
        }}
    ]))
    return api(request,res[0],'GET')

def Create(request):
    # POST REQUEST
    col = mongod().item
    dic = json.loads(request.body)
    res = None
    # insert if nama exist
    if dic.get('nama') is not None and request.method == 'POST':
        res = col.find_one_and_update({'nama':dic.get('nama')},{'$set':{'nama':dic.get('nama')}},upsert=True)
    # proccess response
    if res is None:
        return api_e(
                    request,
                    {'success':True},
                    'POST'
                ) 
    else:
        return JsonResponse(
                    {'success':False},
                    json_dumps_params={'indent': 4},
                    safe=False
                )

def Update(request):
    # PUT REQUEST
    col     = mongod().item
    data    = json.loads(request.body)
    res     = None
    # update if exist
    if data.get('id') is not None and request.method == 'PUT':
        res     = col.update_one(
                        {
                            '_id':ObjectId(data.get('id'))
                        },
                        {
                            '$set':{
                                'nama':data.get('nama')
                            }
                        }
                    )
    # proccess response
    if res is not None and res.modified_count is not 0:
        return api_e(
                    request,
                    {'success':True},
                    'PUT'
                )  
    else: 
        return JsonResponse(
                    {'success':False},
                    json_dumps_params={'indent': 4},
                    safe=False
                )

def Delete(request,id):
    # DELETE REQUEST
    col = mongod().item
    # delete if id exist
    res = col.delete_one({'_id':ObjectId(id)}) if id is not None and request.method == 'DELETE' else None
    # proccess response
    if res is not None and res.deleted_count is not 0:
        return api_e(
                request,
                {'success':True},
                'DELETE'
            ) 
    else:
        return JsonResponse(
                    {'success':False},
                    json_dumps_params={'indent': 4},
                    safe=False
                )

def PajakCreate(request):
    col = mongod().config
    data    = json.loads(request.body)
    # delete if id exist
    res = None
    if data.get('nama') is not None and request.method == 'POST':
        res = col.update_one(
                    {'type':'pajak'},
                    {'$push':{
                            'data':{
                                'id'    :ObjectId(),
                                'nama'  :data.get('nama'),
                                'rate'  :float(data.get('rate'))
                            }
                        }
                    }
                )
    # proccess response
    if res is not None and res.modified_count is not 0:
        return api_e(
                request,
                {'success':True},
                'POST'
            ) 
    else:
        return JsonResponse(
                    {'success':False},
                    json_dumps_params={'indent': 4},
                    safe=False
                )

def PajakUpdate(request):
    # PUT REQUEST
    col     = mongod().config
    data    = json.loads(request.body)
    res     = None
    # update if exist
    if data.get('id') is not None and request.method == 'PUT':
        res     = col.update_one(
                        {
                            '$and':[
                                {'type':'pajak'},
                                {'data.id':ObjectId(data.get('id'))}
                            ]
                        },
                        {
                            '$set':{
                                'data.$.nama':data.get('nama'),
                                'data.$.rate':float(data.get('rate'))
                            }
                        }
                    )
    # proccess response
    if res is not None and res.modified_count is not 0:
        return api_e(
                request,
                {'success':True},
                'PUT'
            ) 
    else:
        return JsonResponse(
                    {'success':False},
                    json_dumps_params={'indent': 4},
                    safe=False
                )

def PajakDelete(request,id):
    # DELETE REQUEST
    col = mongod().config
    # delete if id exist
    res = None
    if id is not None and request.method == 'DELETE':
        res = col.update_one(
                    {'type':'pajak'},
                    {'$pull':{
                            'data':{'id':ObjectId(id)}
                        }
                    }
                )

    # proccess response
    if res is not None and res.modified_count is not 0:
        return api_e(
                request,
                {'success':True},
                'DELETE'
            ) 
    else:
        return JsonResponse(
                    {'success':False},
                    json_dumps_params={'indent': 4},
                    safe=False
                )