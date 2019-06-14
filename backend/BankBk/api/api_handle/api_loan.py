from django.http import HttpResponse
from . import db_connect

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET': # 查询
        pass
    elif request.method == 'POST': # 新建
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id(request, loan_id):
    if request.method == 'GET': # 查询
        pass
    elif request.method == 'DELETE': # 新建
        pass
    elif request.method == 'POST': # 新建
        pass
    else:
        return db_connect.httpRespError()