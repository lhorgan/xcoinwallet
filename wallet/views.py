from django.shortcuts import render
from django.http import HttpResponse

from wallet.wallet_helper import *

def login(request):
    return 0

def wallet(request):
    return render(request, "wallet.html", {"user": request.user})

def balance(request):
    compiled_code = get_compiled_code()
    balance = tally_value(compiled_code, request.user)
    return HttpResponse(balance)

def send(request):
    print(request.POST)
    compiled_code = get_compiled_code()
    send_xcoins(compiled_code, request.POST["address"], request.POST["amount"], request.user)
    return HttpResponse("Hooray!")