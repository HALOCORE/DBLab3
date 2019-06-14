from django.http import HttpResponse
from . import db_connect
import json

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET': # 查询客户
        pass
    elif request.method == 'POST': # 新建客户
        pass
    else:
        return db_connect.httpRespError()

@db_connect.auto_auth
def handle_id(request, customer_id):
    # 处理GET
    if request.method == 'GET':
        info = request.GET
        data = {
            "data":"fdsd",
            "weweq":"dsdsa",
        }
        return db_connect.httpRespOK("OK", data=data)
        # TODO
    elif request.method == 'PUT': # 更新一个客户信息
        pass
    elif request.method == 'DELETE': # 删除一个客户信息
        pass
    else:
        return db_connect.httpRespError()
    
    

@db_connect.auto_auth
def handle_id_cusaccount(request, customer_id):
    return HttpResponse("handle_id_cusaccount ! ")


def handle_id_loan(request, customer_id):
    return HttpResponse("handle_id_loan ! ")