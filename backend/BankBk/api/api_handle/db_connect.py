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



MSG_UNDEFINE = {"status": "undefined"}
MSG_FORBIDDEN = {"status": "forbidden"}
MSG_ERROR = {"status": "error"}

from django.http import HttpResponse
import json
from datetime import date, datetime
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


def httpRespForbidden(msg=""):
    resp_dict = MSG_FORBIDDEN.copy()
    resp_dict['describe'] = msg
    resp = HttpResponse(json.dumps(resp_dict, ensure_ascii=False, cls=CJsonEncoder), status=403, content_type=JSON_CONTENT_TYPE)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

def httpRespError(msg=""):
    resp_dict = MSG_ERROR.copy()
    resp_dict['describe'] = msg
    resp = HttpResponse(json.dumps(resp_dict, ensure_ascii=False, cls=CJsonEncoder), status=400, content_type=JSON_CONTENT_TYPE)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp

def httpRespOK(status:str, metadata=None, data=None):
    """状态，元数据字典，数据字典"""
    data_pack = {"status":status, "metadata":metadata, "data":data}
    resp = HttpResponse(json.dumps(data_pack, ensure_ascii=False, cls=CJsonEncoder, indent=2), status=200, content_type=JSON_CONTENT_TYPE)
    resp['Access-Control-Allow-Origin'] = '*'
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
        auth_result = None
        if 'pwdtoken' in cookie:
            auth_result = check_token(cookie['pwdtoken'])
        try:
            if auth_result is not None:
                # 调用处理函数
                return func(*args, **kwargs)
            else:
                # 拒绝访问
                print("# debug mode. 权限检查关闭.")
                return func(*args, **kwargs)
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