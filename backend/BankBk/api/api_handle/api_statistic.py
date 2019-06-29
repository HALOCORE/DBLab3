from django.http import HttpResponse, HttpRequest
from . import db_connect, api__REQUEST

@db_connect.auto_auth
def handle_deposit(request:HttpRequest):
    #按货币计算余额，储蓄账户数
    where = ""
    if len(request.GET) == 0:
        where = " WHERE accountType='deposit'"
    else:
        where = " WHERE "+api__REQUEST.gen_where(request.GET)+" AND accountType='deposit'"
    remain_title, remain_data = api__REQUEST.calc_currency(request.GET)
    count_title, count_data = api__REQUEST.calc_count("cusAccount",where)
    metadata = remain_title+count_title
    data = {"remain_sum":remain_data, "count_account":count_data}
    return db_connect.httpRespOK("OK",metadata,data)



@db_connect.auto_auth
def handle_cheque(request:HttpRequest):
    #余额之和，支票账户数
    where = " "
    if len(request.GET) == 0:
        where = " WHERE accountType='cheque'"
    else:
        where = " WHERE "+api__REQUEST.gen_where(request.GET)+" AND accountType='cheque'"
    remain_title, remain_data = api__REQUEST.calc_sum("remain","cusAccount",where)
    count_title, count_data = api__REQUEST.calc_count("cusAccount",where)
    metadata = remain_title+count_title
    data = {"remain_sum":remain_data, "count_account":count_data}
    return db_connect.httpRespOK("OK",metadata,data)
    

@db_connect.auto_auth
def handle_loan(request:HttpRequest):
    #贷款金额，发放金额，贷款记录数
    where = " "
    if len(request.GET) == 0:
        where = " "
    else:
        where = " WHERE " + api__REQUEST.gen_where(request.GET)
    loan_sum_title, loan_sum_data = api__REQUEST.calc_sum("loanAmount","loan",where)
    paid_sum_title, paid_sum_data = api__REQUEST.calc_sum("loanPaid","loan",where)
    loan_count_title, loan_count_data = api__REQUEST.calc_count("loan",where)
    metadata = loan_sum_title+paid_sum_title+ loan_count_title
    data = {"loan_sum":loan_sum_data,"paid_sum":paid_sum_data,"loan_count":loan_count_data}
    return db_connect.httpRespOK("OK",metadata,data)