from django.http import HttpResponse
from . import db_connect

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET': # 查询员工
        pass
    elif request.method == 'POST': # 新建员工
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id(request, staff_id):
    if request.method == 'GET': # 获取一个员工信息
        pass
    elif request.method == 'PUT': # 更新一个员工信息
        pass
    elif request.method == 'DELETE': # 删除一个员工信息
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_cusaccount(request, staff_id):
    if request.method == 'GET': # 列出某个指定员工的所有管理账户信息
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_loan(request, staff_id):
    if request.method == 'GET': # 列出某个指定员工的所有负责贷款
        pass
    else:
        return db_connect.httpRespError()
