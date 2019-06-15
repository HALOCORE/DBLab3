from django.http import HttpRequest, HttpResponse
from django.http import QueryDict
from . import db_connect
from . import api__REQUEST

@db_connect.auto_auth
def handle_main(request:HttpRequest):
    if request.method == 'GET': # 查询客户
        metadata, data = api__REQUEST.query_fuzz(
            [], 'customer', request.GET)
        return db_connect.httpRespOK("OK",metadata, data)
    
    elif request.method == 'POST': # 新建客户
        customid = request.POST.get('customID')
        if customid is None:
            return db_connect.httpRespError()
        else:
            api__REQUEST.insert_one('customer', request.POST)
            return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError()

@db_connect.auto_auth
def handle_id(request:HttpRequest, customer_id):
    # 处理GET
    if request.method == 'GET': # 获取一个客户信息
        metadata, data = api__REQUEST.specify_get([], 'customer', 'customID', customer_id)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'PUT': # 更新一个客户信息
        put = QueryDict(request.body)
        field = put.getlist('field',None)
        field_value = put.getlist('field_value',None)
        api__REQUEST.specify_update('customer', field, field_value, 'customID', customer_id)
        return db_connect.httpRespOK("OK")
    elif request.method == 'DELETE': # 删除一个客户信息
        api__REQUEST.specify_delete('customer', 'customID', customer_id)
        return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_cusaccount(request:HttpRequest, customer_id):
    if request.method == 'GET':
        sql = "SELECT * from cusAccount, depositAccount WHERE " + \
            "cusA_accountIDX = accountIDX " + \
            "and accountIDX in " + \
            "(SELECT depo_cusA_accountIDX from cus_and_depAccount WHERE "+ \
            "cust_customID = %s)"
        param = (customer_id,)
        metadata1, data1 = api__REQUEST.query_all(sql, param)
        
        sql = "SELECT * from cusAccount, chequeAccount WHERE " + \
            "cusA_accountIDX = accountIDX " + \
            "and accountIDX in " + \
            "(SELECT cheq_cusA_accountIDX from cus_and_cheAccount WHERE "+ \
            "cust_customID = %s)"
        param = (customer_id,)
        metadata2, data2 = api__REQUEST.query_all(sql, param)
        return db_connect.httpRespOK("OK", [metadata1, metadata2], [data1, data2])
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_loan(request:HttpRequest, customer_id):
    if request.method == 'GET':
        sql = "SELECT * from loan WHERE " + \
            "loanIDX in " + \
            "(SELECT loan_loanIDX from cus_and_loan WHERE "+ \
            "cust_customID = %s)"
        param = (customer_id,)
        metadata, data = api__REQUEST.query_all(sql, param)
        return db_connect.httpRespOK("OK", metadata, data)
    else:
        return db_connect.httpRespError()