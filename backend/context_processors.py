# context_processors.py

from django.contrib import messages
from core.models import UserAccount
from backend.models import Wallet, OtherServices2, Wallet2
from backend.utils import get_pay_sprint_headers
from backend.config.consts import PaySprintRoutes
import requests

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
        user = UserAccount.objects.get(username=request.user)
        # if user.userType == "Admin":
        #     response = requests.post(url=PaySprintRoutes.CREDIT_BALANCE.value, headers=get_pay_sprint_headers())
        #     if response.status_code == 200 and response.json().get("response_code") == 1:
        #         balance = response.json().get("wallet")
        #     else:
        #         messages.error(request, response.json().get("message"), extra_tags="danger")
        # else:
        wallet = Wallet2.objects.get_or_create(userAccount=request.user)[0]
        balance = wallet.balance

    return {'wallet2_balance': balance}


def external_service_nav(request):
    external_services = OtherServices2.objects.all()
    
    return {'external_services': external_services}
