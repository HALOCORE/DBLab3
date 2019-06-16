from django.http import HttpResponse, HttpRequest
from . import db_connect, api__REQUEST

@db_connect.auto_auth
def handle_deposit(request:HttpRequest):
    pass


@db_connect.auto_auth
def handle_cheque(request:HttpRequest):
    pass

@db_connect.auto_auth
def handle_loan(request:HttpRequest):
    pass