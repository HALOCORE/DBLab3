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

auth_token_user = {
    # "efotj34f83w":("leit", ...日期时间...),
    # "rf9348fjq1e":("union", ..),
    # "zc0q9e1dq11":("hqy", ..),
}

auth_user_token = {
    'leit':[],  # ['efotj34f83w'],
    'union':[], # ['rf9348fjq1e'],
    'hqy':[]    # ['zc0q9e1dq11']
}

import random
from datetime import date, datetime
def gen_token():
    token = "".join([chr(random.randint(ord('a'), ord('z'))) for _ in range(11)])
    return token


def check_user_pwd(user:str, pwd:str):
    """检查某个用户是否有效"""
    if user in AUTH_USERS:
        if pwd == AUTH_USERS[user]:
            new_token = gen_token()
            auth_user_token[user].append(new_token)
            auth_token_user[new_token] = (user, datetime.now())
            return new_token
    return None


def check_token(token:str):
    """检查某个token"""
    if token in auth_token_user:
        if token in auth_token_user:
            return auth_token_user[token][0]
    return None



MSG_UNDEFINE = {"status": "undefined"}
MSG_FORBIDDEN = {"status": "forbidden"}
MSG_ERROR = {"status": "error"}

from django.http import HttpResponse
import json
from decimal import Decimal

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def httpSetToken(token:str):
    resp_dict = {'status': 'OK', 'describe': 'set token in cookie.'}
    resp = HttpResponse(json.dumps(resp_dict, ensure_ascii=False, cls=CJsonEncoder), status=200, content_type=JSON_CONTENT_TYPE)
    resp['Set-Cookie'] = 'token='+token + '; Max-Age=600; Path=/;'
    return resp

def httpRespForbidden(msg=""):
    resp_dict = MSG_FORBIDDEN.copy()
    resp_dict['describe'] = msg
    resp = HttpResponse(json.dumps(resp_dict, ensure_ascii=False, cls=CJsonEncoder), status=403, content_type=JSON_CONTENT_TYPE)
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Allow-Methods'] = 'POST,GET,DELETE,PUT'
    resp['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

def httpRespError(msg=""):
    resp_dict = MSG_ERROR.copy()
    resp_dict['describe'] = msg
    resp = HttpResponse(json.dumps(resp_dict, ensure_ascii=False, cls=CJsonEncoder), status=400, content_type=JSON_CONTENT_TYPE)
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Allow-Methods'] = 'POST,GET,DELETE,PUT'
    resp['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

def httpRespOK(status:str, metadata=None, data=None):
    """状态，元数据字典，数据字典"""
    data_pack = {"status":status, "metadata":metadata, "data":data}
    resp = HttpResponse(json.dumps(data_pack, ensure_ascii=False, cls=CJsonEncoder, indent=2), status=200, content_type=JSON_CONTENT_TYPE)
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Allow-Methods'] = 'POST,GET,DELETE,PUT'
    resp['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp
# --------------------- 权限检查装饰器 ---------------------

from pymysql import MySQLError

class MyDeleteError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "(DeleteErr: primary key not found. %s)" % self.msg

class MyUpdateError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "(UpdateErr: param invalid. %s)" % self.msg

def auto_auth(func):
    def wrapper(*args, **kwargs):
        msg = MSG_FORBIDDEN
        cookie = args[0].COOKIES
        auto_auth_user = None
        if 'token' in cookie:
            auto_auth_token = cookie['token']
            auto_auth_user = check_token(auto_auth_token)
        try:
            if auto_auth_user is not None:
                # 调用处理函数
                return func(*args, **kwargs)
            else:
                # 拒绝访问
                print("# debug mode. 权限检查关闭.")
                return httpRespForbidden('未通过安全验证.')
                # return func(*args, **kwargs)
        except MySQLError as err:
            if str(err).find('1064') > 0:
                raise err
            return httpRespError(str(err))
        except MyDeleteError as err:
            return httpRespError(str(err))
        except MyUpdateError as err:
            return httpRespError(str(err))
        except KeyError as err:
            return httpRespError('可能是参数缺失造成参数字典KeyError. ' + str(err))
    return wrapper