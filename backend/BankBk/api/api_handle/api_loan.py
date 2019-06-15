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
            api__REQUEST.insert_one('loan', request.POST)
            return db_connect.httpRespOK("OK")
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id(request, loan_id):
    if request.method == 'GET': # 查询
        metadata, data = api__REQUEST.specify_get([], 'loan', 'loanIDX', loan_id)
        return db_connect.httpRespOK("OK", metadata, data)
    elif request.method == 'DELETE': # 新建
        pass
        return db_connect.httpRespError()
        # TODO: 存储过程
    elif request.method == 'POST': # 发放贷款
        pass
        return db_connect.httpRespError()
        # TODO: 存储过程
    else:
        return db_connect.httpRespError()