import pymysql

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'

MSG_UNDEFINE = '{"status": "undefined"}'
MSG_FORBIDDEN = '{"status": "forbidden"}'
MSG_ERROR = '{"status": "error"}'

connection = "sdsdsds"

print("# db_connect: 初始化connection.")

AUTH_USERS = {
    "leit":"123456",
    "union":"654321",
    "hqy":"666",
}

auth_pwd_tokens = {
    "efotj34f83w":["leit", '20190614'],
    "rf9348fjq1e":["union", '20190614'],
    "zc0q9e1dq11":["hqy", '20190614'],
}

def check_user_pwd(user:str, pwd:str):
    """检查某个用户是否有效"""
    if user in AUTH_USERS:
        if pwd == AUTH_USERS[user]:
            return True
    return False

def check_token(token:str):
    """检查某个token"""
    if token in auth_pwd_tokens:
        return auth_pwd_tokens[token]
    return None



# --------------------- 权限检查装饰器 ---------------------

from django.http import HttpResponse
import json

def auto_auth(func):
    def wrapper(request):
        msg = MSG_FORBIDDEN
        cookie = request.COOKIES
        auth_result = None
        if 'pwdtoken' in cookie:
            auth_result = check_token(cookie['pwdtoken'])
        if auth_result is not None:
            # 调用处理函数
            return func(request)
        else:
            # 拒绝访问
            print("# debug mode. 权限检查关闭.")
            return func(request)
            # return HttpResponse(json.dumps(msg), status=403, content_type=JSON_CONTENT_TYPE)
    return wrapper