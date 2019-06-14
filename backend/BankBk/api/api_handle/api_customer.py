from django.http import HttpResponse
from . import db_connect
import json

@db_connect.auto_auth
def handle_main(request):
    return HttpResponse("handle_main ! ")

@db_connect.auto_auth
def handle_id(request):
    # 处理GET
    if request.method == 'GET':
        data = {
            "data":"fdsd",
            "weweq":"dsdsa",
        }
        msg = json.dumps(data)
    elif request.method == 'POST':
        pass
    
    return HttpResponse(msg, status=200, content_type=db_connect.JSON_CONTENT_TYPE)

@db_connect.auto_auth
def handle_id_cusaccount(request):
    return HttpResponse("handle_id_cusaccount ! ")


def handle_id_loan(request):
    return HttpResponse("handle_id_loan ! ")