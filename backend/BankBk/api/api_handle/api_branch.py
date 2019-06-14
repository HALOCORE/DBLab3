from django.http import HttpResponse
from django.http import QueryDict
from . import db_connect
from . import api__REQUEST

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET':#查询支行
        metadata, all_branch = api__REQUEST.query_fuzz(
            [], 'branch', request.GET)
        return db_connect.httpRespOK("OK",metadata,all_branch)
    
    elif request.method == 'POST':#新建一个支行
        branchName = request.POST.get('branchName')
        if branchName is None:
            return db_connect.httpRespError()
        else:
            api__REQUEST.insert_one('branch', request.POST)
            return db_connect.httpRespOK("OK")
    else:
        # 无法解析的请求类型
        return db_connect.httpRespError()


@db_connect.auto_auth
def handle_name(request, branch_name):
    if request.method == 'GET': # 获取一个支行信息
        metadata,data = api__REQUEST.specify_get(
            [],'branch', 'branchName', branch_name)
        return db_connect.httpRespOK("OK",metadata,data)
    elif request.method == 'PUT': # 更新一个支行信息
        put = QueryDict(request.body)
        field = put.get('field',None)
        field_value = put.get('field_value',None)
        api__REQUEST.specify_update('branch',field,field_value,'branchName',branch_name)
        return db_connect.httpRespOK("OK")
    elif request.method == 'DELETE': # 删除一个支行信息
        api__REQUEST.specify_delete('branch', 'branchName', branch_name)
    else:
        return db_connect.httpRespError()