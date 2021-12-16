from django.urls import path
from . import mongo,mysql

urlpatterns = [
    # public requestor
    path('mongo/data'                 , mongo.Get     , name='GetData'),
    path('mongo/data/create'          , mongo.Create  , name='CreateData'),
    path('mongo/data/update'          , mongo.Update  , name='UpdateData'),
    path('mongo/data/delete/<str:id>' , mongo.Delete  , name='DeleteData'),
    path('mongo/dataPajak/create'          , mongo.PajakCreate  , name='CreateData'),
    path('mongo/dataPajak/update'          , mongo.PajakUpdate  , name='UpdateData'),
    path('mongo/dataPajak/delete/<str:id>' , mongo.PajakDelete  , name='DeleteData'),
    # public requestor
    path('mysql/data'                 , mysql.Get     , name='MGetData'),
    path('mysql/data/create'          , mysql.Create     , name='MGetData'),
    path('mysql/data/update'          , mysql.Update     , name='MGetData'),
    path('mysql/data/delete/<int:id>' , mysql.Delete     , name='MGetData'),
    path('mysql/dataPajak/create'          , mysql.PajakCreate     , name='MGetData'),
    path('mysql/dataPajak/update'          , mysql.PajakUpdate     , name='MGetData'),
    path('mysql/dataPajak/delete/<int:id>' , mysql.PajakDelete     , name='MGetData'),
]