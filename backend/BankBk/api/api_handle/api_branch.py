

from django.http import HttpResponse

def handle_main(request):
    return HttpResponse("handle_main ! ")


def handle_id(request):
    return HttpResponse("handle_id ! ")
