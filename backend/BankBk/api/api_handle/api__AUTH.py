from django.http import HttpResponse, HttpRequest
from . import db_connect

def login(request:HttpRequest):
    if request.method == 'GET':
        if 'username' not in request.GET or 'password' not in request.GET:
            return db_connect.httpRespForbidden("登录请求格式错误")
        username = request.GET['username']
        password = request.GET['password']
        token = db_connect.check_user_pwd(username, password)
        if token == None:
            return db_connect.httpRespForbidden("用户名或密码错误")
        else:
            return db_connect.httpSetToken(token)
    else:
        return db_connect.httpRespError("不支持的method.")


def logout(request:HttpRequest):
    if request.method == 'GET':
        return db_connect.httpSetToken("")
    else:
        return db_connect.httpRespError("不支持的method.")