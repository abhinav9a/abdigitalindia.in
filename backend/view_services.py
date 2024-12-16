from django.shortcuts import render, redirect
from core.models import UserAccount
# from .forms import OtherServicesForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import json
import requests
import base64
from decimal import Decimal, ROUND_DOWN
from backend.utils import (is_kyc_completed, generate_qr_code, is_user_onboard, generate_key, generate_unique_id,
                           get_client_ip, electricity_operator_id, recharge_prepaid_operator_id,
                           recharge_postpaid_operator_id, dth_operator_id, loan_operator_id, water_gas_lpg_operator_id)
from .models import (CommissionTxn, Wallet, WalletTransaction, Wallet2Transaction, ServiceActivation, DMTBankList, AepsTxnCallbackByEko,
                     PanVerificationTxn, BankVerificationTxn, DmtTxn, Commission, Payout, BbpsTxn, CreditCardTxn,
                     AdhaarVerificationTxn, OtherServices)
from django.http import JsonResponse, HttpResponse
from requests.exceptions import ConnectionError
from .context_processors import wallet_balance, wallet2_balance
import os
from datetime import datetime, timedelta
from django.utils import timezone
from urllib.parse import quote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
import hmac
import time
from backend.config.consts import PaySprintRoutes
from django.template.loader import get_template
from weasyprint import HTML

import jwt
import random
import logging


logger = logging.getLogger(__name__)


'''**********************
* ONBOARD USER API VIEW *
**********************'''
# ONBOARD USER (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def onboarding_user(request):
    onboardingDetails = UserAccount.objects.get(username=request.user)
    if request.method == 'POST':
        dob = request.POST.get('dob')
        line = request.POST.get('line')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')

        secret_key, secret_key_timestamp = generate_key()

        url = "https://api.eko.in/ekoicici/v1/user/onboard"

        payload = {"initiator_id": "9568855837", "pan_number": onboardingDetails.pancard_no.upper(), "mobile": onboardingDetails.mobile, "first_name": onboardingDetails.first_name, "last_name": onboardingDetails.last_name,
                   "email": onboardingDetails.email, "residence_address": json.dumps({"line": line, "city": city, "state": state, "pincode": pincode}), "dob": dob, "shop_name": onboardingDetails.shopName}

        headers = {"accept": "application/json", "developer_key": "552d8d5d982965b60f8fb4c618f95f4e", "secret-key": secret_key, "secret-key-timestamp": secret_key_timestamp, "content-type": "application/x-www-form-urlencoded"
                   }

        response = requests.put(url, data=payload, headers=headers)

        try:
            if response.status_code == 200:
                api_data = response.json()
                message = api_data.get('message')
                data = api_data.get('data', None)
                logger.error(f"EKO onboarding_user response ==> {json.dumps(data)}")
                if data is not None:
                    user_code = data['user_code']
                    onboardingDetails.eko_user_code = user_code
                    onboardingDetails.dob = dob
                    onboardingDetails.save()

                messages.success(request, message=message,
                                 extra_tags='success')
            else:
                api_data = response.json()
                logger.error(f"EKO onboarding_user ERROR response ==> {json.dumps(api_data)}")
                message = api_data.get('message')
                messages.success(request, message=message, extra_tags='danger')
        except Exception as e:
            print('Custom Exception from onboarding==>', e)
            messages.success(request, message=e, extra_tags='danger')
            return redirect('onboardingUser')
    return render(request, 'backend/Pages/onboardingUser.html', {'onboardingDetails': onboardingDetails, "dob": str(onboardingDetails.dob)})


'''****************
* QR PAYMENT VIEW *
****************'''
# 1. ACTIVATE (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def activate_qr_payment(request):
    try:
        ''' ACTIVATE QR PAYMENT SERVICE = 27 '''
        service_activation, created = ServiceActivation.objects.get_or_create(userAccount=request.user)
        user_code = UserAccount.objects.get(username=request.user).eko_user_code
        secret_key, secret_key_timestamp = generate_key()
        url = "https://api.eko.in/ekoicici/v1/user/service/activate"

        payload = {"service_code": "27", "user_code": user_code,"initiator_id": "9568855837"}
        headers = {"accept": "application/json", "content-type": "application/x-www-form-urlencoded", 'developer_key': '552d8d5d982965b60f8fb4c618f95f4e', 'secret-key': secret_key,'secret-key-timestamp': secret_key_timestamp}

        response = requests.put(url, data=payload, headers=headers)
        api_data = response.json()
        messages.success(request, message=api_data.get('message'), extra_tags='success')

        if created or not service_activation.QrPaymentService:
            # if response.message == 'This service already exist for the user code' or response.message == '':
            service_activation.QrPaymentService = True
            service_activation.save()
        
    except Exception as e:
        messages.error(request, message=f'custom error : {e}', extra_tags='danger')

    return redirect('recharge_wallet')

# 2. INITIATE QR PAYMENT (DONE, PENDING PAYMENT FETCH)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def recharge_wallet(request):
    service_activation = ServiceActivation.objects.get_or_create(userAccount=request.user)[0]
    if request.method == 'POST':
        '''QR Generation'''
        try:
            initiate_detail = UserAccount.objects.get(username=request.user)
            secret_key, secret_key_timestamp = generate_key()
            name = f'{initiate_detail.first_name} {initiate_detail.last_name}'
            email = initiate_detail.email
            sender = initiate_detail.mobile

            if not all([name, email, sender]):
                return JsonResponse({'success': False, 'message': 'All fields must be provided'})

            url = "https://api.eko.in/ekoicici/v1/customer/createcustomer"

            payload = {"initiator_id": "9568855837","name": name,"sender_id": sender,"email": email}

            headers = {'content-type': 'application/json','developer_key': '552d8d5d982965b60f8fb4c618f95f4e','secret_key': secret_key,'secret-key-timestamp': secret_key_timestamp}

            response = requests.post(url, json=payload, headers=headers)
            api_data = response.json()
            
            data = api_data.get('data', None)
            qr_string = data['qr_string']
            image_bytes = generate_qr_code(qr_string)
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            return JsonResponse({'success': True, 'message': 'QR Generated successfully', 'image_bytes': image_base64})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error Occurred!!!, {e}'})

    return render(request, 'backend/Pages/RechargeWallet.html', {'service_activation': service_activation})


# FETCH/REFRESH WALLET BALANCE (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def reload_wallet(request):
    try:
        balance = wallet_balance(request)
        return JsonResponse({'success': True ,'balance':balance})
    except:
        return JsonResponse({'success': False ,'message':'Error'})

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def reload_wallet2(request):
    try:
        balance = wallet2_balance(request)
        return JsonResponse({'success': True ,'balance':balance})
    except:
        return JsonResponse({'success': False ,'message':'Error'})


def import_banks_from_excel(request):
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']
        DMTBankList.create_from_excel(excel_file)
        messages.success(request, 'Imported successfully')
        return redirect('dashboard')
    return render(request, 'backend/Pages/importBank.html')


'''**********************
* VERIFICATION API VIEW *
**********************'''
# PANCARD VERIFICATION (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def pan_verification(request):
    if request.method == 'POST':
        charge = Decimal(3.26)
        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error Occurred!!! {e}'})
        
        # check the balance for service
        if wallet.balance >= charge:
            try:
                pan = request.POST.get('pan').upper()
                secret_key, secret_key_timestamp = generate_key()

                url = "https://api.eko.in/ekoicici/v1/pan/verify"

                payload = {"pan_number": pan, "purpose": "1", "initiator_id": "9568855837", "purpose_desc": "onboarding"}

                headers = {'Content-Type': 'application/x-www-form-urlencoded', 'developer_key': '552d8d5d982965b60f8fb4c618f95f4e', 'secret-key': secret_key, 'secret-key-timestamp': secret_key_timestamp}

                response = requests.request("POST", url, headers=headers, data=payload)
                response.raise_for_status()

                api_data = response.json()
                message = api_data.get('message')

                if message == "PAN verification successful":
                    data = api_data.get('data', None)
                    if data is not None:
                        context = {'pan_number': data['pan_number'],'title':data['title'],'first_name':data['first_name'],'last_name':data['last_name']}

                        # Charge user for Pan Verification service 3.26Rs
                        wallet.balance -= charge
                        wallet.save()

                        # Create a transaction entry for Pan Verification Service
                        PanVerificationTxn.objects.create(wallet=wallet, amount=charge, txn_status='Success', description='Pan Verification Service')
                        
                        return JsonResponse({'success': True, 'message': message, 'context': context})
                    else:
                        return JsonResponse({'success': True, 'message': 'Data not available.'})
                else:
                    return JsonResponse({'success': False, 'message': message})
            except ConnectionError:
                return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error Occurred!!! {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient Balance, Please Recharge Wallet.'})

    return render(request, 'backend/Services/Verification/PanVerification.html')

# BANK ACCOUNT VERIFICATION (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def bank_verification(request):
    if request.method == 'POST':
        charge = Decimal(6)
        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error Occurred!!! {e}'})
        
        # check the balance for service
        if wallet.balance >= charge:
            try:
                user_code = UserAccount.objects.get(username=request.user).eko_user_code
                secret_key, secret_key_timestamp = generate_key()

                accountNumber = request.POST.get('accountNumber')
                ifsc = request.POST.get('ifsc')
                client_ref_id = generate_unique_id()

                url = f"https://api.eko.in/ekoicici/v1/banks/ifsc:{ifsc}/accounts/{accountNumber}"

                payload = {
                    "initiator_id": "9568855837",
                    "customer_id": 9568855837,
                    "client_ref_id": client_ref_id,  # unique id from our end. max 20 char
                    "user_code": user_code
                }

                headers = {'developer_key': '552d8d5d982965b60f8fb4c618f95f4e','secret-key': secret_key,'secret-key-timestamp': secret_key_timestamp,'Content-Type': 'application/x-www-form-urlencoded'}

                response = requests.request("POST", url, headers=headers, data=payload)
                response.raise_for_status()

                api_data = response.json()
                message = api_data.get('message')

                if message == "Success!  Account details found..":
                    data = api_data.get('data', None)
                    if data is not None:
                        context = {'bank': data['bank'],'recipient_name': data['recipient_name'],'ifsc': data['ifsc'],'account': data['account']}

                        transaction_id = data['tid']
                        # Charge user for Bank Verification service 6Rs
                        wallet.balance -= charge
                        wallet.save()

                        # Create a transaction entry for wallet
                        BankVerificationTxn.objects.create(
                            wallet=wallet, 
                            txnId=transaction_id,
                            client_ref_id=client_ref_id,
                            amount=charge,
                            txn_status='Success',
                            description='Bank Verification Service')
                        
                        return JsonResponse({'success': True, 'message': message, 'context': context})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            except ConnectionError:
                return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error Occurred!!! {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient Balance, Please Recharge Wallet.'})

    return render(request, 'backend/Services/Verification/BankVerification.html')


'''
Adhaar Verification
'''
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def adhaar_consent(request):
    if request.method == 'POST':  
        try:
            secret_key, secret_key_timestamp = generate_key()

            user_code = UserAccount.objects.get(username=request.user).eko_user_code
            adhaar = request.POST.get('adhaar')
            ip = get_client_ip(request)

            url = f"https://api.eko.in/ekoicici/v2/external/getAdhaarConsent?source=NEWCONNECT&initiator_id=9568855837&is_consent=Y&consent_text={adhaar}&user_code={user_code}&realsourceip={ip}"

            payload = {}
            headers = {'developer_key': '552d8d5d982965b60f8fb4c618f95f4e', 'secret-key': secret_key, 'secret-key-timestamp': secret_key_timestamp}

            response = requests.request("GET", url, headers=headers, data=payload)

            api_data = response.json()
            print('api_data==>', api_data)
            
            message = api_data.get('message')

            if message == "Karza Aadhaar Consent Signed":
                data_response = api_data.get('data', None)
                if data_response is not None:
                    access_key = data_response.get('access_key', None)

                    url = f"https://api.eko.in/ekoicici/v2/external/getAdhaarOTP?source=NEWCONNECT&initiator_id=9568855837&aadhar={adhaar}&is_consent=Y&access_key={access_key}&caseId={adhaar}&user_code={user_code}&realsourceip={ip}"

                    payload = {}
                    headers = {
                        'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
                        'secret-key': secret_key,
                        'secret-key-timestamp': secret_key_timestamp
                    }

                    response1 = requests.request("GET", url, headers=headers, data=payload)
                    api_data1 = response1.json()
                    print('api_data1==>', api_data1)
                    message1 = api_data1.get('message')
                    if message1 == "Karza Aadhaar Otp Sent":
                        data_response1 = api_data1.get('data', None)
                        if data_response1 is not None:
                            return JsonResponse({'success': True, 'message': message1, 'context': data_response1})
                        else:
                            return JsonResponse({'success': False, 'message': 'Data not available.'})
                    else:
                        return JsonResponse({'success': False, 'message': message1})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            else:
                return JsonResponse({'success': False, 'message': message})
        except ConnectionError:
            return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})

    return render(request, 'backend/Services/Verification/AdhaarVerification.html')

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def adhaar_verification(request):
    if request.method == 'POST':
        charge = Decimal(5)
        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error Occurred!!! {e}'})

        if wallet.balance >= charge:
            try:
                secret_key, secret_key_timestamp = generate_key()
                user_code = UserAccount.objects.get(username=request.user).eko_user_code
                ip = get_client_ip(request)

                otp = request.POST.get('otp')
                adhaar = request.POST.get('adhaarVerify')
                access_key = request.POST.get('accessKeyVerify')

                url = f"https://api.eko.in/ekoicici/v1/external/getAdhaarFile?initiator_id=9568855837&otp={otp}&is_consent=Y&share_code=1111&access_key={access_key}&caseId={adhaar}&aadhar={adhaar}&user_code={user_code}&realsourceip={ip}"

                payload = {}
                headers = {
                    'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
                    'secret-key': secret_key,
                    'secret-key-timestamp': secret_key_timestamp
                }

                response = requests.request("GET", url, headers=headers, data=payload)
                api_data = response.json()
                print('api_data==>', api_data)
                
                message = api_data.get('message')

                if message == "Aadhaar File Downloaded":
                    data_response = api_data.get('data', None)
                    if data_response is not None:

                        # Charge user for Bank Verification service 6Rs
                        wallet.balance -= charge
                        wallet.save()

                        # Create a transaction entry for wallet
                        AdhaarVerificationTxn.objects.create(wallet=wallet, amount=charge, txn_status='Success', description='Adhaar Verification Service')

                        return JsonResponse({'success': True, 'message': message, 'context': data_response})
                    else:
                        return JsonResponse({'success': False, 'message': 'Data not available.'})
                else:
                    return JsonResponse({'success': False, 'message': message})
            except ConnectionError:
                return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient Balance, Please Recharge Wallet.'})

    return render(request, 'backend/Services/Verification/AdhaarVerification.html')


'''**************************
* USER SERVICE INQUIRY VIEW *
**************************'''
# ACTIVATED SERVICE INQUIRY (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def get_services(request):
    if request.method == 'POST':
        secret_key, secret_key_timestamp = generate_key()

        # Get list of services
        url = "https://api.eko.in/ekoicici/v1/user/services"

        querystring = {"initiator_id":"9568855837"}

        headers = {
            "developer_key": "552d8d5d982965b60f8fb4c618f95f4e",
            "secret_key": secret_key,
            "secret-key-timestamp": secret_key_timestamp,
            'cache-control': "no-cache",
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 200:
            try:
                api_data = response.json()
            except ValueError:
                api_data = {'error': 'Something went wrong!!!'}

            return JsonResponse({'success': True, 'message': 'Request saved successfully', 'api_data':api_data}, status=response.status_code)
        else:
            return JsonResponse({'success': False,'message': 'API request failed'}, status=response.status_code)

    return render(request, 'backend/Pages/getServices.html')


# USER ACTIVATED SERVICE INQUIRY (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def get_user_services(request):
    if request.method == 'POST':
        secret_key, secret_key_timestamp = generate_key()
        user_code = UserAccount.objects.get(username=request.user).eko_user_code

        if user_code is not None:
            # Get list of services
            url = f"https://api.eko.in/ekoicici/v1/user/services/user_code:{user_code}"

            querystring = {"initiator_id":"9568855837"}

            headers = {
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded",
                "developer_key": "552d8d5d982965b60f8fb4c618f95f4e",
                "secret-key": secret_key,
                "secret-key-timestamp": secret_key_timestamp
            }

            response = requests.get(url, headers=headers, params=querystring)

            if response.status_code == 200:
                try:
                    api_data = response.json()
                except ValueError:
                    api_data = {'error': 'Something went wrong!!!'}

                return JsonResponse({'success': True, 'message': 'Request saved successfully', 'api_data':api_data}, status=response.status_code)
            else:
                return JsonResponse({'success': False,'message': 'API request failed'}, status=response.status_code)
        else:
            return JsonResponse({'success': False,'message': 'User code not found, Get onboard...'})

    return render(request, 'backend/Pages/userServicesInquiry.html')


'''************
*  AEPS VIEW  *
************'''

# activate aeps service for code = 43
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def activate_aeps(request):
    try:
        ''' ACTIVATE AEPS SERVICE = 43 '''

        secret_key, secret_key_timestamp = generate_key()
        user_code = UserAccount.objects.get(username=request.user).eko_user_code
        service_activation, created = ServiceActivation.objects.get_or_create(userAccount=request.user)

        modelname=request.POST.get('modelname')
        devicenumber=request.POST.get('devicenumber')
        line=request.POST.get('line')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')

        appline=request.POST.get('appline')
        appcity=request.POST.get('appcity')
        appstate=request.POST.get('appstate')
        apppincode=request.POST.get('apppincode')

        pan_card = request.FILES['pan_card']
        aadhar_front = request.FILES['aadhar_front']
        aadhar_back = request.FILES['aadhar_back']

        # url = "https://api.eko.in/ekoicici/v1/user/service/activate"
        url = "https://api.eko.in:25002/ekoicici/v1/user/service/activate"

        address=json.dumps({"line": line, "city": city, "state": state, "pincode": pincode})
        appaddress=json.dumps({"line": appline, "city": appcity, "state": appstate, "pincode": apppincode})

        payload = {"form-data": f"user_code={user_code}&initiator_id=9568855837&service_code=43&modelname={modelname}&devicenumber={devicenumber}&office_address={address}&address_as_per_proof={appaddress}"}

        files = [(('pan_card'),pan_card), (('aadhar_front'),aadhar_front), (('aadhar_back'),aadhar_back)]
        
        headers = {"accept": "application/json","developer_key": "552d8d5d982965b60f8fb4c618f95f4e","secret-key": secret_key,"secret-key-timestamp": secret_key_timestamp}

        response = requests.put(url, data=payload, headers=headers, files=files)
        logger.error(f"==> AEPS Response: {response.text}")
        api_data = response.json()
        message = api_data.get('message')
        messages.success(request, message=message, extra_tags='success')

        print('==>Aeps here',response.text)
        logger.error(f"==> AEPS Payload: {payload}")
        logger.error(f"==> AEPS Response API DATA: {api_data}")
        if created or not service_activation.AepsService:
            if message == 'This service already exist for the user code' or message == 'AePS Registration Successful':
                service_activation.AepsService = True
                service_activation.save()
    except Exception as e:
        messages.error(request, message=f'custom error : {e}', extra_tags='danger')

    return redirect('aeps')

# render aeps template with configuration
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def aeps(request):
    service_activation = ServiceActivation.objects.get_or_create(userAccount=request.user)[0]
    return render(request, 'backend/Services/AEPS/AEPS.html', {'service_activation': service_activation})

# aeps configuration
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def get_config_info(request):
    secret_key, secret_key_timestamp = generate_key()
    user_code = UserAccount.objects.get(username=request.user).eko_user_code
    return JsonResponse({
        'initiator_id': "9568855837",
        'user_code': user_code,
        'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",
        'secret_key':secret_key,
        'secret_key_timestamp':secret_key_timestamp
    })


'''************
*  DMT VIEW  *
************'''

'''
IF CUSTOMER EXIST THEN,
1. get the customer profile (if exist) and available fund limit
2. get all recipients (if exist)
3. add recipient (if not exist)
4. make payment
5. make refund (if payment failed)
'''
# get customer information (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def get_dmt_customer_info(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code
            customer_mobile = request.POST.get('customer_mobile')

            url = f"https://api.eko.in/ekoicici/v2/customers/mobile_number:{customer_mobile}?initiator_id=9568855837&user_code={user_code}"

            headers = {
            'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",
            'secret-key': secret_key,
            'secret-key-timestamp': secret_key_timestamp,
            'content-type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("GET", url, headers=headers)
            api_data = response.json()
            message = api_data.get('message')
            print(response.text)

            if message == "Non-KYC active":
                data = api_data.get('data', None)
                if data is not None:
                    return JsonResponse({'success': True, 'message': message, 'context': data})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            else:
                return JsonResponse({'success': False, 'message': message})
        except ConnectionError:
            return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})

    return render(request, 'backend/Services/DMT/CustomerInfo.html')


# get the recipient of the customer (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def list_dmt_recipient(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code
            customer_mobile = request.POST.get('customer_mobile')

            url = f"https://api.eko.in/ekoicici/v2/customers/mobile_number:{customer_mobile}/recipients?initiator_id=9568855837&user_code={user_code}"

            payload = {}
            headers = {
                'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",
                'secret-key': secret_key,
                'secret-key-timestamp': secret_key_timestamp,
                'content-type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            api_data = response.json()
            message = api_data.get('message')

            if message == "Success":
                data = api_data.get('data', None)
                if data is not None:
                    context = {'recipient_list':data['recipient_list']}
                    return JsonResponse({'success': True, 'message': message, 'context': context})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            else:
                return JsonResponse({'success': False, 'message': message})
        except ConnectionError:
            return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})

    return render(request, 'backend/Services/DMT/DMT.html')


# add the recipient of the customer (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def create_dmt_recipient(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code

            customer_mobile = request.POST.get('customer_mobile')
            account = request.POST.get('account')
            ifsc = request.POST.get('ifsc')

            recipient_name = request.POST.get('recipient_name')
            recipient_mobile = request.POST.get('recipient_mobile')
            bank_id = request.POST.get('bank_id')

            if not customer_mobile or not account or not ifsc or not recipient_name or not recipient_mobile or not bank_id:
                messages.success(request, message="All Fields are required", extra_tags='danger')
                return redirect('create_dmt_recipient')
            
            acc_ifsc = f"{account}_{ifsc}"

            url = f"https://api.eko.in/ekoicici/v2/customers/mobile_number:{customer_mobile}/recipients/acc_ifsc:{acc_ifsc}"

            payload = f'recipient_type=3&initiator_id=9568855837&bank_id={bank_id}&recipient_name={recipient_name}&recipient_mobile={recipient_mobile}&user_code={user_code}'

            headers = {
                'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
                'secret-key': secret_key,
                'secret-key-timestamp': secret_key_timestamp,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)
            api_data = response.json()
            print(api_data)
            messages.success(request, message=api_data.get('message'), extra_tags='success')

        except Exception as e:
            messages.success(request, message=f"Internal server error: {e}", extra_tags='danger')
    
    bank_list = DMTBankList.objects.all().order_by('-id')
    return render(request, 'backend/Services/DMT/CreateRecipient.html', {'bank_list': bank_list})


# intiate the payment (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def initiate_dmt_payment(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid amount'})
        
        dmt_charge = amount + (Decimal(0.01) * amount)
        dmt_charge = dmt_charge.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})
        
        # check the balance for service
        if wallet.balance >= dmt_charge:
            try:
                secret_key, secret_key_timestamp = generate_key()
                user_code = UserAccount.objects.get(username=request.user).eko_user_code
                customer_mobile = request.POST.get('customer_id')
                recipient_id = request.POST.get('recipient_id')
                currency = request.POST.get('currency')
                amount = request.POST.get('amount')
                channel = request.POST.get('channel')
                latlong = quote(request.POST.get('latlong'))
                timestamp = quote(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                client_ref_id = generate_unique_id()

                # Perform manual validation
                if not latlong:
                    return JsonResponse({'success': True, 'message': 'Enable your location for this service'})

                if not customer_mobile or not recipient_id or not amount or not currency or not channel:
                    return JsonResponse({'success': True, 'message': 'All fields are required'})

                try:
                    amount = Decimal(amount)
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Invalid amount'})

                url = "https://api.eko.in/ekoicici/v2/transactions"

                payload = f'initiator_id=9568855837&customer_id={customer_mobile}&recipient_id={recipient_id}&amount={amount}&currency={currency}&timestamp={timestamp}&client_ref_id={client_ref_id}&state=1&channel={channel}&latlong={latlong}&user_code={user_code}'
                
                headers = {'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",'secret-key': secret_key,'secret-key-timestamp': secret_key_timestamp,'content-type': 'application/x-www-form-urlencoded'}

                response = requests.request("POST", url, headers=headers, data=payload)
                api_data = response.json()

                print('from DMT==> ',response.text)

                message = api_data.get('message')
                data = api_data.get('data', None)

                if data is not None:
                    txstatus_desc = data.get("txstatus_desc", 'N/A')
                    sender_name = data.get("sender_name", 'N/A')
                    transaction_id = data.get('tid','N/A')
                    bank = data.get("bank", 'N/A')
                    currency = data.get("currency", 'N/A')
                    bank_ref_num = data.get("bank_ref_num", 'N/A')
                    recipient_id = data.get("recipient_id", 'N/A')
                    channel_desc = data.get("channel_desc", 'N/A')
                    recipient_name = data.get('recipient_name', 'N/A')
                    customer_id = data.get('customer_id', 'N/A')
                    account = data.get('account', 'N/A')

                    if "Transaction successful" in message:
                        # Charge user for DMT
                        wallet.balance -= dmt_charge
                        wallet.save()

                        # Commission transaction
                        c_obj = Commission.objects.get_or_create(userAccount=request.user)[0]
                        commission_amount = (dmt_charge - amount) * (c_obj.DmtCommission / 100)

                        # add commission amount into wallet
                        wallet.balance += commission_amount
                        wallet.save()

                        # Create a transaction entry for wallet
                        DmtTxn.objects.create(
                            wallet=wallet,
                            txn_status=txstatus_desc,
                            sender_name=sender_name,
                            txnId=transaction_id,
                            bank=bank,
                            currency=currency,
                            bank_ref_num=bank_ref_num,
                            recipient_id=recipient_id,
                            channel_desc=channel_desc,
                            recipient_name=recipient_name,
                            customer_id=customer_id,
                            account=account,
                            commission=commission_amount,
                            client_ref_id=client_ref_id,
                            amount=dmt_charge,
                            description='DMT Transaction'
                            )

                        return JsonResponse({'success': True, 'message': txstatus_desc, 'context': data})
                    else:
                        DmtTxn.objects.create(wallet=wallet, txnId=transaction_id, recipient_name=recipient_name, client_ref_id=client_ref_id,amount=dmt_charge,txn_status=txstatus_desc,description='DMT Transaction')
                        return JsonResponse({'success': True, 'message': message, 'context': data})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            except ConnectionError:
                return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient Balance, Please Recharge Wallet.'})

    return render(request, 'backend/Services/DMT/DMT.html')


# Initiate a refund if txn fails
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def initiate_dmt_refund(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code

            txn_id = request.POST.get('txn_id')
            otp = request.POST.get('otp')

            if not txn_id or not otp:
                messages.success(request, message="All Fields are required", extra_tags='danger')
                return redirect('initiate_dmt_refund')
            
            url = f"https://api.eko.in/ekoicici/v2/transactions/{txn_id}/refund"

            payload = f'initiator_id=9568855837&otp={otp}&state=1&user_code={user_code}'

            headers = {'developer_key': '552d8d5d982965b60f8fb4c618f95f4e','secret-key': secret_key,'secret-key-timestamp': secret_key_timestamp,'Content-Type': 'application/x-www-form-urlencoded'}

            response = requests.request("POST", url, headers=headers, data=payload)
            api_data = response.json()
            message = api_data.get('message')
            print("from dmt refund==> ",response.text)
            if message == 'Refund done':
                data = api_data.get('data', None)
                if data is not None:
                    tid = data['tid']
                    refund_tid = data['refund_tid']
                    
                    txn_obj = DmtTxn.objects.get(txnId=tid)
                    txn_obj.txn_status = 'Refunded'
                    txn_obj.description = f'Refunded with TID {refund_tid}'
                    txn_obj.save()
            messages.success(request, message=message, extra_tags='success')

        except Exception as e:
            messages.success(request, message=f"Internal server error: {e}", extra_tags='danger')
    
    return render(request, 'backend/Services/DMT/Refund.html')


# Resend refund OTP if txn fails
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def resend_dmt_refund_otp(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code

            resend_txn_id = request.POST.get('resend_txn_id')

            if not resend_txn_id:
                messages.success(request, message="All Fields are required", extra_tags='danger')
                return redirect('initiate_dmt_refund')

            url = f"https://api.eko.in/ekoicici/v2/transactions/{resend_txn_id}/refund/otp"

            payload = f'initiator_id=9568855837&user_code={user_code}'

            headers = {'developer_key': '552d8d5d982965b60f8fb4c618f95f4e','secret-key': secret_key,'secret-key-timestamp': secret_key_timestamp,'Content-Type': 'application/x-www-form-urlencoded'}

            response = requests.request("POST", url, headers=headers, data=payload)
            api_data = response.json()
            message = api_data.get('message')

            print(response.text)

            messages.success(request, message=message, extra_tags='success')
        except Exception as e:
            messages.success(request, message=f"Internal server error: {e}", extra_tags='danger')
    
    return render(request, 'backend/Services/DMT/Refund.html')


'''
IF CUSTOMER NOT EXIST THEN,
1. create customer profile
2. verify with otp
'''
# create customer (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def create_dmt_customer(request):
    if request.method == 'POST':  
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code
            customer_mobile = request.POST.get('customer_mobile')
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            line=request.POST.get('line')
            city=request.POST.get('city')
            state=request.POST.get('state')
            pincode=request.POST.get('pincode')

            if not customer_mobile or not name or not dob or not line or not city or not state or not pincode:
                return JsonResponse({'success': True, 'message': 'All fields are required'})
            
            address=json.dumps({"line": line, "city": city, "state": state, "pincode": pincode})

            url = f"https://api.eko.in/ekoicici/v2/customers/mobile_number:{customer_mobile}"

            payload = f'initiator_id=9568855837&name={name}&user_code={user_code}&dob={dob}&residence_address={address}'

            headers = {
                'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",
                'secret-key': secret_key,
                'secret-key-timestamp': secret_key_timestamp,
                'content-type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)
            api_data = response.json()
            message = api_data.get('message')

            if message == "Wallet opened successfully.":
                data = api_data.get('data', None)
                if data is not None:
                    return JsonResponse({'success': True, 'message': message, 'context': data})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            elif message == 'OTP sent. Proceed with verification.':
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'message': message})
        except ConnectionError:
            return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})

    return render(request, 'backend/Services/DMT/CreateCustomer.html')


# verify customer with otp (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def verify_dmt_otp(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code
            customer_id = request.POST.get('customer_id')
            otp = request.POST.get('otp')

            url = f"https://api.eko.in/ekoicici/v2/customers/verification/otp:{otp}"

            payload = f'customer_id_type=mobile_number&customer_id={customer_id}&initiator_id=9568855837&user_code={user_code}'

            headers = {
                'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",
                'secret-key': secret_key,
                'secret-key-timestamp': secret_key_timestamp,
                'content-type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)
            api_data = response.json()
            message = api_data.get('message')
            print(response.text)

            if message == "Wallet opened successfully.":
                data = api_data.get('data', None)
                if data is not None:
                    return JsonResponse({'success': True, 'message': message, 'context': data})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            else:
                return JsonResponse({'success': False, 'message': message})
        except ConnectionError:
            return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})

    return render(request, 'backend/Services/DMT/CreateCustomer.html')


'''
PAYOUT / FUND TRANSFER
'''
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def add_bank(request):
    userObj = UserAccount.objects.get(username=request.user)
    if request.method == 'POST':
        mode = request.POST.get('mode')
        acc_type = request.POST.get('acc_type')
        recipient_name = request.POST.get('recipient_name')
        account = request.POST.get('account')
        ifsc = request.POST.get('ifsc')

        userObj.acc_name = recipient_name
        userObj.acc_no = account
        userObj.ifsc = ifsc.upper()
        userObj.acc_type = acc_type
        userObj.payment_mode = mode

        userObj.save()
        messages.success(request, message='Bank Added Successfully', extra_tags='success')

    return render(request, 'backend/Services/Payout/AddBankAcc.html', {'userObj': userObj})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def transfer_fund(request):
    userObj = UserAccount.objects.get(username=request.user)
    if request.method == 'POST':
        secret_key, secret_key_timestamp = generate_key()

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
                client_ref_id = generate_unique_id()

                url = "https://api.eko.in/ekoicici/v1/agent/user_code:34702001/settlement"

                payload = f'initiator_id=9568855837&amount={amount}&payment_mode={userObj.payment_mode}&client_ref_id={client_ref_id}&recipient_name={userObj.acc_name}&ifsc={userObj.ifsc}&account={userObj.acc_no}&service_code=45&sender_name=ABDIGITALINDIAPVTLTD&tag=CASHOUT&beneficiary_account_type={userObj.acc_type}'

                headers = {
                    'developer_key': "552d8d5d982965b60f8fb4c618f95f4e",
                    'secret-key': secret_key,
                    'secret-key-timestamp': secret_key_timestamp,
                    'content-type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                api_data = response.json()
                message = api_data.get('message')

                print('from PayOut==>',response.text)

                if "Transaction processed successfully" in message or 'Transaction initiated successfully' in message:
                    data = api_data.get('data')
                    transaction_id = data['tid']
                    client_ref_id = data['client_ref_id']
                    ifsc = data['ifsc']
                    account = data['account']
                    txn_status = data['txstatus_desc']

                    # Charge user for DMT
                    wallet.balance -= payout_charge
                    wallet.save()

                    # Create a transaction entry for wallet
                    Payout.objects.create(userAccount = request.user, amount=payout_charge, txn_status=txn_status, tid=transaction_id, client_ref_id=client_ref_id,recipient_name=userObj.acc_name, ifsc=ifsc, account=account)

                    messages.success(request, message)
                    return redirect('transfer_fund')
                else:
                    messages.error(request, message)
                    return redirect('transfer_fund')
            except Exception as e:
                messages.error(request, f'Internal server error: {e}')
                return redirect('transfer_fund')
        else:
            messages.error(request, 'Insufficient Balance, Please Recharge Wallet.')
            return redirect('transfer_fund')

    return render(request, 'backend/Services/Payout/Payout.html', {'userObj': userObj})


'''
BBPS
'''
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bbps(request):
    return render(request, 'backend/Services/BBPS/BBPS.html')

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bbps_operator(request, id):
    secret_key, secret_key_timestamp = generate_key()
    url = f"https://api.eko.in/ekoicici/v2/billpayments/operators?category={id}"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
        'secret-key': secret_key,
        'secret-key-timestamp': secret_key_timestamp
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    api_data = response.json()
    # print(api_data)
    opdata = []
    for key, value in api_data.items():
        for i in value:
            opdata.append(i['operator_id'])
    
    print("====>",opdata)

    return render(request, 'backend/Services/BBPS/BBPS_Operator.html', {'api_data': api_data})


# Recharge
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bbps_recharge(request, id):
    secret_key, secret_key_timestamp = generate_key()
    url = f"https://api.eko.in/ekoicici/v2/billpayments/operators?category={id}"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
        'secret-key': secret_key,
        'secret-key-timestamp': secret_key_timestamp
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    api_data = response.json()

    return render(request, 'backend/Services/BBPS/BBPS_Recharge.html', {'api_data': api_data})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def get_bbps_recharge_param(request):
    secret_key, secret_key_timestamp = generate_key()

    operator_id = request.GET.get('operator_id')
    url = f"https://api.eko.in/ekoicici/v2/billpayments/operators/{operator_id}"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
        'secret-key': secret_key,
        'secret-key-timestamp': secret_key_timestamp
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    api_data = response.json()
    return JsonResponse({'context': api_data})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def get_bbps_operator_param(request):
    try:
        secret_key, secret_key_timestamp = generate_key()

        operator_id = request.GET.get('operator_id')
        url = f"https://api.eko.in/ekoicici/v2/billpayments/operators/{operator_id}"
        payload = {}
        headers = {'Content-Type': 'application/json','developer_key': '552d8d5d982965b60f8fb4c618f95f4e','secret-key': secret_key,'secret-key-timestamp': secret_key_timestamp}
        response = requests.request("GET", url, headers=headers, data=payload)
        api_data = response.json()
    except:
        messages.error(request, message="Service Not Available.")
        return redirect('bbps')
    return render(request, 'backend/Services/BBPS/BBPS_Operator_Params.html', {'api_data': api_data})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bbps_fetch_bill(request):
    try:
        secret_key, secret_key_timestamp = generate_key()

        utility_acc_no = request.GET.get('utility_acc_no')
        confirmation_mobile_no = request.GET.get('confirmation_mobile_no')
        operator_id = request.GET.get('operator_id')
        latlong = request.GET.get('latlong')
        amount = request.GET.get('amount', 100)
        hcc = request.GET.get('hcc', None)

        if not utility_acc_no or not operator_id or not amount or not latlong:
            return JsonResponse({'success': False, 'message': 'All fields are required'})

        url = "https://api.eko.in/ekoicici/v2/billpayments/fetchbill?initiator_id=9568855837"

        payload = json.dumps({
            "source_ip": get_client_ip(request),
            "user_code": "34702001",
            "client_ref_id": generate_unique_id(),
            "utility_acc_no": utility_acc_no,
            "confirmation_mobile_no": confirmation_mobile_no,
            "amount": amount,
            "operator_id": operator_id,
            "latlong": latlong,
            "hc_channel": 1 if hcc is not None else 0
        })

        print(payload)

        headers = {
            'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
            'secret-key-timestamp': secret_key_timestamp,
            'secret-key': secret_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        api_data = response.json()
        print(response.text)

        reason = api_data.get('invalid_params', {}).get('reason', '')

        message = api_data.get('message')
        if message == 'Due Bill Amount For utility':
            return JsonResponse({'success': True, 'context': api_data})
        else:
            return JsonResponse({'success': False, 'message': f"{reason} | {message}"})
    except ConnectionError:
        return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bbps_paybill(request):
    try:
        utility_acc_no = request.GET.get('utility_acc_no')
        confirmation_mobile_no = request.GET.get('confirmation_mobile_no', utility_acc_no)
        operator_id = request.GET.get('operator_id')
        latlong = request.GET.get('latlong')
        amount = request.GET.get('amount')
        hcc = request.GET.get('hcc', None)

        if not utility_acc_no or not operator_id or not amount or not latlong or not confirmation_mobile_no:
            return JsonResponse({'success': False, 'message': 'All fields are required'})

        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})

        # check the balance for service
        if wallet.balance >= Decimal(amount):
            try:
                url = "https://api.eko.in:25002/ekoicici/v2/billpayments/paybill?initiator_id=9568855837"

                payload = json.dumps({"source_ip": get_client_ip(request),"user_code": "34702001","amount": amount,"client_ref_id": generate_unique_id(),"utility_acc_no": utility_acc_no,"confirmation_mobile_no": confirmation_mobile_no,"sender_name": f'{request.user.first_name} {request.user.last_name}',"operator_id": operator_id,"latlong": latlong,"hc_channel": 1 if hcc is not None else 0})

                print("Pay bill payload ===>", payload)

                ## Generating secret-key, timestamp & hash
                key = 'd3d8a58d-d437-46bf-bbeb-f7a601a437f8'
                encoded_key = base64.b64encode(key.encode()).decode()
                timestamp = round(time.time() * 1000)
                secret_key_timestamp = str(timestamp)
                secret_key = base64.b64encode(hmac.new(encoded_key.encode(), secret_key_timestamp.encode(), hashlib.sha256).digest()).decode()
                user_code = '34702001'
                concatenated_string = secret_key_timestamp + utility_acc_no + amount + user_code
                request_hash = base64.b64encode(hmac.new(encoded_key.encode(), concatenated_string.encode(), hashlib.sha256).digest()).decode()

                headers = {'developer_key': '552d8d5d982965b60f8fb4c618f95f4e', 'secret-key-timestamp': secret_key_timestamp, 'secret-key': secret_key, 'request_hash': request_hash,'Content-Type': 'application/json', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.9.0'}

                response = requests.request("POST", url, headers=headers, data=payload)
                print('Pay bill response ==>',response.text)
                api_data = response.json()
                message = api_data.get('message')

                if 'Success' in message:
                    data = api_data.get('data')
                    amount = data.get("amount", 'N/A')

                    # Charge user for DMT
                    wallet.balance -= Decimal(amount)
                    wallet.save()

                    # Create a transaction entry for wallet
                    BbpsTxn.objects.create(userAccount = request.user, txstatus_desc = data.get("txstatus_desc", 'N/A'), utilitycustomername = data.get("utilitycustomername", 'N/A'), tid = data.get("tid", 'N/A'), sender_id = data.get("sender_id", 'N/A'), recipient_id = data.get("recipient_id", 'N/A'), amount = data.get("amount", 'N/A'), customermobilenumber = data.get("customermobilenumber", 'N/A'), operator_name = data.get("operator_name", 'N/A'), totalamount = data.get("totalamount", 'N/A'), approvalreferencenumber =  data.get("approvalreferencenumber", 'N/A'), account = data.get("account", 'N/A'))

                    '''
                    Commission Distribution, hcc=0, fixed commission
                    '''
                    commission = Commission.objects.get_or_create(userAccount=request.user)[0]
                    amount = Decimal(amount)
                    if hcc is None:

                        if int(operator_id) in electricity_operator_id:
                            
                            ElectricityCommission = commission.BbpsInstantElectricity

                            if ElectricityCommission != 0:
                                # Self Commission
                                wallet.balance += Decimal(ElectricityCommission)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=ElectricityCommission, txn_status="Success", desc="BBPS Electricity Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)
                            
                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsInstantElectricityDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsInstantElectricityMaster
                            else:
                                manager1_commission = Decimal(0.0)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsInstantElectricityDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsInstantElectricityMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity Commission", agent_name=request.user.username)

                        elif int(operator_id) in recharge_prepaid_operator_id:

                            RechargePrepaidCommission = commission.BbpsInstantRechargePrepaid

                            if RechargePrepaidCommission != 0:
                                # Self Commission
                                wallet.balance += Decimal(RechargePrepaidCommission)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=RechargePrepaidCommission, txn_status="Success", desc="BBPS Recharge Prepaid Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)
                            
                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsInstantRechargePrepaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsInstantRechargePrepaidMaster
                            else:
                                manager1_commission = Decimal(0.0)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsInstantRechargePrepaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsInstantRechargePrepaidMaster
                            else:
                                manager2_commission = Decimal(0.0)
                            
                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Recharge Prepaid Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Recharge Prepaid Commission", agent_name=request.user.username)
                        
                        elif int(operator_id) in recharge_postpaid_operator_id:

                            RechargePostpaidCommission = commission.BbpsInstantRechargePostpaid

                            if RechargePostpaidCommission != 0:
                                # Self Commission
                                wallet.balance += Decimal(RechargePostpaidCommission)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=RechargePostpaidCommission, txn_status="Success", desc="BBPS Recharge Postpaid Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)
                            
                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsInstantRechargePostpaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsInstantRechargePostpaidMaster
                            else:
                                manager1_commission = Decimal(0.0)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsInstantRechargePostpaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsInstantRechargePostpaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Recharge Postpaid Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager1.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Recharge Postpaid Commission", agent_name=request.user.username)

                        elif int(operator_id) in dth_operator_id:

                            DTHCommission = commission.BbpsInstantDTH

                            if DTHCommission != 0:
                                # Self Commission
                                wallet.balance += Decimal(DTHCommission)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=DTHCommission, txn_status="Success", desc="BBPS DTH Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)
                            
                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsInstantDTHDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsInstantDTHMaster
                            else:
                                manager1_commission = Decimal(0.0)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsInstantDTHDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsInstantDTHMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS DTH Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager1.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS DTH Commission", agent_name=request.user.username)
                        
                        elif int(operator_id) in loan_operator_id:

                            LoanCommission = commission.BbpsInstantLoan

                            if LoanCommission != 0:
                                # Self Commission
                                wallet.balance += Decimal(LoanCommission)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=LoanCommission, txn_status="Success", desc="BBPS Loan Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)
                            
                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsInstantLoanDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsInstantLoanMaster
                            else:
                                manager1_commission = Decimal(0.0)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsInstantLoanDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsInstantLoanMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Loan Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager1.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Loan Commission", agent_name=request.user.username)

                    else:
                        # In Percentage (%)
                        if int(operator_id) in electricity_operator_id:

                            if amount >= 0 and amount <= 1000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab1

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor1
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster1
                                else:
                                    manager1_commission = Decimal(0.0)
                                
                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor1
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster1
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                            elif amount >= 1001 and amount <= 2000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab2

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor2
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster2
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor2
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster2
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                            elif amount >= 2001 and amount <= 10000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab3

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor3
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster3
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor3
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster3
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)
                            
                            elif amount >= 10001 and amount <= 15000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab4

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor4
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster4
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor4
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster4
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                            elif amount >= 15001 and amount <= 25000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab5

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor5
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster5
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor5
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster5
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                            elif amount >= 25001 and amount <= 100000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab6

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor6
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster6
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor6
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster6
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                            elif amount >= 100001 and amount <= 200000:
                                ElectricityCommission = commission.BbpsHCElectricitySlab7

                                if ElectricityCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(ElectricityCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Electricity High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabDistributor7
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCElectricitySlabMaster7
                                else:
                                    manager1_commission = Decimal(0.0)
                                
                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabDistributor7
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCElectricitySlabMaster7
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Electricity High Commission", agent_name=request.user.username)

                        # In Percentage (%)
                        elif int(operator_id) in water_gas_lpg_operator_id:
                            
                            if amount >= 0 and amount <= 1000:
                                WaterNGasCommission = commission.BbpsHCWaterNGasSlab1

                                if WaterNGasCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(WaterNGasCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabDistributor1
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabMaster1
                                else:
                                    manager1_commission = Decimal(0.0)
                                
                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabDistributor1
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabMaster1
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                            elif amount >= 1001 and amount <= 10000:
                                WaterNGasCommission = commission.BbpsHCWaterNGasSlab2

                                if WaterNGasCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(WaterNGasCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabDistributor2
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabMaster2
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabDistributor2
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabMaster2
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)
                           
                            elif amount >= 10001 and amount <= 15000:
                                WaterNGasCommission = commission.BbpsHCWaterNGasSlab3

                                if WaterNGasCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(WaterNGasCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabDistributor3
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabMaster3
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabDistributor3
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabMaster3
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                            elif amount >= 15001 and amount <= 25000:
                                WaterNGasCommission = commission.BbpsHCWaterNGasSlab4

                                if WaterNGasCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(WaterNGasCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabDistributor4
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabMaster4
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabDistributor4
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabMaster4
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                            elif amount >= 25001 and amount <= 100000:
                                WaterNGasCommission = commission.BbpsHCWaterNGasSlab5

                                if WaterNGasCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(WaterNGasCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabDistributor5
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabMaster5
                                else:
                                    manager1_commission = Decimal(0.0)

                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabDistributor5
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabMaster5
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                            elif amount >= 100001 and amount <= 200000:
                                WaterNGasCommission = commission.BbpsHCWaterNGasSlab6

                                if WaterNGasCommission != 0:
                                    # Self Commission
                                    commission_amount = amount * (Decimal(WaterNGasCommission) / 100)
                                    wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                    wallet.save()
                                    CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name="Self")

                                # extract manager1 | D/M/A
                                manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                                # extract manager2 | M/A
                                manager2 = UserAccount.objects.get(id=manager1.userManager)

                                # Getting manager1 commission slabs
                                if manager1.userType == 'Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabDistributor6
                                elif manager1.userType == 'Master Distributor':
                                    manager1_commission = commission.BbpsHCWaterNGasSlabMaster6
                                else:
                                    manager1_commission = Decimal(0.0)
                                
                                manager1_commission = amount * (Decimal(manager1_commission) / 100)
                                manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # Getting manager2 commission slabs
                                if manager2.userType == 'Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabDistributor6
                                elif manager2.userType == 'Master Distributor':
                                    manager2_commission = commission.BbpsHCWaterNGasSlabMaster6
                                else:
                                    manager2_commission = Decimal(0.0)

                                manager2_commission = amount * (Decimal(manager2_commission) / 100)
                                manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                                # manager1 credit
                                if manager1.userType != "Admin" and manager1_commission != 0:
                                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                    manager1_wallet.balance += manager1_commission
                                    manager1_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                                # manager2 credit
                                if manager2.userType != "Admin" and manager2_commission != 0:
                                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                    manager2_wallet.balance += manager2_commission
                                    manager2_wallet.save()
                                    CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Water & Gas High Commission", agent_name=request.user.username)

                        # In Percentage (%)
                        elif int(operator_id) in recharge_postpaid_operator_id:
                            MobilePostpaidCommission = commission.BbpsHCMobilePostpaid

                            if MobilePostpaidCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(MobilePostpaidCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Mobile Postpaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCMobilePostpaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCMobilePostpaidMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCMobilePostpaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCMobilePostpaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Mobile Postpaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Mobile Postpaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) AIRTEL Mobile Prepaid Recharge
                        elif int(operator_id) == 1:
                            AirtelPrepaidCommission = commission.BbpsHCAirtelMobilePrepaid

                            if AirtelPrepaidCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(AirtelPrepaidCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Airtel Mobile Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCAirtelMobilePrepaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCAirtelMobilePrepaidMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCAirtelMobilePrepaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCAirtelMobilePrepaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Airtel Mobile Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Airtel Mobile Prepaid High Commission", agent_name=request.user.username)
                            
                        # In Percentage (%) BSNL Mobile Prepaid Recharge
                        elif int(operator_id) == 5:
                            BSNLPrepaidCommission = commission.BbpsHCBSNLMobilePrepaid

                            if BSNLPrepaidCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(BSNLPrepaidCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS BSNL Mobile Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCBSNLMobilePrepaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCBSNLMobilePrepaidMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCBSNLMobilePrepaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCBSNLMobilePrepaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS BSNL Mobile Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS BSNL Mobile Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) JIO Mobile Prepaid Recharge
                        elif int(operator_id) == 90:
                            JioPrepaidCommission = commission.BbpsHCJioMobilePrepaid

                            if JioPrepaidCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(JioPrepaidCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS JIO Mobile Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCJioMobilePrepaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCJioMobilePrepaidMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCJioMobilePrepaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCJioMobilePrepaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS JIO Mobile Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS JIO Mobile Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) VI Mobile Prepaid Recharge
                        elif int(operator_id) == 400:
                            ViPrepaidCommission = commission.BbpsHCVIMobilePrepaid

                            if ViPrepaidCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(ViPrepaidCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS VI Mobile Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCVIMobilePrepaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCVIMobilePrepaidMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCVIMobilePrepaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCVIMobilePrepaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS VI Mobile Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS VI Mobile Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) MTNL Delhi & MTNL Mumbai Mobile Prepaid Recharge
                        elif int(operator_id) in [91, 508]:
                            MTNLPrepaidCommission = commission.BbpsHCMTNLMobilePrepaid

                            if MTNLPrepaidCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(MTNLPrepaidCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS MTNL Mobile Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCMTNLMobilePrepaidDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCMTNLMobilePrepaidMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCMTNLMobilePrepaidDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCMTNLMobilePrepaidMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS MTNL Mobile Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS MTNL Mobile Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) Dish TV DTH Prepaid Recharge
                        elif int(operator_id) == 16:
                            DishTVCommission = commission.BbpsHCDTHDishTv

                            if DishTVCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(DishTVCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Dish TV DTH Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCDTHDishTvDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCDTHDishTvMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCDTHDishTvDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCDTHDishTvMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Dish TV DTH Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Dish TV DTH Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) TataSky DTH Prepaid Recharge
                        elif int(operator_id) == 20:
                            TataSkyCommission = commission.BbpsHCDTHTataSky

                            if TataSkyCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(TataSkyCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS TataSky DTH Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCDTHTataSkyDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCDTHTataSkyMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCDTHTataSkyDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCDTHTataSkyMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS TataSky DTH Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS TataSky DTH Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) Airtel DTH Prepaid Recharge
                        elif int(operator_id) == 21:
                            AirtelDTVCommission = commission.BbpsHCDTHAirtelDTv

                            if AirtelDTVCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(AirtelDTVCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Airtel TV DTH Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCDTHAirtelDTvDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCDTHAirtelDTvMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCDTHAirtelDTvDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCDTHAirtelDTvMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Airtel TV DTH Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Airtel TV DTH Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) Videocon D2H DTH Prepaid Recharge
                        elif int(operator_id) == 95:
                            VideoconCommission = commission.BbpsHCDTHVideoconTv

                            if VideoconCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(VideoconCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Videocon TV DTH Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCDTHVideoconTvDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCDTHVideoconTvMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCDTHVideoconTvDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCDTHVideoconTvMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Videocon TV DTH Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Videocon TV DTH Prepaid High Commission", agent_name=request.user.username)

                        # In Percentage (%) Sun TV DTH Prepaid Recharge
                        elif int(operator_id) == 17:
                            BigTVCommission = commission.BbpsHCDTHBigTv

                            if BigTVCommission != 0:
                                # Self Commission
                                commission_amount = amount * (Decimal(BigTVCommission) / 100)
                                wallet.balance += commission_amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                                wallet.save()
                                CommissionTxn.objects.create(userAccount=request.user, amount=commission_amount, txn_status="Success", desc="BBPS Big TV DTH Prepaid High Commission", agent_name="Self")

                            # extract manager1 | D/M/A
                            manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                            # extract manager2 | M/A
                            manager2 = UserAccount.objects.get(id=manager1.userManager)

                            # Getting manager1 commission slabs
                            if manager1.userType == 'Distributor':
                                manager1_commission = commission.BbpsHCDTHBigTvDistributor
                            elif manager1.userType == 'Master Distributor':
                                manager1_commission = commission.BbpsHCDTHBigTvMaster
                            else:
                                manager1_commission = Decimal(0.0)
                            
                            manager1_commission = amount * (Decimal(manager1_commission) / 100)
                            manager1_commission = manager1_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # Getting manager2 commission slabs
                            if manager2.userType == 'Distributor':
                                manager2_commission = commission.BbpsHCDTHBigTvDistributor
                            elif manager2.userType == 'Master Distributor':
                                manager2_commission = commission.BbpsHCDTHBigTvMaster
                            else:
                                manager2_commission = Decimal(0.0)

                            manager2_commission = amount * (Decimal(manager2_commission) / 100)
                            manager2_commission = manager2_commission.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

                            # manager1 credit
                            if manager1.userType != "Admin" and manager1_commission != 0:
                                manager1_wallet = Wallet.objects.get(userAccount=manager1)
                                manager1_wallet.balance += manager1_commission
                                manager1_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="BBPS Big TV DTH Prepaid High Commission", agent_name=request.user.username)

                            # manager2 credit
                            if manager2.userType != "Admin" and manager2_commission != 0:
                                manager2_wallet = Wallet.objects.get(userAccount=manager2)
                                manager2_wallet.balance += manager2_commission
                                manager2_wallet.save()
                                CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="BBPS Big TV DTH Prepaid High Commission", agent_name=request.user.username)

                    return JsonResponse({'success': True, 'context': api_data})
                else:
                    return JsonResponse({'success': False, 'message': message})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient Balance, Please Recharge Wallet.'})
    except ConnectionError:
        return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})


'''
PANCARD UTI
'''
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def pancard_uti(request):

    url = "https://sit.paysprint.in/service-api/api/v1/service/pan/generateurl"

    payload = json.dumps({
        "merchantcid": request.user.platform_id,
        "refid": random.randint(1, 1000000000),
        "redirect_url": ""
    })

    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJQU1BSSU5UIiwicGFydG5lcklkIjoiUFMwMDE2NjYiLCJ0aW1lc3RhbXAiOjE3MDkxMTk2NDAzNDEsInJlcWlkIjo3MTk5MDA5MzF9.dk4NgW8jLJb9iZWT6aG7UthTs70z6DpzFD6smJ4KOj0"

    headers = {
        'Authorisedkey': 'NjA5NjY4OWI3YWJmNTlhODczODQ3MmE2MzU5YWI1MDc=',
        'Content-Type': 'application/json',
        'Token': token,
        'accept': 'application/json',
        'Cookie': 'ci_session=f4d4bbpdoaldaajlsc9vjkuc5bn6hjcs'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    api_data = response.json()
    print(response.text)

    return render(request, 'backend/Services/UTI/UTI.html', {'api_data': api_data})


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def pancard_nsdl(request):

    url = "https://sit.paysprint.in/service-api/api/v1/service/pan/V2/generateurl"

    payload = json.dumps({
        "kyctype": "K",
        "refid": random.randint(1, 1000000000),
        "title": 1,
        "firstname": "Jatin",
        "lastname": "Gautam",
        "email": "trendingindiana@gmail.com",
        "mode": "P",
        "gender": "M",
        "redirect_url": "http://127.0.0.1:8000/user/",
        "merchant_code": "R124"
    })
    headers = {
        'Authorisedkey': 'MzNkYzllOGJmZGVhNWRkZTc1YTgzM2Y5ZDFlY2EyZTQ=',
        'Content-Type': 'application/json',
        'Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJQQVlTUFJJTlQiLCJ0aW1lc3RhbXAiOjE2MTAwMjYzMzgsInBhcnRuZXJJZCI6IlBTMDAxIiwicHJvZHVjdCI6IldBTExFVCIsInJlcWlkIjoxNjEwMDI2MzM4fQ.buzD40O8X_41RmJ0PCYbBYx3IBlsmNb9iVmrVH9Ix64',
        'accept': 'application/json',
        'Cookie': 'ci_session=vp983lqfjupkkkdprffigh21ad6pc7he'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    api_data = response.json()
    print(response.text)

    return render(request, 'backend/Services/NSDL/NSDL.html', {'api_data': api_data})


'''
VPA
'''
# @login_required(login_url='user_login')
# @user_passes_test(is_kyc_completed, login_url='unauthorized')
# @user_passes_test(is_user_onboard, login_url='onboardingUser')
# def vpa_verification(request):
#     api_data = None
#     if request.method == 'POST':
#         try:
#             secret_key, secret_key_timestamp = generate_key()

#             customer_vpa = request.GET.get('customer_vpa')
#             mobile_number = request.GET.get('mobile_number')

#             url = f"https://api.eko.in/ekoicici/v2/customers/mobile_number:{mobile_number}/vpa-verification/{mobile_number}"

#             payload = f'initiator_id=9568855837&user_code=34702004&customer_vpa={customer_vpa}&client_ref_id=RIM10011909045679291'
#             headers = {
#             'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
#             'secret-key': secret_key,
#             'secret-key-timestamp': secret_key_timestamp,
#             'Content-Type': 'application/x-www-form-urlencoded'
#             }

#             response = requests.request("POST", url, headers=headers, data=payload)
#             api_data = response.json()

#             print(response.text)

#         except:
#             messages.error(request, message="Something weng wrong, Try later.")
#             return redirect('vpa_verification')
        
#     return render(request, 'backend/Services/VPA/VPA.html', {'api_data': api_data})


'''
CREDIT CARD BILL
'''
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def credit_card_bill(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid amount'})
        
        credit_card_charge = amount + (Decimal(0.0) * amount)
        credit_card_charge = credit_card_charge.quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        # Getting user's wallet
        try:
            wallet = Wallet.objects.get(userAccount=request.user)
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})
        
        # check the balance for service
        if wallet.balance >= credit_card_charge:
            try:
                secret_key, secret_key_timestamp = generate_key()

                recipient_id = request.POST.get('recipient_id')
                customer_mobile = request.POST.get('customer_id')
                amount = request.POST.get('amount')

                client_ref_id = generate_unique_id()

                # Perform manual validation
                if not customer_mobile or not recipient_id or not amount:
                    return JsonResponse({'success': True, 'message': 'All fields are required'})

                # try:
                #     amount = Decimal(amount)
                # except ValueError:
                #     return JsonResponse({'success': False, 'message': 'Invalid amount'})

                url = "https://api.eko.in/ekoicici/v2/creditcard/payments"

                payload = json.dumps({"recipient_id": recipient_id,"initiator_id": "9568855837","amount": amount,"client_ref_id": client_ref_id,"customer_id": customer_mobile,"channel": "2"})

                headers = {
                    'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
                    'secret-key': secret_key,
                    'secret-key-timestamp': secret_key_timestamp,
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                api_data = response.json()

                print('from Credit Card==> ', response.text)

                message = api_data.get('message')
                data = api_data.get('data', None)

                if data is not None:
                    txstatus_desc = data.get("txstatus_desc", 'N/A')
                    sender_name = data.get("sender_name", 'N/A')
                    transaction_id = data.get('tid','N/A')
                    recipient_name = data.get('recipient_name', 'N/A')
                    ifsc = data.get('ifsc', 'N/A')
                    bank_ref_num = data.get("bank_ref_num", 'N/A')
                    account = data.get('account', 'N/A')


                    if "Transaction processed successfully" in message:
                        # Charge user for DMT
                        wallet.balance -= credit_card_charge
                        wallet.save()

                        # Commission transaction
                        # c_obj = Commission.objects.get_or_create(userAccount=request.user)[0]
                        # commission_amount = (credit_card_charge - amount) * (c_obj.DmtCommission / 100)

                        # add commission amount into wallet
                        # wallet.balance += commission_amount
                        # wallet.save()

                        # Create a transaction entry for wallet
                        CreditCardTxn.objects.create(
                            wallet=wallet,
                            txn_status=txstatus_desc,
                            sender_name=sender_name,
                            txnId=transaction_id,
                            ifsc=ifsc,
                            bank_ref_num=bank_ref_num,
                            recipient_name=recipient_name,
                            account=account,
                            client_ref_id=client_ref_id,
                            amount=credit_card_charge,
                            description='Credit Card Transaction'
                            )

                        return JsonResponse({'success': True, 'message': txstatus_desc, 'context': data})
                    else:
                        CreditCardTxn.objects.create(wallet=wallet, txnId=transaction_id, recipient_name=recipient_name, client_ref_id=client_ref_id,amount=credit_card_charge,txn_status=txstatus_desc,description='Credit Card Transaction')
                        return JsonResponse({'success': True, 'message': message, 'context': data})
                else:
                    return JsonResponse({'success': False, 'message': 'Data not available.'})
            except ConnectionError:
                return JsonResponse({'success': False, 'message': 'No internet connection. Please check your network.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Internal server error: {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient Balance, Please Recharge Wallet.'})

    return render(request, 'backend/Services/CreditCard/CreditCard.html')


# add the recipient of the customer (DONE)
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def create_credit_card_recipient(request):
    if request.method == 'POST':
        try:
            secret_key, secret_key_timestamp = generate_key()
            user_code = UserAccount.objects.get(username=request.user).eko_user_code

            customer_mobile = request.POST.get('customer_mobile')
            account = request.POST.get('account')
            recipient_name = request.POST.get('recipient_name')
            recipient_mobile = request.POST.get('recipient_mobile')

            bank_code = request.POST.get('bank_code')
            bank_details = bank_code.split("_")
            bank_id = bank_details[0].strip()

            if not customer_mobile or not account or not bank_details[1].strip() or not recipient_name or not recipient_mobile or not bank_id:
                messages.success(request, message="All Fields are required", extra_tags='danger')
                return redirect('create_credit_card_recipient')
            
            acc_bank_code = f"{account}_{bank_details[1].strip()}"

            url = f"https://api.eko.in/ekoicici/v2/customers/mobile_number:{customer_mobile}/recipients/acc_bankcode:{acc_bank_code}"

            payload = f'recipient_type=3&initiator_id=9568855837&bank_id={bank_id}&recipient_name={recipient_name}&recipient_mobile={recipient_mobile}&user_code={user_code}'

            headers = {
                'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
                'secret-key': secret_key,
                'secret-key-timestamp': secret_key_timestamp,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)
            api_data = response.json()
            print(api_data)
            messages.success(request, message=api_data.get('message'), extra_tags='success')

        except Exception as e:
            messages.success(request, message=f"Internal server error: {e}", extra_tags='danger')
    
    bank_list = DMTBankList.objects.all().order_by('-id')
    return render(request, 'backend/Services/CreditCard/CreateRecipient.html', {'bank_list': bank_list})


# LATER
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def otherServices(request, service):
    if request.method == 'POST':
        userAccount = request.user
        name = request.POST.get('fullName')
        gender = request.POST.get('gender')
        father_name = request.POST.get('father_name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        adhaar = request.POST.get('adhaar')
        pan = request.POST.get('pan')
        serviceName = service
        serviceDescription = request.POST.get('serviceDescription')

        doc1 = request.FILES.get('doc1', None)
        doc2 = request.FILES.get('doc2', None)
        doc3 = request.FILES.get('doc3', None)
        doc4 = request.FILES.get('doc4', None)

        OtherServices.objects.create(userAccount=userAccount, name=name, doc1=doc1, doc2=doc2, doc3=doc3, doc4=doc4, gender=gender, father_name=father_name, dob=dob, address=address, mobile=mobile, email=email,adhaar=adhaar, pan=pan,serviceName=serviceName,serviceDescription=serviceDescription)

        messages.success(request, "Request received, We'll contact you soon.")
        return redirect('dashboard')

    return render(request, 'backend/Services/Other/otherServices.html', {'service': service})


# LATER
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def festivalSeasonDhamaka(request):
    return render(request, 'backend/Pages/festivalSeasonDhamaka.html')


'''**********************
*  SERVICE REPORT VIEW  *
**********************'''

# aeps report
@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def aeps_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = AepsTxnCallbackByEko.objects.filter(userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = AepsTxnCallbackByEko.objects.filter(userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/AEPS/AEPS_Report.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def wallet_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = WalletTransaction.objects.filter(wallet__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = WalletTransaction.objects.filter(wallet__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Wallet/Wallet_Report.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def wallet2_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = Wallet2Transaction.objects.filter(wallet2__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = Wallet2Transaction.objects.filter(wallet2__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Wallet/Wallet_Report.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def pan_verification_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = PanVerificationTxn.objects.filter(wallet__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = PanVerificationTxn.objects.filter(wallet__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Verification/Pan_Report.html', context)

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def adhaar_verification_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = AdhaarVerificationTxn.objects.filter(wallet__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = AdhaarVerificationTxn.objects.filter(wallet__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Verification/Adhaar_Report.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bank_verification_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = BankVerificationTxn.objects.filter(wallet__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = BankVerificationTxn.objects.filter(wallet__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Verification/Bank_Report.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def dmt_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = DmtTxn.objects.filter(wallet__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = DmtTxn.objects.filter(wallet__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/DMT/DMT_Report.html', context)

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def credit_card_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = CreditCardTxn.objects.filter(wallet__userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = CreditCardTxn.objects.filter(wallet__userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/CreditCard/CredirCard_Report.html', context)


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def payout_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = Payout.objects.filter(userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = Payout.objects.filter(userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Payout/Payout_Report.html', context)

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def bbps_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = BbpsTxn.objects.filter(userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = BbpsTxn.objects.filter(userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/BBPS/BBPS_Report.html', context)

@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_onboard, login_url='onboardingUser')
def commission_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = CommissionTxn.objects.filter(userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = CommissionTxn.objects.filter(userAccount=request.user).order_by('-id')

    except ValueError as e:
        messages.error(request, str(e))
        transactions = []

    paginator = Paginator(transactions, 50)

    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    context = {'transactions_page': transactions_page}
    return render(request, 'backend/Services/Commission/Commission_Report.html', context)


@login_required(login_url='user_login')
def generate_slip(request, src, id):
    if src == 'dmt':
        transactions = DmtTxn.objects.get(id=id)
    elif src == 'pan':
        transactions = PanVerificationTxn.objects.get(id=id)
    elif src == 'bank':
        transactions = BankVerificationTxn.objects.get(id=id)
    elif src == 'bbps':
        transactions = BbpsTxn.objects.get(id=id)


    # # Render HTML template with dynamic data
    # template = get_template("backend/Pages/template.html")
    # html_content = template.render({
    #     "transactions": transactions
    # })

    # # Create PDF response
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="transaction_slip.pdf"'

    # # Generate PDF using WeasyPrint
    # HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf(response)

    # return response
    return render(request, 'backend/Pages/template.html', {'transactions':transactions})

# RIZING Pay
# {"initiator_id": "8979754644",
# "developer_key": "2a99ba339a6420c39c1442a3e367b090",
# "secret_key": "jMMwtNyfD6byT96Pkocj5e799kTminSEGPa/uArzTKo=",
# "secret_key_timestamp": "1707210545149",
# "user_code": "33178058",
# "language": "en",
# "environment": "production"}