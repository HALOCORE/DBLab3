

from django.http import HttpResponse
from django.db import connection

def handle_main(request):
    
    return HttpResponse("handle_main ! ")


def handle_id(request):
    return HttpResponse("handle_id ! ")
