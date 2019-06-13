from django.http import HttpResponse

def handle_main(request):
    return HttpResponse("handle_main ! ")


def handle_id(request):
    return HttpResponse("handle_id ! ")


def handle_id_cusaccount(request):
    return HttpResponse("handle_id_cusaccount ! ")


def handle_id_loan(request):
    return HttpResponse("handle_id_loan ! ")