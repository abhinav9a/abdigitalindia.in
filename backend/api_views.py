# myapp/views.py
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from urllib.parse import urlencode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import QRTxnCallbackByEkoSerializer, AepsTxnCallbackByEkoSerializer, CMSTxnCallbackByEkoSerializer
from core.models import UserAccount
from .models import (AepsTxnCallbackByEko, Wallet, Commission, CommissionTxn, CMSTxnCallbackByEko, 
                     Wallet2, PaySprintCommissionCharge, Wallet2Transaction)
from .utils import generate_key
import hashlib
import hmac
import base64
from decimal import Decimal, ROUND_DOWN

import logging


logger = logging.getLogger(__name__)


# @api_view(['POST'])
# def debit_receiver_hook(request):
#     formatted_data = {
#         "txn_detail": request.data
#     }
#     serializer = QRTxnCallbackByEkoSerializer(data=formatted_data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'success': True, 'message': 'Data saved successfully'}, status=200)
#     return Response({'success': False, 'errors': serializer.errors})

@api_view(['POST'])
def debit_receiver_hook(request):
    formatted_data = {
        "txn_detail": request.data
    }

    tid = request.data['tid']

    serializer = QRTxnCallbackByEkoSerializer(data=formatted_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"ekoTxnId": tid, "proceed": 1}, status=200)
    return Response({'success': False, 'errors': serializer.errors})

@api_view(['POST'])
def aeps_txn_callback(request):
    action = request.data['action']
    print('DATA==> ',request.data, '<==END')
    formatted_data = None

    detail= request.data['detail']
    data = detail.get('data')
    if action == 'debit-hook':
        service_type = data.get('type', None)
        if service_type is not None:
            try:
                userAccount = UserAccount.objects.get(username=request.data['platform_user']).id
            except Exception as e:
                return Response({'success': True, 'message': f'Error getting user details ==> {e}'}, status=200)

            formatted_data = {
                "userAccount": userAccount,
                "tx_status": 'P',
                "client_ref_id": detail['client_ref_id'],
                "service_type": service_type,
                "txn_detail": request.data
            }

            key = "d3d8a58d-d437-46bf-bbeb-f7a601a437f8"
            
            secret_key, secret_key_timestamp = generate_key()
            data_signature = ''
            if service_type == '2':
                # request signature = secret_key_timestamp + customer_id + amount + user_code
                formatted_data['amount'] = detail['data']['amount']
                data_signature = secret_key_timestamp + detail['data']['customer_id'] + formatted_data['amount'] + detail['data']['user_code']
            if service_type == '3':
                # request signature = secret_key_timestamp + customer_id + user_code
                data_signature = secret_key_timestamp + detail['data']['customer_id'] + detail['data']['user_code']
            if service_type == '4':
                # request signature = secret_key_timestamp + customer_id + user_code
                data_signature = secret_key_timestamp + detail['data']['customer_id'] + detail['data']['user_code']

            # Encode the key using base64
            encoded_key = base64.b64encode(key.encode()).decode()

            # HMAC the concatenated string and encoded key using HMAC-SHA256
            try:
                signature_req_hash = hmac.new(encoded_key.encode(), data_signature.encode(), hashlib.sha256).digest()
            except Exception as e:
                return Response({'success': True, 'message': f'Error Creating request hash ==> {e}'}, status=200)
                
            # Encode the result using base64
            request_hash = base64.b64encode(signature_req_hash).decode()
            if UserAccount.objects.get(id=userAccount).is_active:
                response = {"action": "go","allow": True,"secret_key_timestamp": secret_key_timestamp,"request_hash": request_hash,"secret_key": secret_key}
            else:
                response = {"action": "go","allow": False,"message": "You're not allowed to make payment. Your account is inactive."}
        else:
            return Response({"action": "go","allow": True}, status=200)
    elif action == 'eko-response':
        try:
            detail= request.data['detail']
            client_ref_id= detail['client_ref_id']
            txn_obj = AepsTxnCallbackByEko.objects.filter(client_ref_id=client_ref_id).first()
            if txn_obj is not None:
                status = detail['response']['message']

                try:
                    tid = detail['response']['data']['tid']
                except:
                    tid = 'N/A'

                if txn_obj.service_type == "2":
                    try:
                        aadhar = detail['response']['data']['aadhar']
                    except:
                        aadhar = 'N/A'
                else:
                    aadhar = 'N/A'

                if status == "Transaction Successful":
                    txn_obj.tx_status = '0'

                    # Get user's wallet
                    wallet = Wallet.objects.get(userAccount=txn_obj.userAccount)

                    commission = Commission.objects.get_or_create(userAccount=txn_obj.userAccount)[0]

                    # current user | D/M/R/A

                    # extract manager1 | D/M/A
                    manager1 = UserAccount.objects.get(id=wallet.userAccount.userManager)

                    # extract manager2 | M/A
                    manager2 = UserAccount.objects.get(id=manager1.userManager)

                    if txn_obj.amount >= 8000:
                        txn_obj.commission = commission.AepsCommissionSlab8
                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor8
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster8
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor8
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster8
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 3000 and txn_obj.amount <= 7999:
                        txn_obj.commission = commission.AepsCommissionSlab7
                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor7
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster7
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor7
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster7
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 2500 and txn_obj.amount <= 2999:
                        txn_obj.commission = commission.AepsCommissionSlab6
                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor6
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster6
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor6
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster6
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 2000 and txn_obj.amount <= 2499:
                        txn_obj.commission = commission.AepsCommissionSlab5
                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor5
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster5
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor5
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster5
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 1500 and txn_obj.amount <= 1999:
                        txn_obj.commission = commission.AepsCommissionSlab4
                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor4
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster4
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor4
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster4
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 1000 and txn_obj.amount <= 1499:
                        txn_obj.commission = commission.AepsCommissionSlab3

                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor3
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster3
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor3
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster3
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 200 and txn_obj.amount <= 999:
                        txn_obj.commission = commission.AepsCommissionSlab2
                        
                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor2
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster2
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor2
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster2
                        else:
                            manager2_commission = Decimal(0.0)
                    elif txn_obj.amount >= 100 and txn_obj.amount <= 199:
                        txn_obj.commission = commission.AepsCommissionSlab1

                        # Getting manager1 commission slabs
                        if manager1.userType == 'Distributor':
                            manager1_commission = commission.AepsCommissionSlabDistributor1
                        elif manager1.userType == 'Master Distributor':
                            manager1_commission = commission.AepsCommissionSlabMaster1
                        else:
                            manager1_commission = Decimal(0.0)

                        # Getting manager2 commission slabs
                        if manager2.userType == 'Distributor':
                            manager2_commission = commission.AepsCommissionSlabDistributor1
                        elif manager2.userType == 'Master Distributor':
                            manager2_commission = commission.AepsCommissionSlabMaster1
                        else:
                            manager2_commission = Decimal(0.0)
                    else:
                        txn_obj.commission = Decimal(0.0)
                        manager1_commission = Decimal(0.0)
                        manager2_commission = Decimal(0.0)

                    # current user credit
                    wallet.balance += (txn_obj.amount + txn_obj.commission)
                    wallet.save()

                    # manager1 credit
                    manager1_wallet = Wallet.objects.get(userAccount=manager1)
                    manager1_wallet.balance += manager1_commission
                    manager1_wallet.save()
                    if manager1.userType != "Admin":
                        CommissionTxn.objects.create(userAccount=manager1, amount=manager1_commission, txn_status="Success", desc="AePS Commission", agent_name=txn_obj.userAccount.username)

                    # manager2 credit
                    manager2_wallet = Wallet.objects.get(userAccount=manager2)
                    manager2_wallet.balance += manager2_commission
                    manager2_wallet.save()
                    if manager2.userType != "Admin":
                        CommissionTxn.objects.create(userAccount=manager2, amount=manager2_commission, txn_status="Success", desc="AePS Commission", agent_name=txn_obj.userAccount.username)

                elif status=="Transaction Fail" or status=="Transaction Pending":
                    txn_obj.tx_status = '1'
                else:
                    txn_obj.tx_status = "other"

                txn_obj.txn_detail = request.data
                txn_obj.tid = tid
                txn_obj.aadhar_no = aadhar
                txn_obj.save()
                
                return Response({"message": "Received."}, status=200)
            else:
                return Response({"message": "Entry not in use."}, status=200)
        except Exception as e:
            return Response({"message": f"Transaction Failed due to internal server error ==> {e}"}, status=200)
    else:
        try:
            detail= request.data['detail']
            client_ref_id= detail['client_ref_id']
            txn_obj = AepsTxnCallbackByEko.objects.filter(client_ref_id=client_ref_id).first()

            txn_obj.tx_status = '1'
            txn_obj.aadhar_no = 'N/A'
            txn_obj.txn_detail = request.data
            txn_obj.save()
            return Response({"message": "Details saved with txn_status fail."}, status=200)
        except Exception as e:
            return Response({"message": f"Transaction Failed due to internal server error ==> {e}"}, status=200)    

    serializer = AepsTxnCallbackByEkoSerializer(data=formatted_data)
    if serializer.is_valid():
        serializer.save()
        return Response(response, status=200)
    return Response({'success': False, 'errors': serializer.errors})




# @api_view(['POST', 'OPTIONS', 'CAPTURE'])
# @permission_classes([AllowAny])
# def eko_txn_callback(request):
#     print('===>',request.data)

#     headers = {
#         'Access-Control-Allow-Origin': '*',
#         'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
#         'Access-Control-Allow-Headers': 'X-Requested-With'
#     }

#     formatted_data = {
#         "txn_detail": request.data
#     }
#     # serializer = CMSTxnCallbackByEkoSerializer(data=formatted_data)
#     # if serializer.is_valid():
#     #     serializer.save()
#     return HttpResponse('''<PidData>
# 	<Data type=\\\"X\\\">MjAyMS0xMi0wNlQwNjo0ODoyM51MswAVy/PSZSqgXRudRMXTP356NsUJ4q4qItIZDjYZfOD4zwDpqlKT4aU927NvMJm6+IxgTTZEFngZ0TY+ibqUeQQiB7JEwj+8xeeO+7Y+G4yJmL7FjqNfQG7O/AgMP8AXWFS522iUeGmqkyf7InpXIj7VCiKlNDu+QNu+donxOQ6hRlNJ5J0kc082Fct4hvEr4iFVL9UrAx1+kR8yDbLAISxc+37RI7cxn577uNsazb/jy7O+tTk9zE6Ia3uPY0uqKfMNqNhSTomHMeJo5S0wuOW7uyRYrvz8Q4hUlCuqsup0ZmKA5su1F7HU60q6DHkO0eH+mk8Q/gA8ymaEHeBadkd+i/8tTZnxDyp/gw+z3vT+MPZNLKT4WAE5w2nhOoOOS+F9NPpJ2mn+FqwkRQ7VnEv09g0/bTyAZHCvmhUAy/NHYVYEPaycRpoSIzGuA3REoX++HaOetubgBx9vVVIl5ZKAR4hlwzuGJbcFlyJh6uxjQIK1bJh/jPJH/m+WyJpZwc99IArg9hnBkUFTO42ZeaHXj7+4BNDahs6vFtoquJGFXHYkZUZ866itGA6Dh8iJCjIjd8f6IEah1U+SKX0mkAzh4IM91lw6sIeNpykMwk99FTDJ33vkW+ao1mf/LK8yWV3hisEGqQtCAhn3S71lpf/pJk4TOVLIJKwqnlcsin6mWcLr3Ve8xkWvJW8dRVfZ+KbQTpdOU4oQs3iv4jl0ORbuJJhVC2IEOGpUfpQyS8OO0x8D7RTvl+L3FmtKIXNZ7qlfkYdxKnH3a0QSvFY8KFpxOhUKcQXqIWU/Yuhtldgjb6D2Ys2QvgR99kRhDF7449fbqkQnnNF8uIGX3MIailsw/JFcTiko22s6in6gzPuv7AoPl1XIfDURnvQQnxlGb3MArO2rD48SVmNpwYGBnGTTyV1OYl9EbrJ1NPVcoXFCt6tcDDXwnhB09iJK7PWmKuIe5wP8dGWK/kgdYuEYRmsso+niYg2zUwdt41JGFPVJR0eCwNCOcmQ2uocPGmukB3h0h6dR1mMCTYBPUyNIxQznMxGAj72N0yHXwCS5FR6Qih8sYTDA/x1OOnuANK/m7CuCJ6H+tv48PU6vubtQAfxKCXQMiUZp0qbc</Data>
# 	<DeviceInfo dc=\\\"79bfab62-5fd1-4ea1-bf5c-00cc714ae571\\\" dpId=\\\"MANTRA.MSIPL\\\" mc=\\\"MIIEGjCCAwKgAwIBAgIGAX0iDKcNMA0GCSqGSIb3DQEBCwUAMIHqMSowKAYDVQQDEyFEUyBNYW50cmEgU29mdGVjaCBJbmRpYSBQdnQgTHRkIDcxQzBBBgNVBDMTOkIgMjAzIFNoYXBhdGggSGV4YSBvcHBvc2l0ZSBHdWphcmF0IEhpZ2ggQ291cnQgUyBHIEhpZ2h3YXkxEjAQBgNVBAkTCUFobWVkYWJhZDEQMA4GA1UECBMHR3VqYXJhdDEdMBsGA1UECxMUVGVjaG5pY2FsIERlcGFydG1lbnQxJTAjBgNVBAoTHE1hbnRyYSBTb2Z0ZWNoIEluZGlhIFB2dCBMdGQxCzAJBgNVBAYTAklOMB4XDTIxMTEyNTEyMjEzNVoXDTIxMTIxNTA1MjMxMlowgbAxJTAjBgNVBAMTHE1hbnRyYSBTb2Z0ZWNoIEluZGlhIFB2dCBMdGQxHjAcBgNVBAsTFUJpb21ldHJpYyBNYW51ZmFjdHVyZTEOMAwGA1UEChMFTVNJUEwxEjAQBgNVBAcTCUFITUVEQUJBRDEQMA4GA1UECBMHR1VKQVJBVDELMAkGA1UEBhMCSU4xJDAiBgkqhkiG9w0BCQEWFXN1cHBvcnRAbWFudHJhdGVjLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALwP8kOTVlcHl1sOaXo3e1DLJJMRdrfrVOsAsgkrZQNnppVB8c9hY0OPP9ncWNl7SMobrrA6k2lSI0RDd1/4vd11ZUlic/IaHkNJQ6XJHE+Cwl8r2zVlAIO/cyibm7oPZRuf6TFzwrxltxuRL9J81lT/bm53injV8Six7Zg0pYqoJ1kwXqxF3ql+T3SCDp9zUfohwC60X3lFnqxOLgrIH430exaSsRl1UjnaDbU71ihme1yXDeVkKaQNIlTXbj1RJNXeHJpJMEpDyld54oHTmvSIsZip/QmT8rzUHcRjuois71J4ZLV836AyncYBvWqfdr4ETJ3DpSIA1gLw8w8lpw8CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAG+TPUnji6Ziyge9bIr9fEQ/4rnB2JaJXrnUxkuL3WG/vpCHBwWuSw67nHo4CzQx7XUgrA8sWZPnL1JFViWaFN1kKy/4veUtuMF12gBDwAs9egUDqb1jijcg7V9gv6aegftq0cXH6mU6qhUCtDm8Q5jMBn2v3FpQBXcTNZa4jWUDy2TkrKwssMlBFB3Jz+k2rMe1jsFc0ZoFyCmAqU7Vb80tRO0/RC4zjmO3YQXpUYjxd6frh3LRSl6626P6Qpf/szX4bpZp3s4Kuf1J/M7wF2/pcQfcoypXPv3iDlaqOU3VbjOgNCj3OHmJjabmin0mFbwN08pFNthFGvv8Xxe6Hkw==\\\" mi=\\\"MFS100\\\" rdsId=\\\"MANTRA.AND.001\\\" rdsVer=\\\"1.0.5\\\">
# 		<additional_info>
# 			<Param name=\\\"srno\\\" value=\\\"2174371\\\"/>
# 			<Param name=\\\"sysid\\\" value=\\\"356922093643968\\\"/>
# 			<Param name=\\\"ts\\\" value=\\\"2021-12-06T06:48:25+05:30\\\"/>
# 		</additional_info>
# 	</DeviceInfo>
# 	<Hmac>fTun00oL2ZVMzDRTWVcQA2mCbD6lk9JHLaBtOM3YiNrXUDvVdmemY9WplASeCJ8Z</Hmac>
# 	<Resp errCode=\\\"0\\\" errInfo=\\\"Capture Success\\\" fCount=\\\"1\\\" fType=\\\"0\\\" iCount=\\\"0\\\" iType=\\\"0\\\" nmPoints=\\\"35\\\" pCount=\\\"0\\\" pType=\\\"0\\\" qScore=\\\"83\\\"/>
# 	<Skey ci=\\\"20221021\\\">agdti+4wZR9bKRVEHGMknQRUqTiFbloF4HoY7ko1GoVTj7uDMklfgkS1C/NljxJgnYyPY3TRjpvBHtOOuYKxbN/nD1zZxKcGokwENOIyAU6Ac+jm+iqeuNA7AWS/l/fDNs+70pRNg5ZeVh5eDQ8p6mDnPxyu0V7YanOfyD8PDim3YgXiI2Isg4NFJAsY8vGAKBygp6+L7lg8vu9QPFS5vin1KE0eAUyruhrsoNl8r1a0O2tQUssra+JO4aqdjIlgtp+Xlgx9sot43UpCa7HVdF+ASJXojptQYaC6yAoZj9HgrBQm2SmV6U/5J5krcr/75LBxPKQumuiuh+3WktTdnQ==</Skey>
# </PidData>''', content_type='text/xml') ()
#     # return Response({'success': False, 'errors': serializer.errors})


from django.http import HttpResponse
from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString

@api_view(['POST', 'OPTIONS', 'CAPTURE'])
@permission_classes([AllowAny])
def eko_txn_callback(request):
    print('===>', request.data)

    # Create an XML element
    pid_data = ET.Element('PidData')
    data = ET.SubElement(pid_data, 'Data', type='X')
    data.text = '''<PidData>
	<Data type=\\\"X\\\">MjAyMS0xMi0wNlQwNjo0ODoyM51MswAVy/PSZSqgXRudRMXTP356NsUJ4q4qItIZDjYZfOD4zwDpqlKT4aU927NvMJm6+IxgTTZEFngZ0TY+ibqUeQQiB7JEwj+8xeeO+7Y+G4yJmL7FjqNfQG7O/AgMP8AXWFS522iUeGmqkyf7InpXIj7VCiKlNDu+QNu+donxOQ6hRlNJ5J0kc082Fct4hvEr4iFVL9UrAx1+kR8yDbLAISxc+37RI7cxn577uNsazb/jy7O+tTk9zE6Ia3uPY0uqKfMNqNhSTomHMeJo5S0wuOW7uyRYrvz8Q4hUlCuqsup0ZmKA5su1F7HU60q6DHkO0eH+mk8Q/gA8ymaEHeBadkd+i/8tTZnxDyp/gw+z3vT+MPZNLKT4WAE5w2nhOoOOS+F9NPpJ2mn+FqwkRQ7VnEv09g0/bTyAZHCvmhUAy/NHYVYEPaycRpoSIzGuA3REoX++HaOetubgBx9vVVIl5ZKAR4hlwzuGJbcFlyJh6uxjQIK1bJh/jPJH/m+WyJpZwc99IArg9hnBkUFTO42ZeaHXj7+4BNDahs6vFtoquJGFXHYkZUZ866itGA6Dh8iJCjIjd8f6IEah1U+SKX0mkAzh4IM91lw6sIeNpykMwk99FTDJ33vkW+ao1mf/LK8yWV3hisEGqQtCAhn3S71lpf/pJk4TOVLIJKwqnlcsin6mWcLr3Ve8xkWvJW8dRVfZ+KbQTpdOU4oQs3iv4jl0ORbuJJhVC2IEOGpUfpQyS8OO0x8D7RTvl+L3FmtKIXNZ7qlfkYdxKnH3a0QSvFY8KFpxOhUKcQXqIWU/Yuhtldgjb6D2Ys2QvgR99kRhDF7449fbqkQnnNF8uIGX3MIailsw/JFcTiko22s6in6gzPuv7AoPl1XIfDURnvQQnxlGb3MArO2rD48SVmNpwYGBnGTTyV1OYl9EbrJ1NPVcoXFCt6tcDDXwnhB09iJK7PWmKuIe5wP8dGWK/kgdYuEYRmsso+niYg2zUwdt41JGFPVJR0eCwNCOcmQ2uocPGmukB3h0h6dR1mMCTYBPUyNIxQznMxGAj72N0yHXwCS5FR6Qih8sYTDA/x1OOnuANK/m7CuCJ6H+tv48PU6vubtQAfxKCXQMiUZp0qbc</Data>
	<DeviceInfo dc=\\\"79bfab62-5fd1-4ea1-bf5c-00cc714ae571\\\" dpId=\\\"MANTRA.MSIPL\\\" mc=\\\"MIIEGjCCAwKgAwIBAgIGAX0iDKcNMA0GCSqGSIb3DQEBCwUAMIHqMSowKAYDVQQDEyFEUyBNYW50cmEgU29mdGVjaCBJbmRpYSBQdnQgTHRkIDcxQzBBBgNVBDMTOkIgMjAzIFNoYXBhdGggSGV4YSBvcHBvc2l0ZSBHdWphcmF0IEhpZ2ggQ291cnQgUyBHIEhpZ2h3YXkxEjAQBgNVBAkTCUFobWVkYWJhZDEQMA4GA1UECBMHR3VqYXJhdDEdMBsGA1UECxMUVGVjaG5pY2FsIERlcGFydG1lbnQxJTAjBgNVBAoTHE1hbnRyYSBTb2Z0ZWNoIEluZGlhIFB2dCBMdGQxCzAJBgNVBAYTAklOMB4XDTIxMTEyNTEyMjEzNVoXDTIxMTIxNTA1MjMxMlowgbAxJTAjBgNVBAMTHE1hbnRyYSBTb2Z0ZWNoIEluZGlhIFB2dCBMdGQxHjAcBgNVBAsTFUJpb21ldHJpYyBNYW51ZmFjdHVyZTEOMAwGA1UEChMFTVNJUEwxEjAQBgNVBAcTCUFITUVEQUJBRDEQMA4GA1UECBMHR1VKQVJBVDELMAkGA1UEBhMCSU4xJDAiBgkqhkiG9w0BCQEWFXN1cHBvcnRAbWFudHJhdGVjLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALwP8kOTVlcHl1sOaXo3e1DLJJMRdrfrVOsAsgkrZQNnppVB8c9hY0OPP9ncWNl7SMobrrA6k2lSI0RDd1/4vd11ZUlic/IaHkNJQ6XJHE+Cwl8r2zVlAIO/cyibm7oPZRuf6TFzwrxltxuRL9J81lT/bm53injV8Six7Zg0pYqoJ1kwXqxF3ql+T3SCDp9zUfohwC60X3lFnqxOLgrIH430exaSsRl1UjnaDbU71ihme1yXDeVkKaQNIlTXbj1RJNXeHJpJMEpDyld54oHTmvSIsZip/QmT8rzUHcRjuois71J4ZLV836AyncYBvWqfdr4ETJ3DpSIA1gLw8w8lpw8CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAG+TPUnji6Ziyge9bIr9fEQ/4rnB2JaJXrnUxkuL3WG/vpCHBwWuSw67nHo4CzQx7XUgrA8sWZPnL1JFViWaFN1kKy/4veUtuMF12gBDwAs9egUDqb1jijcg7V9gv6aegftq0cXH6mU6qhUCtDm8Q5jMBn2v3FpQBXcTNZa4jWUDy2TkrKwssMlBFB3Jz+k2rMe1jsFc0ZoFyCmAqU7Vb80tRO0/RC4zjmO3YQXpUYjxd6frh3LRSl6626P6Qpf/szX4bpZp3s4Kuf1J/M7wF2/pcQfcoypXPv3iDlaqOU3VbjOgNCj3OHmJjabmin0mFbwN08pFNthFGvv8Xxe6Hkw==\\\" mi=\\\"MFS100\\\" rdsId=\\\"MANTRA.AND.001\\\" rdsVer=\\\"1.0.5\\\">
		<additional_info>
			<Param name=\\\"srno\\\" value=\\\"2174371\\\"/>
			<Param name=\\\"sysid\\\" value=\\\"356922093643968\\\"/>
			<Param name=\\\"ts\\\" value=\\\"2021-12-06T06:48:25+05:30\\\"/>
		</additional_info>
	</DeviceInfo>
	<Hmac>fTun00oL2ZVMzDRTWVcQA2mCbD6lk9JHLaBtOM3YiNrXUDvVdmemY9WplASeCJ8Z</Hmac>
	<Resp errCode=\\\"0\\\" errInfo=\\\"Capture Success\\\" fCount=\\\"1\\\" fType=\\\"0\\\" iCount=\\\"0\\\" iType=\\\"0\\\" nmPoints=\\\"35\\\" pCount=\\\"0\\\" pType=\\\"0\\\" qScore=\\\"83\\\"/>
	<Skey ci=\\\"20221021\\\">agdti+4wZR9bKRVEHGMknQRUqTiFbloF4HoY7ko1GoVTj7uDMklfgkS1C/NljxJgnYyPY3TRjpvBHtOOuYKxbN/nD1zZxKcGokwENOIyAU6Ac+jm+iqeuNA7AWS/l/fDNs+70pRNg5ZeVh5eDQ8p6mDnPxyu0V7YanOfyD8PDim3YgXiI2Isg4NFJAsY8vGAKBygp6+L7lg8vu9QPFS5vin1KE0eAUyruhrsoNl8r1a0O2tQUssra+JO4aqdjIlgtp+Xlgx9sot43UpCa7HVdF+ASJXojptQYaC6yAoZj9HgrBQm2SmV6U/5J5krcr/75LBxPKQumuiuh+3WktTdnQ==</Skey>
</PidData>'''

    device_info = ET.SubElement(pid_data, 'DeviceInfo', dc='79bfab62-5fd1-4ea1-bf5c-00cc714ae571', dpId='MANTRA.MSIPL', mc='MIIEGjCCAwKgAwIBAgIGAX0iDKcNMA0GCSqGSIb3DQEBCwUAMIHqMSowKAYDVQQDEyFEUyBNYW50cmEgU29mdGVjaCBJbmRpYSBQdnQgTHRkIDcxQzBBBgNVBDMTOkIgMjAzIFNoYXBhdGggSGV4YSBvcHBvc2l0ZSBHdWphcmF0IEhpZ2ggQ291cnQgUyBHIEhpZ2h3YXkxEjAQBgNVBAkTCUFobWVkYWJhZDEQMA4GA1UECBMHR3VqYXJhdDEdMBsGA1UECxMUVGVjaG5pY2FsIERlcGFydG1lbnQxJTAjBgNVBAoTHE1hbnRyYSBTb2Z0ZWNoIEluZGlhIFB2dCBMdGQxCzAJBgNVBAYTAklOMB4XDTIxMTEyNTEyMjEzNVoXDTIxMTIxNTA1MjMxMlowgbAxJTAjBgNVBAMTHE1hbnRyYSBTb2Z0ZWNoIEluZGlhIFB2dCBMdGQxHjAcBgNVBAsTFUJpb21ldHJpYyBNYW51ZmFjdHVyZTEOMAwGA1UEChMFTVNJUEwxEjAQBgNVBAcTCUFITUVEQUJBRDEQMA4GA1UECBMHR1VKQVJBVDELMAkGA1UEBhMCSU4xJDAiBgkqhkiG9w0BCQEWFXN1cHBvcnRAbWFudHJhdGVjLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALwP8kOTVlcHl1sOaXo3e1DLJJMRdrfrVOsAsgkrZQNnppVB8c9hY0OPP9ncWNl7SMobrrA6k2lSI0RDd1/4vd11ZUlic/IaHkNJQ6XJHE+Cwl8r2zVlAIO/cyibm7oPZRuf6TFzwrxltxuRL9J81lT/bm53injV8Six7Zg0pYqoJ1kwXqxF3ql+T3SCDp9zUfohwC60X3lFnqxOLgrIH430exaSsRl1UjnaDbU71ihme1yXDeVkKaQNIlTXbj1RJNXeHJpJMEpDyld54oHTmvSIsZip/QmT8rzUHcRjuois71J4ZLV836AyncYBvWqfdr4ETJ3DpSIA1gLw8w8lpw8CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAG+TPUnji6Ziyge9bIr9fEQ/4rnB2JaJXrnUxkuL3WG/vpCHBwWuSw67nHo4CzQx7XUgrA8sWZPnL1JFViWaFN1kKy/4veUtuMF12gBDwAs9egUDqb1jijcg7V9gv6aegftq0cXH6mU6qhUCtDm8Q5jMBn2v3FpQBXcTNZa4jWUDy2TkrKwssMlBFB3Jz+k2rMe1jsFc0ZoFyCmAqU7Vb80tRO0/RC4zjmO3YQXpUYjxd6frh3LRSl6626P6Qpf/szX4bpZp3s4Kuf1J/M7wF2/pcQfcoypXPv3iDlaqOU3VbjOgNCj3OHmJjabmin0mFbwN08pFNthFGvv8Xxe6Hkw==</Skey>''')
    additional_info = ET.SubElement(device_info, 'additional_info')
    param1 = ET.SubElement(additional_info, 'Param', name='srno', value='2174371')
    param2 = ET.SubElement(additional_info, 'Param', name='sysid', value='356922093643968')
    param3 = ET.SubElement(additional_info, 'Param', name='ts', value='2021-12-06T06:48:25+05:30')

    hmac = ET.SubElement(pid_data, 'Hmac')
    hmac.text = 'fTun00oL2ZVMzDRTWVcQA2mCbD6lk9JHLaBtOM3YiNrXUDvVdmemY9WplASeCJ8Z'

    resp = ET.SubElement(pid_data, 'Resp', errCode='0', errInfo='Capture Success', fCount='1', fType='0', iCount='0', iType='0', nmPoints='35', pCount='0', pType='0', qScore='83')

    skey = ET.SubElement(pid_data, 'Skey', ci='20221021')
    skey.text = 'agdti+4wZR9bKRVEHGMknQRUqTiFbloF4HoY7ko1GoVTj7uDMklfgkS1C/NljxJgnYyPY3TRjpvBHtOOuYKxbN/nD1zZxKcGokwENOIyAU6Ac+jm+iqeuNA7AWS/l/fDNs+70pRNg5ZeVh5eDQ8p6mDnPxyu0V7YanOfyD8PDim3YgXiI2Isg4NFJAsY8vGAKBygp6+L7lg8vu9QPFS5vin1KE0eAUyruhrsoNl8r1a0O2tQUssra+JO4aqdjIlgtp+Xlgx9sot43UpCa7HVdF+ASJXojptQYaC6yAoZj9HgrBQm2SmV6U/5J5krcr/75LBxPKQumuiuh+3WktTdnQ=='

    # Serialize XML element to string
    xml_string = ET.tostring(pid_data)
    pretty_xml = parseString(xml_string).toprettyxml()

    # Set response headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'X-Requested-With',
        'Content-Type': 'text/xml',
    }

    # Return HTTP response with serialized XML content
    return HttpResponse(pretty_xml, headers=headers)


@api_view(['GET', 'POST'])
def pay_sprint_onboarding_callback(request):
    logger.error(f"Request Body: {request.data}")
    if request.method == 'POST':
        try:
            data = request.data

            if data.get("event") == "MERCHANT_ONBOARDING":
                request_id = data.get("param").get("request_id")
                amount = data.get("param").get("amount")
                merchant_id = data.get("param").get("merchant_id")

                user = UserAccount.objects.get(platform_id=merchant_id)
                wallet = Wallet2.objects.get(userAccount=user)
                onboarding_charge = PaySprintCommissionCharge.objects.get(service_type='Onboarding')

                if wallet.balance < onboarding_charge.flat_charge:
                    return Response({"status": 400,"message": "Transaction Failed"}, status=400)

                wallet.balance -= onboarding_charge.flat_charge
                wallet.save()
                # Log Transaction
                Wallet2Transaction.objects.create(
                    wallet2=wallet,
                    txnId=request_id,
                    amount=onboarding_charge.flat_charge,
                    txn_status='Success',
                    client_ref_id="N/A",
                    description="AEPS 2 Onboarding Charges",
                    transaction_type="Onboarding Charges Deduct"
                )

                # user.pay_sprint_ref_no = request_id
                # user.save()

                return Response({"status":200,"message":"Transaction completed successfully"}, status=200)

            elif data.get("event") == "MERCHANT_STATUS_ONBOARD":
                return Response({"status":200,"message":"Transaction completed successfully"}, status=200)
        except Exception as e:
            logger.error(f"Error in {__name__}: {e}")
            return Response({"status": 400,"message": "Transaction Failed"}, status=400)

        # elif  data.get("event") == "PAYOUT_SETTLEMENT":
        #     request_id = data.get("param").get("request_id")
        #     amount = data.get("param").get("amount")
        #     merchant_id = data.get("param").get("merchant_id")
        #
        #     user = UserAccount.objects.get(platform_id=merchant_id)
        #     wallet = Wallet.objects.get(userAccount=user)
        #
        #     if wallet.balance < amount:
        #         return Response({"status": 400,"message": "Transaction Failed"}, status=400)
        #
        #     wallet.balance -= float(amount)
        #     wallet.save()
        #
        #     user.pay_sprint_ref_no = request_id
        #     user.save()
        #
        #     return Response({"status":200,"message":"Transaction completed successfully"}, status=200)

    elif request.method == 'GET':
        data = request.GET.get('data')
        params = urlencode({'data': data})
        url = f"{reverse('dashboard')}?{params}"
        return redirect(url)
