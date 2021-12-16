import json
from bson import Decimal128
from django.db      import connection
from django.http    import JsonResponse
from .models        import item,pajak

def Get(request):
    query = f"""SELECT
        REPLACE(REPLACE(REPLACE(REPLACE(IFNULL(
            JSON_OBJECT(
            'data',
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id',itm.id,
                    'nama',itm.nama,
                    'pajak',(
                        SELECT
                            JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'id',paj.id,
                                    'nama',paj.nama,
                                    'rate',REPLACE(paj.rate,paj.rate,CONCAT(paj.rate,'%'))
                                )
                        )
                        FROM api_item_pajak paj
                    )
                )
            )
        ),JSON_OBJECT('data','[]')
        ),'\\\\','/'),'/',''),'\"[','['),']\"',']') as result
    FROM api_item_item itm"""
    cursor = connection.cursor()
    cursor.execute(query)
    res = cursor.fetchone()
    for item in res:
        res = str(item)
    return JsonResponse(json.loads(res),json_dumps_params={'indent': 4})

def Create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nama') is not None:
            i = item(nama=data.get('nama'))
            i.save()
        return JsonResponse({'success':(True if data.get('nama') is not None else False)},json_dumps_params={'indent': 4},safe=False)
    else:
        return JsonResponse({'success':False},json_dumps_params={'indent': 4},safe=False)

def Update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nama') is not None and data.get('id') is not None:
            i = item.objects.get(pk=int(data.get('id')))
            i.nama = data.get('nama')
            i.save()
        return JsonResponse({'success':(True if data.get('nama') is not None else False)},json_dumps_params={'indent': 4},safe=False)
    else:
        return JsonResponse({'success':False},json_dumps_params={'indent': 4},safe=False)

def Delete(request,id):
    if request.method == 'DELETE':
        if id is not None:
            i = item.objects.get(pk=int(id))
            i.delete()
        return JsonResponse({'success':(True if id is not None else False)},json_dumps_params={'indent': 4},safe=False)
    else:
        return JsonResponse({'success':False},json_dumps_params={'indent': 4},safe=False)


def PajakCreate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('nama') is not None:
            i = pajak(nama=data.get('nama'),rate=float(data.get('rate')))
            i.save()
        return JsonResponse({'success':(True if data.get('nama') is not None else False)},json_dumps_params={'indent': 4},safe=False)
    else:
        return JsonResponse({'success':False},json_dumps_params={'indent': 4},safe=False)

def PajakUpdate(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get('nama') is not None and data.get('id') is not None:
            i = pajak.objects.get(pk=int(data.get('id')))
            i.nama = data.get('nama')
            i.rate = float(data.get('rate'))
            i.save()
        return JsonResponse({'success':(True if data.get('nama') is not None else False)},json_dumps_params={'indent': 4},safe=False)
    else:
        return JsonResponse({'success':False},json_dumps_params={'indent': 4},safe=False)

def PajakDelete(request,id):
    if request.method == 'DELETE':
        if id is not None:
            i = pajak.objects.get(pk=int(id))
            i.delete()
        return JsonResponse({'success':(True if id is not None else False)},json_dumps_params={'indent': 4},safe=False)
    else:
        return JsonResponse({'success':False},json_dumps_params={'indent': 4},safe=False)