from django.http import HttpResponse
from . import db_connect

@db_connect.auto_auth
def handle_main(request):
    return HttpResponse("handle_main ! ")

@db_connect.auto_auth
def handle_id(request):
    return HttpResponse("handle_id ! ")
