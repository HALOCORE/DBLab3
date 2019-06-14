from django.http import HttpResponse
from . import db_connect

@db_connect.auto_auth
def handle_deposit(request):
    return HttpResponse("handle_main ! ")

@db_connect.auto_auth
def handle_cheque(request):
    return HttpResponse("handle_id ! ")

@db_connect.auto_auth
def handle_deposit_id(request, deposit_id):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT': # 更新
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_cheque_id(request, deposit_id):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT': # 更新
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id(request, account_id):
    if request.method == 'DELETE':
        pass
    else:
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_id_customer(request, account_id):
    if request.method == 'GET':
        pass
    else:
        return db_connect.httpRespError()


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