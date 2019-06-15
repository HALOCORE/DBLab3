from django.http import HttpResponse
from django.http import QueryDict
from . import db_connect, api__REQUEST

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET': # 查询员工
        metadata, data = api__REQUEST.query_fuzz(
            [], 'staff', request.GET)
        return db_connect.httpRespOK("OK", metadata, data)

    elif request.method == 'POST': # 新建员工
        staffID = request.POST.get('staffID')
        if staffID is None:
            return db_connect.httpRespError()
        else:
            api__REQUEST.insert_one('staff', request.POST)
            return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id(request, staff_id):
    if request.method == 'GET': # 获取一个员工信息
        metadata, data = api__REQUEST.specify_get([], 'staff', 'staffID', staff_id)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'PUT': # 更新一个员工信息
        put = QueryDict(request.body)
        field = put.getlist('field',None)
        field_value = put.getlist('field_value',None)
        api__REQUEST.specify_update('staff',field,field_value,'staffID',staff_id)
        return db_connect.httpRespOK("OK")
    elif request.method == 'DELETE': # 删除一个员工信息
        api__REQUEST.specify_delete('staff', 'staffID', staff_id)
        return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_cusaccount(request, staff_id):
    if request.method == 'GET': # 列出某个指定员工的所有管理账户信息
        sql = "SELECT * from cusAccount, depositAccount WHERE " + \
            "cusA_accountIDX = accountIDX " + \
            "and staf_staffID = %s"
        param = (staff_id,)
        metadata1, data1 = api__REQUEST.query_all(sql, param)
        
        sql = "SELECT * from cusAccount, chequeAccount WHERE " + \
            "cusA_accountIDX = accountIDX " + \
            "and staf_staffID = %s"
        param = (staff_id,)
        metadata2, data2 = api__REQUEST.query_all(sql, param)
        return db_connect.httpRespOK("OK", [metadata1, metadata2], [data1, data2])
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_loan(request, staff_id):
    if request.method == 'GET': # 列出某个指定员工的所有负责贷款
        sql = "SELECT * from loan WHERE staf_staffID = %s"
        param = (staff_id,)
        metadata, data = api__REQUEST.query_all(sql, param)
        return db_connect.httpRespOK("OK", metadata, data)
    else:
        return db_connect.httpRespError()
