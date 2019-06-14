from django.http import HttpResponse
from . import db_connect
from . import api__REQUEST

@db_connect.auto_auth
def handle_main(request):
    if request.method == 'GET':#查询支行
        branch = request.GET.get('branch')
        if branch is None:#查询所有支行
            metadata,all_branch = api__REQUEST.query_table('branch')
            return db_connect.httpRespOK("OK",metadata,all_branch)
        else:#按名字查询
            query = {}
            query['branchName'] = branch
            metadata,data = api__REQUEST.query_specify([],'branch',query)
            return db_connect.httpRespOK("OK",metadata,data)
    elif request.method == 'POST':#新建一个支行
        city = request.POST.get('city','')
        branchName = request.POST.get('name')
        #
        if branchName is None:
            return db_connect.httpRespError()
        else:
            data = {}
            data['city'] = city
            data['branchName'] = branchName
            api__REQUEST.insert_one('branch',data)
            return db_connect.httpRespOK("OK")
    else:
        # 无法解析的请求类型
        return db_connect.httpRespError()

@db_connect.auto_auth
def handle_name(request, branch_name):
    return db_connect.httpRespOK("ooo")
    if request.method == 'GET': # 获取一个支行信息
        pass
    elif request.method == 'PUT': # 更新一个支行信息
        pass
    elif request.method == 'DELETE': # 删除一个支行信息
        pass
    else:
        return db_connect.httpRespError()