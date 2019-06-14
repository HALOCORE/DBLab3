from django.http import HttpResponse
from django.http import QueryDict
from . import db_connect
from . import api__REQUEST
import json

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET': # 查询客户
        metadata, data = api__REQUEST.query_fuzz(
            [], 'customer', request.GET)
        return db_connect.httpRespOK("OK",metadata, data)
    
    elif request.method == 'POST': # 新建客户
        branchName = request.POST.get('branchName')
        if branchName is None:
            return db_connect.httpRespError()
        else:
            api__REQUEST.insert_one('branch', request.POST)
            return db_connect.httpRespOK("OK")
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
        put = QueryDict(request.body)
        field = put.get('field',None)
        field_value = put.get('field_value',None)
        api__REQUEST.specify_update('branch',field,field_value,'branchName',branch_name)
        return db_connect.httpRespOK("OK")
    elif request.method == 'DELETE': # 删除一个客户信息
        pass
    else:
        return db_connect.httpRespError()
    
    

@db_connect.auto_auth
def handle_id_cusaccount(request, customer_id):
    return HttpResponse("handle_id_cusaccount ! ")


def handle_id_loan(request, customer_id):
    return HttpResponse("handle_id_loan ! ")