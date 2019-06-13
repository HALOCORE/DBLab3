from django.http import HttpResponse

def handle_main(request):
    return HttpResponse("staff handle_main ! ")


def handle_id(request):
    return HttpResponse("staff handle_id ! ")