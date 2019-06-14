import pymysql

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'

# Connect to the database
connection = pymysql.connect(host='193.112.68.240',
                             port=3306,
                             user='root',
                             password='612089',
                             db='BankDB',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)#游标类型可不设置，再看

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



MSG_UNDEFINE = '{"status": "undefined"}'
MSG_FORBIDDEN = '{"status": "forbidden"}'
MSG_ERROR = '{"status": "error"}'

from django.http import HttpResponse
import json

def httpRespForbidden(msg=MSG_FORBIDDEN):
    return HttpResponse(json.dumps(msg), status=403, content_type=JSON_CONTENT_TYPE)

def httpRespError(msg=MSG_ERROR):
    return HttpResponse(json.dumps(msg), status=400, content_type=JSON_CONTENT_TYPE)

def httpRespOK(status:str, metadata=None, data=None):
    """状态，元数据字典，数据字典"""
    data_pack = {"status":status, "metadata":metadata, "data":data}
    return HttpResponse(json.dumps(data_pack), status=200, content_type=JSON_CONTENT_TYPE)

# --------------------- 权限检查装饰器 ---------------------



def auto_auth(func):
    def wrapper(*args, **kwargs):
        msg = MSG_FORBIDDEN
        cookie = args[0].COOKIES
        auth_result = None
        if 'pwdtoken' in cookie:
            auth_result = check_token(cookie['pwdtoken'])
        if auth_result is not None:
            # TODO:
            # 调用处理函数
            return func(*args, **kwargs)
        else:
            # 拒绝访问
            print("# debug mode. 权限检查关闭.")
            return func(*args, **kwargs)
            # return HttpResponse(json.dumps(msg), status=403, content_type=JSON_CONTENT_TYPE)
    return wrapper