import qrcode
from io import BytesIO
from backend.models import (WalletTransaction, ServiceActivation, PaySprintMerchantAuth, PaySprintPayout, Wallet,
                            Wallet2Transaction)
from django.utils import timezone
import hmac
import base64
import hashlib
from django.db import transaction
from datetime import datetime, timedelta
from core.models import UserAccount
import random
import time
import socket
import jwt
from backend.config.secrets import JWT_KEY, AUTHORISED_KEY, PARTNER_ID, AES_ENCRYPTION_IV, AES_ENCRYPTION_KEY
from backend.config.consts import PaySprintRoutes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
import json
import logging


logger = logging.getLogger(__name__)


def generate_unique_id():
    timestamp = int(time.time() * 1000000)  # Microsecond precision
    random_part = random.randint(0, 999)  # Random component
    machine_id = socket.gethostname().replace('-', '')  # Machine identifier (hostname)

    # Combine components and truncate to meet length constraint
    unique_id = f'AB{timestamp}{random_part}{machine_id}'
    unique_id = unique_id.replace('-', '')[:20]  # 18 characters to accommodate "AB" prefix

    return unique_id

# check the user is admin
def is_admin_user(user):
    return user.groups.filter(name='Admin').exists()

def is_distributor_access(user):
    return user.groups.filter(name='Distributor').exists() or user.groups.filter(name='Master Distributor').exists() or user.groups.filter(name='Admin').exists()

def is_master_distributor_access(user):
    return user.groups.filter(name='Master Distributor').exists() or user.groups.filter(name='Admin').exists()

# check the user's KYC completed
def is_kyc_completed(user):
    return user.kycStatus == 'C'

# check if the user onboard
def is_user_onboard(user):
    return user.eko_user_code is not None

# convert qr_string into image
def generate_qr_code(qr_string):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to bytes
    buffer = BytesIO()
    img.save(buffer)
    image_bytes = buffer.getvalue()
    buffer.close()

    return image_bytes

# generate tranaction Id with a Prefix
# def generate_transaction_id(transaction_prefix):
#     try:
#         last_transaction = WalletTransaction.objects.latest('id')
#     except WalletTransaction.DoesNotExist:
#         last_transaction = None

#     # Get the current date and time
#     now = timezone.now()

#     # If there are no existing transactions or the month has changed, reset the sequence
#     if last_transaction is None or last_transaction.timestamp.month != now.month or last_transaction.timestamp.year != now.year:
#         unique_sequence = 0
#     else:
#         unique_sequence = last_transaction.unique_sequence

#     transaction_number = "{:07d}".format(unique_sequence + 1)

#     current_month = now.month
#     current_year = str(now.year)[-2:]

#     transaction_id = f'{transaction_prefix}{current_year}{current_month:02d}{transaction_number}'

#     return transaction_number, transaction_id

# Get secret key for API authentication
def generate_key():
    key = "d3d8a58d-d437-46bf-bbeb-f7a601a437f8"
    
    # Encode it using base64
    encoded_key = base64.b64encode(key.encode()).decode()

    # Generate timestamp
    timestamp = str(int(datetime.now().timestamp() * 1000))

    # Compute the signature by hashing the timestamp with the encoded key
    signature = hmac.new(encoded_key.encode(), timestamp.encode(), hashlib.sha256).digest()

    # Encode it using base64 to get the secret key
    secret_key = base64.b64encode(signature).decode().strip()

    return secret_key, timestamp


def generate_platform_id(user_code):
    try:
        last_user = UserAccount.objects.latest('id')
    except UserAccount.DoesNotExist:
        last_user = None

    # Get the current date and time
    now = timezone.now()
    
    # If there are no existing users or the month has changed, reset the sequence
    if last_user is None or last_user.date_joined.month != now.month or last_user.date_joined.year != now.year:
        unique_sequence = 0
    else:
        unique_sequence = last_user.unique_sequence

    serial_number = "{:04d}".format(unique_sequence + 1)
    user_code = user_code[0]
    current_month = datetime.now().month
    current_year = str(datetime.now().year)[-2:]
    platform_id = f'AB{user_code}{current_year}{current_month:02d}{serial_number}'
    return serial_number, platform_id


# check if the user onboard
def is_qrpayment_activated(user):
    obj = ServiceActivation.objects.get(userAccount=user).QrPaymentService
    return obj


def get_client_ip(request):
    # Extract the client's IP address from different headers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    remote_addr = request.META.get('REMOTE_ADDR')

    # Initialize variable to store the IPv4 address
    ipv4_address = None

    # Check X-Forwarded-For header for IPv4 address
    if x_forwarded_for:
        # Split the X-Forwarded-For header by comma and iterate through each part
        for addr in x_forwarded_for.split(','):
            # Remove any leading/trailing spaces
            addr = addr.strip()
            # Check if the address is a valid IPv4 address
            if '.' in addr and ':' not in addr:
                ipv4_address = addr
                break  # Found IPv4 address, exit loop

    # Check X-Real-IP header for IPv4 address
    if not ipv4_address and x_real_ip:
        # Remove any leading/trailing spaces
        x_real_ip = x_real_ip.strip()
        # Check if the address is a valid IPv4 address
        if '.' in x_real_ip and ':' not in x_real_ip:
            ipv4_address = x_real_ip

    # Check REMOTE_ADDR header for IPv4 address
    if not ipv4_address and remote_addr:
        # Remove any leading/trailing spaces
        remote_addr = remote_addr.strip()
        # Check if the address is a valid IPv4 address
        if '.' in remote_addr and ':' not in remote_addr:
            ipv4_address = remote_addr

    # Return the extracted IPv4 address
    return ipv4_address


# def get_token():
#     timestamp = int(time.time())
#     random_number = random.randint(1, 1000000000)
#     secret_key = "UFMwMDE2NjY1Y2RhZmRhZDAzZmJjZjdiNmU2YzE5N2RhOWY1ODdlYQ=="
    
#     payload = {
#         "timestamp": timestamp,
#         "partnerId": "PS001666",
#         "reqid": random_number
#     }
    
#     token = jwt.encode(payload, secret_key, algorithm='HS256')
#     return token

def get_token():
    random_number = round(random.random() * 1000000000)
    timestamp = int(time.time() * 1000)
    secret_key = "UFMwMDE2NjY1Y2RhZmRhZDAzZmJjZjdiNmU2YzE5N2RhOWY1ODdlYQ=="
    
    payload = {
        "iss": "PSPRINT",
        "timestamp": timestamp,
        "partnerId": "PS001666",
        "reqid": random_number
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return token


def is_user_registered_with_paysprint(user):
    if not user.pay_sprint_ref_no:
        return False
    return True


def generate_pay_sprint_token():
    payload = {
        "timestamp": int(time.time() * 1000),
        "partnerId": PARTNER_ID,
        "reqid": str(int(time.time() * 1000)),
    }
    
    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')
    return token


def get_pay_sprint_headers():
    headers = {
        "Token": generate_pay_sprint_token()
        # "Authorisedkey": AUTHORISED_KEY
    }
    logger.error(f"Request Headers: {json.dumps(headers)}")
    return headers


def decrypt_pay_sprint_token_token(token):
    try:
        decoded_payload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def encrypt_aes_128(data):
    try:
        key = AES_ENCRYPTION_KEY.encode('utf-8')
        iv = AES_ENCRYPTION_IV.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(data.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        raise Exception(f"Encryption error: {e}")


def get_pay_sprint_common_payload(request, user):
    latitude, longitude = request.POST.get("latlong").split(",")
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "mobilenumber": user.mobile,
        "referenceno": int(time.time() * 1000),
        "ipaddress": get_client_ip(request),
        "adhaarnumber": request.POST.get("aadhar_no"),
        "accessmodetype": "SITE",
        "data": request.POST.get("data"),
        # "data": fingerprint_data,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "submerchantid": user.platform_id,
    }
    return data


def get_pay_sprint_payload(request, user, transaction_type, merchant_auth_txn_id = None):
    data = get_pay_sprint_common_payload(request, user)
    data.update({
        "nationalbankidentification": request.POST.get("bank_identifier"),
        "requestremarks": request.POST.get("remarks"),
        "pipe": request.POST.get("aeps_bank"),  # "bank2 OR bank3// bank1 work for UAT only",
        "transactiontype": transaction_type,
        "is_iris": "No"
    })
    if transaction_type in ["CW", "M", "FM", "IM"]:
        data["amount"] = request.POST.get("amount")
    if transaction_type == "CW":
        data["MerAuthTxnId"] = merchant_auth_txn_id
    return data


def is_merchant_bank_registered(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    if obj:
        return obj.is_bank2_registered or obj.is_bank3_registered
    return False


def is_merchant_bank2_registered(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    return obj.is_bank2_registered if obj else False


def is_merchant_bank3_registered(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    return obj.is_bank3_registered if obj else False


def is_bank2_last_authentication_valid(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    last_auth_date = obj.bank2_last_authentication_date
    is_auth_valid = False
    if last_auth_date:
        is_auth_valid = timezone.now() <= last_auth_date + timedelta(hours=24)
        if not is_auth_valid:
            obj.bank2_MerAuthTxnId = None
            obj.save()
    return is_auth_valid


def is_bank3_last_authentication_valid(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    last_auth_date = obj.bank3_last_authentication_date
    if last_auth_date:
        return timezone.now() <= last_auth_date + timedelta(hours=24)
    else:
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        merchant_auth.bank3_MerAuthTxnId = None
        return False


def is_bank2_MerAuthTxnId_present(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    return True if obj.bank2_MerAuthTxnId else False


def is_bank3_MerAuthTxnId_present(user):
    obj = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
    return True if obj.bank3_MerAuthTxnId else False


def make_post_request(url, data):
    # logger.error("#################################")
    # logger.error(f"API URL: {json.dumps(url)}")
    payload = {"body": encrypt_aes_128(json.dumps(data))}
    response = requests.post(url, json=payload, headers=get_pay_sprint_headers())
    # logger.error(f"Request Data: {json.dumps(data)}")
    # logger.error(f"Encrypted Request Body: {json.dumps(payload)}")
    # logger.error(f"Response Body: {json.dumps(response.json())}")
    # logger.error("#################################")
    return response


def update_payout_statuses(user):
    try:
        payouts = PaySprintPayout.objects.filter(userAccount=user, txn_status__in=['2', '3', '4'])
        payouts_to_update = []
        for payout in payouts:
            payload = {
                "refid": payout.client_ref_id,
                "ackno": payout.tid
            }
            response = requests.post(PaySprintRoutes.TRANSACTION_STATUS.value, json=payload, headers=get_pay_sprint_headers())
            api_data = response.json().get("data")

            if api_data:
                payout.txn_status = api_data.get("txn_status", payout.txn_status)
                payouts_to_update.append(payout)
        if payouts_to_update:
            with transaction.atomic():
                PaySprintPayout.objects.bulk_update(payouts_to_update, ['txn_status'])
    except Exception as e:
        print(f"Error updating payout statuses: {e}")


def get_aadhaar_pay_txn_status(reference_no: str):
    payload = { "Raw_Body": { "body": encrypt_aes_128(json.dumps({'reference': reference_no})) } }
    response = requests.post(url=PaySprintRoutes.AADHAR_PAY_TXN_STATUS.value, json=payload, headers=get_pay_sprint_headers())
    if response.status_code == 200:
        api_data = response.json()
        status = api_data.get('status', False)
        txn_status = api_data.get('txnstatus', 0)
        response_code = api_data.get('response_code', 0)

        if status and txn_status == 1 and response_code == 1:
            return "1"  # Success
        elif status and txn_status == 3 and response_code == 0:
            return "0"  # Failed
        elif status and txn_status == 2 and response_code == 2:
            return "2"  # Pending
        elif not status and response_code == 3:
            return "3"  # Txn_Not_Found
        else:
            return "other"  # Bad_Request
    return "2"


def update_wallet(wallet, amount, txnid, description, action_type):
    """Helper function to update wallet and log transaction."""
    if action_type == 'addWallet':
        wallet.balance += amount
        transaction_type = 'Admin Deposit'
    else:
        wallet.balance -= amount
        transaction_type = 'Admin Deduct'

    wallet.save()

    # Create a transaction entry
    if isinstance(wallet, Wallet):
        WalletTransaction.objects.create(
            wallet=wallet,
            txnId=txnid,
            amount=amount,
            txn_status='Success',
            client_ref_id=generate_unique_id(),
            description=description,
            transaction_type=transaction_type
        )
    else:
        Wallet2Transaction.objects.create(
            wallet=wallet,
            txnId=txnid,
            amount=amount,
            txn_status='Success',
            client_ref_id=generate_unique_id(),
            description=description,
            transaction_type=transaction_type
        )


electricity_operator_id = [22, 23, 24, 53, 55, 56, 57, 59, 60, 61, 62, 63, 69, 76, 78, 81, 82, 96, 101, 107, 109, 115, 121, 122, 125, 126, 131, 133, 136, 137, 138, 139, 140, 141, 142, 143, 145, 148, 149, 150, 153, 155, 156, 160, 164, 166, 171, 174, 175, 178, 190, 195, 198, 204, 230, 238, 239, 242, 243, 244, 245, 246, 247, 364, 375, 397, 452, 465, 473, 491, 546, 598, 603, 618, 619, 2706, 2707]

recharge_postpaid_operator_id = [41, 89, 172, 254, 507, 615]

water_gas_lpg_operator_id = [116, 117, 130, 135, 161, 162, 165, 167, 173, 177, 179, 183, 187, 193, 194, 260, 353, 361, 363, 451, 453, 454, 459, 462, 466, 470, 483, 495, 496, 497, 509, 510, 522, 538, 540, 541, 547, 566, 577, 605, 608, 610, 28, 50, 51, 65, 113, 124, 128, 132, 157, 158, 163, 168, 176, 189, 191, 196, 248, 318, 341, 394, 396, 499, 524, 559, 270, 275, 438]

gas_operator_id = [28, 50, 51, 65, 113, 124, 128, 132, 157, 158, 163, 168, 176, 189, 191, 196, 248, 318, 341, 394, 396, 499, 524, 559]

lpg_operator_id = [270, 275, 438]

dth_operator_id = [16, 17, 20, 21, 95]

loan_operator_id = [269, 280, 300, 302, 304, 307, 310, 311, 312, 314, 315, 316, 317, 321, 322, 324, 327, 328, 329, 331, 332, 334, 336, 339, 340, 342, 345, 346, 348, 349, 350, 351, 352, 354, 355, 356, 357, 359, 365, 368, 372, 373, 374, 376, 378, 380, 381, 384, 386, 389, 390, 415, 420, 421, 423, 424, 425, 428, 430, 435, 436, 439, 440, 441, 442, 444, 450, 457, 461, 464, 468, 474, 475, 476, 477, 479, 480, 482, 488, 489, 490, 494, 498, 500, 502, 504, 505, 506, 513, 514, 515, 516, 517, 518, 519, 526, 527, 528, 529, 530, 531, 552, 555, 557, 560, 564, 569, 570, 571, 574, 575, 578, 580, 581, 584, 586, 588, 589, 597, 604, 607, 611, 612, 2521, 2533, 2657, 2658, 2659, 2660, 2661, 2662, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2674, 2675, 2676, 2677, 2678, 2679, 2680, 2681, 2682, 2683, 2684, 2685, 2686, 2687, 2688, 2689, 2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698, 2699, 2700, 2701, 2702, 2703, 2704]

recharge_prepaid_operator_id = [1, 5, 90, 91, 400, 508]