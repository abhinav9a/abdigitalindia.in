# context_processors.py

from .models import Wallet, OtherServices2, Wallet2

def wallet_balance(request):
    # Default balance to 0 if the user is not authenticated
    balance = 0.0
    
    if request.user.is_authenticated:
        wallet = Wallet.objects.get_or_create(userAccount=request.user)[0]
        balance = wallet.balance
    
    return {'wallet_balance': balance}


def wallet2_balance(request):
    # Default balance to 0 if the user is not authenticated
    balance = 0.0

    if request.user.is_authenticated:
        wallet = Wallet2.objects.get_or_create(userAccount=request.user)[0]
        balance = wallet.balance

    return {'wallet2_balance': balance}


def external_service_nav(request):
    external_services = OtherServices2.objects.all()
    
    return {'external_services': external_services}
