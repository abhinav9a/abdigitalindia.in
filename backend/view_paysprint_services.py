from http.client import responses

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from decimal import Decimal, ROUND_DOWN
import requests
from datetime import datetime
import uuid

from urllib3 import request

from backend.utils import (is_kyc_completed, get_pay_sprint_headers, get_pay_sprint_payload, is_merchant_bank2_registered,
                           is_user_registered_with_paysprint, get_pay_sprint_common_payload, generate_unique_id,
                           is_bank2_last_authentication_valid, make_post_request)
from backend.models import (PaySprintMerchantAuth, PaySprintAadharPayTransactionDetails, Wallet, Payout,
                            PaySprintCashWithdrawlTransactionDetails, PaySprintPayoutBankAccountDetails)
from backend.config.consts import PaySprintRoutes, DMT_BANK_LIST, PAYOUT_TRANSACTION_STATUS
from core.models import UserAccount


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def user_onboarding(request):
    onboarding_details = UserAccount.objects.get(username=request.user)
    redirect_url = None
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        shop_name = request.POST.get('shop_name')

        payload = {
            "merchantcode": request.user.platform_id,
            "mobile": mobile_number,
            "is_new": "1",
            "email": email,
            "firm": shop_name,
            "callback": PaySprintRoutes.CALLBACK_URL.value
        }
        try:
            response = requests.post(PaySprintRoutes.WEB_ONBOARDING.value, json=payload, headers=get_pay_sprint_headers())
            if response.status_code == 200:
                if response.json().get('onboard_pending') == 0:
                    return redirect("dashboard")
                api_data = response.json()
                message = api_data.get('message')
                redirect_url = api_data.get('redirecturl', None)
                return render(request, 'backend/Services/AEPS/AEPS_PaySprint.html', {'url': redirect_url})
            else:
                api_data = response.json()
                message = api_data.get('message')
                messages.success(request, message=message, extra_tags='danger')
        except Exception as e:
            print('Custom Exception from paysprint onboarding==>', e)
            messages.success(request, message=e, extra_tags='danger')

    return render(request, 'backend/Pages/onboardingUserPaySprint.html', {'onboarding_details': onboarding_details})


def get_pay_sprint_aeps_bank_list():
    response = requests.post(PaySprintRoutes.AEPS_BANK_LIST.value, headers=get_pay_sprint_headers())
    if response.status_code == 200:
        bank_list = response.json().get('banklist').get('data')
        return bank_list

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
def balance_enquiry(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Balance Enquiry"
    if request.method == 'POST':
        data = get_pay_sprint_payload(request, user, "BE")
        response = make_post_request(url=PaySprintRoutes.BALANCE_ENQUIRY.value, data=data)
        if response.status_code == 200:
        # if True:
            response = response.json()
            # response = {
            #   "status": True,
            #   "message": "Request Completed",
            #   "ackno": 3214,
            #   "amount": 0,
            #   "balanceamount": "24287.44",
            #   "bankrrn": "2080****6068",
            #   "bankiin": "607152",
            #   "response_code": 1,
            #   "errorcode": "00",
            #   "clientrefno": "435678232323"
            # }
            return render(request, 'backend/Pages/balanceEnquiry.html', {"user": user, "heading": heading, "bank_list": bank_list, "data": response})
        else:
            messages.error(request, message=response.json().get("message"), extra_tags='danger')

    return render(request, 'backend/Pages/balanceEnquiry.html', {"user": user, "heading": heading, "bank_list": bank_list})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
@user_passes_test(is_merchant_bank2_registered, login_url='bank2_registration_paysprint')
def cash_withdrawl(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Cash Withdrawl"
    if request.method == 'POST':
        if not is_bank2_last_authentication_valid(user):
            merchant_authentication_bank_2_api(request=request, user=user)
        merchant_authenticity_response = merchant_authenticity_bank_2_api(request=request, user=user)
        if merchant_authenticity_response.status_code == 200 and is_bank2_last_authentication_valid(user):
        # if merchant_authenticity_response.get("response_code") == 1 and is_bank2_last_authentication_valid(user):
            merchant_auth_txn_id = PaySprintMerchantAuth.objects.get(userAccount=user).bank2_MerAuthTxnId
            data = get_pay_sprint_payload(request, user, "CW", merchant_auth_txn_id)
            response = make_post_request(url=PaySprintRoutes.CASH_WITHDRAWL.value, data=data)

            if response.status_code == 200:
            # if True:
                response = response.json()
                # response = {
                #   "status": True,
                #   "txnstatus": "1",
                #   "message": "Request Completed",
                #   "ackno": "30*****1",
                #   "amount": "100.00",
                #   "bankrrn": "2155*******4",
                #   "response_code": 1
                # }
                response_data = {
                    'userAccount': user,
                    'ack_no': response.get('ackno'),
                    'amount': response.get('amount'),
                    'bank_rrn': response.get('bankrrn'),
                    'txn_status': response.get('txnstatus'),
                }

                merchant_auth = PaySprintCashWithdrawlTransactionDetails.objects.create(**response_data)
                return render(request, 'backend/Pages/paymentSuccess.html', {"cash_withdrawl_response": response_data})
            else:
                messages.error(request, response.json().get("message"), extra_tags='danger')

    return render(request, 'backend/Pages/cashWithdrawl.html', {"user": user, "heading": heading, "bank_list": bank_list})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='bank2_registration_paysprint')
def mini_statement(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Mini Statement"
    if request.method == 'POST':
        data = get_pay_sprint_payload(request, user, "MS")
        response = make_post_request(url=PaySprintRoutes.MINI_STATEMENT.value, data=data)
        if response.status_code == 200:
        # if True:
            response = response.json()
            # response = {
            #   "status": True,
            #   "ackno": 40301468,
            #   "datetime": "2022-21-03 04:54:55",
            #   "balanceamount": "24287.44",
            #   "bankrrn": "2080****0104",
            #   "bankiin": "HDFC Bank",
            #   "message": "Request Completed",
            #   "errorcode": "00",
            #   "ministatement": [
            #     {
            #       "date": "30/06",
            #       "txnType": "Cr",
            #       "amount": "105.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "30/06",
            #       "txnType": "Dr",
            #       "amount": "105.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "31/05",
            #       "txnType": "Cr",
            #       "amount": "105.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "31/05",
            #       "txnType": "Dr",
            #       "amount": "105.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "30/04",
            #       "txnType": "Cr",
            #       "amount": "100.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "30/04",
            #       "txnType": "Dr",
            #       "amount": "100.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "31/03",
            #       "txnType": "Cr",
            #       "amount": "101.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "31/03",
            #       "txnType": "Dr",
            #       "amount": "101.0",
            #       "narration": " APD "
            #     },
            #     {
            #       "date": "01/03",
            #       "txnType": "Cr",
            #       "amount": "150.0",
            #       "narration": " APD "
            #     }
            #   ],
            #   "response_code": 1
            # }
        else:
            messages.error(request, response.json().get("message"), extra_tags='danger')

        return render(request, 'backend/Pages/miniStatement.html', {"user": user, "heading": heading, "bank_list": bank_list, "data": response})

    return render(request, 'backend/Pages/miniStatement.html', {"user": user, "heading": heading, "bank_list": bank_list})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
def aadhar_pay(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Aadhar Pay"
    if request.method == 'POST':
        data = get_pay_sprint_payload(request, user, "M")  # M OR FM OR IM
        response = make_post_request(url=PaySprintRoutes.AADHAR_PAY.value, data=data)
        if response.status_code == 200:
        # if True:
            response = response.json()
            # response = {
            #   "status": True,
            #   "message": "Request Completed",
            #   "ackno": 75,
            #   "amount": 100,
            #   "balanceamount": "1.00",
            #   "bankrrn": "120*****2463",
            #   "bankiin": "60**26",
            #   "response": 200,
            #   "response_code": 1
            # }
            response_data = {
                'userAccount': user,
                'ack_no': response.get('ackno'),
                'amount': response.get('amount'),
                'balance_amount': response.get('balanceamount'),
                'bank_rrn': response.get('bankrrn'),
                'bank_iin': response.get('bankiin'),
            }
            merchant_auth = PaySprintAadharPayTransactionDetails.objects.create(**response_data)
            return render(request, 'backend/Pages/paymentSuccess.html', {"aadhar_pay_response": response_data})
        else:
            messages.error(request, response.json().get("message"), extra_tags='danger')

    return render(request, 'backend/Pages/aadharPay.html', {"user": user, "heading": heading, "bank_list": bank_list})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
def merchant_registration_bank_2(request):
    user = UserAccount.objects.get(username=request.user)
    if request.method == 'POST':
        data = get_pay_sprint_common_payload(request, user)
        response = make_post_request(url=PaySprintRoutes.GET_LIST.value, data=data)
        api_data = response.json()
        if response.status_code == 200:
        # if True:
            merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
            if not merchant_auth:
                merchant_auth = PaySprintMerchantAuth.objects.create(userAccount=user, is_bank2_registered=True, registration_date=datetime.now())
            else:
                merchant_auth.is_bank2_registered = True
                merchant_auth.save()
            # Redirect to the next URL if provided
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
        else:
            messages.error(request, api_data.get('message'), extra_tags='danger')
    context = {
        "user": user,
        "is_registered": is_merchant_bank2_registered(user),
        "title": "Merchant Registration",
        "form_submit_url": "bank2_registration_paysprint"
    }
    return render(request, 'backend/Pages/merchantRegistrationPaySprint.html', context=context)


def merchant_authentication_bank_2_api(request, user):
    data = get_pay_sprint_common_payload(request, user)
    response = make_post_request(url=PaySprintRoutes.BANK_2_AUTHENTICATION.value, data=data)
    api_data = response.json()
    api_data = {
        "response_code": 1,
        "status": True,
        "message": "Two Factor Verification Success",
        "errorcode": "0"
    }
    if response.status_code == 200:
    # if api_data.get('response_code') == 1:
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        merchant_auth.bank2_last_authentication_date = datetime.now()
        merchant_auth.save()
    else:
        messages.error(request, api_data.get('message'), extra_tags='danger')
    return response




def merchant_authenticity_bank_2_api(request, user):
    data = get_pay_sprint_common_payload(request, user)
    response = make_post_request(url=PaySprintRoutes.BANK_2_MERCHANT_AUTHENTICITY.value, data=data)
    api_data = response.json()
    # api_data = {
    #   "response_code": 1,
    #   "status": True,
    #   "message": "Merchant Authenticated Successfully.",
    #   "errorcode": "0",
    #   "MerAuthTxnId": "dsdfs6f5df5f657s65fs5g76t34hhjgg34"
    # }

    if response.status_code == 200:
    # if api_data.get("response_code") == 1:
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        merchant_auth.bank2_MerAuthTxnId = api_data.get('MerAuthTxnId')
        merchant_auth.save()
    else:
        messages.error(request, api_data.get('message'), extra_tags='danger')
    return response
    # return api_data


##########
# PAYOUT
##########

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
def do_transaction(request):
    userObj = UserAccount.objects.get(username=request.user)
    bank_list = get_payout_bank_list(merchant_id=userObj.platform_id)
    activated_banks = [bank for bank in bank_list if bank['status'] == '1']
    document_upload_pending_banks = [bank for bank in bank_list if bank['status'] == '2']
    document_verification_pending_banks = [bank for bank in bank_list if bank['status'] == '3']

    if request.method == 'POST':
        amount = 0
        ref_id = generate_unique_id()
        try:
            amount = Decimal(request.POST.get('amount'))
        except ValueError:
            messages.error(request, 'Invalid amount')
            return redirect('transfer_fund')

        if amount <= 25000:
            x = 6
        else:
            x = 12

        payout_charge = amount + Decimal(x)
        payout_charge = payout_charge.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            messages.error(request, 'Wallet not found')
            return redirect('transfer_fund')
        except Exception as e:
            messages.error(request, f'Internal server error: {e}')
            return redirect('transfer_fund')

        # check the balance for service
        if wallet.balance >= payout_charge:
            try:
                data = {
                    "bene_id": request.POST.get("bene_id"),
                    "amount": float(amount),
                    "refid": ref_id,
                    "mode": request.POST.get("mode")
                }
                response = requests.post(PaySprintRoutes.DO_TRANSACTION.value, json=data, headers=get_pay_sprint_headers())
                api_data = response.json()

                if response.status_code == 200 and api_data.get("status"):
                    messages.success(request, api_data.get('message'))
                    payload = {
                        "refid":ref_id,
                        "ackno":api_data.get("ackno")
                    }
                    # Check the Transaction Status
                    response = requests.post(PaySprintRoutes.TRANSACTION_STATUS.value, json=payload, headers=get_pay_sprint_headers())
                    api_data = response.json()

                    if response.status_code == 200 and api_data.get("status"):
                        data = api_data.get("data")
                        payout_details = {
                            "userAccount": request.user,
                            "amount": data.get("amount"),
                            "txn_status": PAYOUT_TRANSACTION_STATUS.get(data.get("txn_status")),
                            "tid": data.get("utr") if data.get("utr") else "",
                            "client_ref_id": data.get("refid"),
                            "recipient_name": data.get("benename"),
                            "ifsc": data.get("ifsccode"),
                            "account": data.get("acno"),
                            "api_type": "pay_sprint"
                        }

                        # Charge user for DMT
                        wallet.balance -= float(data.get("charges"))
                        wallet.save()

                        # Create a transaction entry for wallet
                        Payout.objects.create(**payout_details)

                        return redirect('do_transaction')

                messages.error(request, api_data.get('message'), extra_tags="danger")
                return redirect('do_transaction')
            except Exception as e:
                messages.error(request, f'Internal server error: {e}')
                return redirect('do_transaction')
        else:
            messages.error(request, 'Insufficient Balance, Please Recharge Wallet.', extra_tags="danger")
            return redirect('do_transaction')

    context = {
        "activated_banks": activated_banks,
        "document_upload_pending_banks": document_upload_pending_banks,
        "document_verification_pending_banks": document_verification_pending_banks
    }
    return render(request, 'backend/Services/Payout/PayoutPaySprint.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
def add_bank(request):
    user = UserAccount.objects.get(username=request.user)
    if request.method == 'POST':
        data = {
            "merchant_code": user.platform_id,
            "account": request.POST.get('acc_no'),
            "bankid": request.POST.get('bank_id'),
            "ifsc": request.POST.get('ifsc').upper(),
            "name": request.POST.get('acc_name'),
            "account_type": request.POST.get('acc_type'),
        }
        response = requests.post(PaySprintRoutes.ADD_ACCOUNT.value, json=data, headers=get_pay_sprint_headers())
        api_data = response.json()
        print(">>>>>>>>>>>>>>>>>>>>>>>> ", api_data)
        # api_data = {'response_code': 2, 'status': True, 'acc_status': 2, 'bene_id': 1258814, 'message': 'Account Detailed saved successfully. Please upload Supportive Document to activate'}
        if api_data.get("response_code") in (1, 2):
        # if True:
            bank_acc = PaySprintPayoutBankAccountDetails.objects.filter(bene_id=api_data.get("bene_id")).first()
            if not bank_acc:
                data.pop("merchant_code")
                bank_acc = PaySprintPayoutBankAccountDetails.objects.create(bene_id=api_data.get("bene_id"), userAccount=user, **data)
                bank_acc.save()
            messages.success(request, message=api_data.get('message'), extra_tags='success')
            return redirect("do_transaction")
        else:
            messages.error(request, api_data.get('message'), extra_tags='danger')

    return render(request, 'backend/Services/Payout/AddBankAccPaySprint.html', {"bank_list": DMT_BANK_LIST})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url='onboarding_user_paysprint')
def upload_supporting_document(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_payout_bank_list(merchant_id=user.platform_id)
    bene_id = request.GET.get('bene_id')
    bank_details = next((f"{bank['name']} - {bank['bankname']} - {bank['account']} - {bank['ifsc']}"
                         for bank in bank_list if bank.get('status') == '2' and bank.get('beneid') == bene_id), "")

    if request.method == 'POST':
        doctype = request.POST.get("doctype")
        payload = {
            "doctype": doctype,
            "bene_id": bene_id,
        }

        files = {
            "passbook": ("panimage.jpg", request.FILES.get("passbook").read(), "image/jpeg")
        }

        if doctype == "PAN":
            files["panimage"] = ("panimage.jpg", request.FILES.get("panimage").read(), "image/jpeg")
        elif doctype == "AADHAR":
            files["front_aadhar"] = ("front_aadhar.jpg", request.FILES.get("front_aadhar").read(), "image/jpeg")
            files["back_aadhar"] = ("back_aadhar.jpg", request.FILES.get("back_aadhar").read(), "image/jpeg")

        response = requests.post(PaySprintRoutes.UPLOAD_DOCUMENT.value, data=payload, files=files, headers=get_pay_sprint_headers())
        print(">>>>>>>>>>>>>>> ", response.json())
        if response.json().get("status"):
            messages.success(request, response.json().get('message'), extra_tags='success')
            return redirect("do_transaction")
        else:
            messages.error(request, response.json().get('message'), extra_tags='danger')
            return redirect(reverse("upload_documents") + f"?bene_id={bene_id}")

    return render(request, 'backend/Services/Payout/UploadDocumentsPaySprint.html', {"bank_details": bank_details, "bene_id": bene_id})


def get_payout_bank_list(merchant_id):
    data = {"merchantid": merchant_id}
    response = requests.post(PaySprintRoutes.GET_LIST.value, json=data, headers=get_pay_sprint_headers())
    return response.json().get("data")
