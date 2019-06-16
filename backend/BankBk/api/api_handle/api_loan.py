from django.http import HttpResponse
from . import db_connect, api__REQUEST

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET': # 查询
        metadata, data = api__REQUEST.query_fuzz(
            [], 'loan', request.GET)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'POST': # 新建
        loan_idx = request.POST.get('loanIDX')
        if loan_idx is None:
            return db_connect.httpRespError()
        else:
            loan_data = request.POST
            loan_data['loanState'] = 1
            loan_data['loanPaid'] = 0
            api__REQUEST.insert_one('loan', loan_data)
            return db_connect.httpRespOK("OK")
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id(request, loan_id):
    if request.method == 'GET': # 查询
        metadata, data = api__REQUEST.specify_get([], 'loan', 'loanIDX', loan_id)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'DELETE': # 删除
        # 无返回值的存储过程。
        # 删除时判断能不能删。如果能删，先删记录再删贷款；
        #                   如果不能删，存储过程抛出异常。
        api__REQUEST.call_procedure('proc_delete_loan', [loan_id])
        return db_connect.httpRespOK('OK')
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_pay(request, loan_id):
    if request.method == 'GET': # 获取发放记录
        sql = 'SELECT * FROM loanPay WHERE loan_loanIDX = %s'
        params = (loan_id,)
        metadata, data = api__REQUEST.query_all(sql, params)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'POST': # 发放贷款
        # 发放贷款 存储过程3个参数
        params = [loan_id, request.POST['loanPayDate'], float(request.POST['loanPayAmount'])]
        api__REQUEST.call_procedure("proc_pay_loan", params)
        return db_connect.httpRespOK("OK")
    else:
        return db_connect.httpRespError()