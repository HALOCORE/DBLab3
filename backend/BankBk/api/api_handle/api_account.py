from django.http import HttpRequest, HttpResponse
from django.http import QueryDict
from . import db_connect, api__REQUEST

@db_connect.auto_auth
def handle_deposit(request:HttpRequest):
    # 查询储蓄账户
    if request.method == 'GET':
        sql = "SELECT * from cusAccount, depositAccount WHERE " + \
            "cusA_accountIDX = accountIDX"
        where = api__REQUEST.gen_where(query_dict=request.GET)
        if where != "":
            sql = sql + " and " + where
        metadata, data = api__REQUEST.query_all(sql, ())
        return db_connect.httpRespOK("OK", metadata, data)
    # 创建储蓄账户
    if request.method == 'POST':
        data = request.POST
        staffID = data['staf_staffID']
        customID = data['cust_customID']
        accountIDX = data['accountIDX']
        currency = data['currency']
        interest = float(data['interest'])
        remain = float(data['remain'])
        params = [staffID, customID, accountIDX, currency, interest, remain]
        api__REQUEST.call_procedure('proc_new_depAccount', params)
        return db_connect.httpRespOK('OK')
    else:
        return db_connect.httpRespError("不支持的method.")


@db_connect.auto_auth
def handle_cheque(request):
    # 查询支票账户
    if request.method == 'GET':
        sql = "SELECT * from cusAccount, chequeAccount WHERE " + \
            "cusA_accountIDX = accountIDX"
        where = api__REQUEST.gen_where(query_dict=request.GET)
        if where != "":
            sql = sql + " and " + where
        metadata, data = api__REQUEST.query_all(sql, ())
        return db_connect.httpRespOK("OK", metadata, data)
    # 创建支票账户
    if request.method == 'POST':
        data = request.POST
        staffID = data['staf_staffID']
        customID = data['cust_customID']
        accountIDX = data['accountIDX']
        remain = float(data['remain'])
        params = [staffID, customID, accountIDX, remain]
        api__REQUEST.call_procedure('proc_new_cheAccount', params)
        return db_connect.httpRespOK('OK')
    else:
        return db_connect.httpRespError("不支持的method.")


@db_connect.auto_auth
def handle_deposit_id(request, deposit_id):
    if request.method == 'GET':
        sql = "SELECT * from cusAccount, depositAccount WHERE " + \
            "cusA_accountIDX = accountIDX and accountIDX = %s"
        sqlparams = (deposit_id,)
        metadata, data = api__REQUEST.query_all(sql, sqlparams)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'PUT': # 更新
        put = QueryDict(request.body)
        field = put.getlist('field', None)
        field_value = put.getlist('field_value', None)
        if len(field) != 2:
            return db_connect.httpRespError("需要两个参数: 操作对应的 customID 和 更新后余额 remain")
        if field[0] != 'cust_customID' or field[1] != 'remain_change':
            return db_connect.httpRespError("两个参数依次是 cust_customID 和 remain_change.")
        custom_id = field_value[0]
        remain_change = float(field_value[1])
        api__REQUEST.call_procedure('proc_alter_depAccount',[deposit_id, custom_id, remain_change])
        return db_connect.httpRespOK("OK")
    elif request.method == 'DELETE':
        api__REQUEST.call_procedure('proc_delete_depAccount', [deposit_id])
        return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError("不支持的method.")


@db_connect.auto_auth
def handle_cheque_id(request, cheque_id):
    if request.method == 'GET':
        sql = "SELECT * from cusAccount, chequeAccount WHERE " + \
            "cusA_accountIDX = accountIDX and accountIDX = %s"
        sqlparams = (cheque_id,)
        metadata, data = api__REQUEST.query_all(sql, sqlparams)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'PUT': # 更新
        put = QueryDict(request.body)
        field = put.getlist('field', None)
        field_value = put.getlist('field_value', None)
        if len(field) != 2:
            return db_connect.httpRespError("需要两个参数: 操作对应的 customID 和 更新后余额 remain")
        if field[0] != 'cust_customID' or field[1] != 'remain_change':
            return db_connect.httpRespError("两个参数依次是 cust_customID 和 remain_change.")
        custom_id = field_value[0]
        remain_change = float(field_value[1])
        api__REQUEST.call_procedure('proc_alter_cheAccount',[cheque_id, custom_id, remain_change])
        return db_connect.httpRespOK("OK")
    elif request.method == 'DELETE':
        api__REQUEST.call_procedure('proc_delete_cheAccount', [cheque_id])
        return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError("不支持的method.")



@db_connect.auto_auth
def handle_id_customer(request, account_id):
    if request.method == 'GET':
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_staff(request, account_id):
    if request.method == 'GET':
        pass
    else:
        return db_connect.httpRespError()