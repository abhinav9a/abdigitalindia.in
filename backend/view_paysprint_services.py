from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
import logging
import json

from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
import requests

from backend.utils import (
    is_kyc_completed,
    get_pay_sprint_headers,
    get_pay_sprint_payload,
    is_merchant_bank_registered,
    is_merchant_bank2_registered,
    is_merchant_bank3_registered,
    is_user_registered_with_paysprint,
    get_pay_sprint_common_payload,
    generate_unique_id,
    is_bank2_last_authentication_valid,
    is_bank3_last_authentication_valid,
    make_post_request,
    update_payout_statuses,
    get_aadhaar_pay_txn_status,
    check_daily_kyc, is_admin_user, update_aeps_txn_status
)
from backend.utils_paysprint import (credit_aeps_commission, credit_mini_statement_commission, debit_aadhaar_pay_charges,
                                     debit_payout_charges, get_total_commission)
from backend.models import (
    PaySprintMerchantAuth,
    PaySprintAEPSTxnDetail,
    Wallet2,
    PaySprintPayout,
    PaySprintPayoutBankAccountDetails, PaySprintCommissionTxn, PaySprintCommissionCharge
)
from backend.config.consts import (
    PaySprintRoutes,
    DMT_BANK_LIST,
    PAYOUT_TRANSACTION_STATUS,
)
from core.models import UserAccount
from core.decorators import transaction_required


logger = logging.getLogger(__name__)


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
def user_onboarding(request):
    onboarding_details = UserAccount.objects.get(username=request.user)
    try:
        redirect_url = None
        if request.method == "POST":
            wallet = Wallet2.objects.get(userAccount=onboarding_details)
            onboarding_charge = PaySprintCommissionCharge.objects.get(service_type='Onboarding')
            if wallet.is_hold:
                messages.error(request, f"Wallet 2 is on hold. Reason: {wallet.hold_reason}.", extra_tags="danger")
                return redirect("onboarding_user_paysprint")
            elif wallet.balance < onboarding_charge.flat_charge:
                messages.error(request, "Insufficient Wallet 2 balance to complete onboarding.", extra_tags="danger")
                return redirect("onboarding_user_paysprint")

            mobile_number = request.POST.get("mobile_number")
            email = request.POST.get("email")
            shop_name = request.POST.get("shop_name")
            message = None

            payload = {
                "merchantcode": request.user.platform_id,
                "mobile": mobile_number,
                "is_new": "1",
                "email": email,
                "firm": shop_name,
                "callback": PaySprintRoutes.CALLBACK_URL.value,
            }
            logger.error(f"PaySprint onboarding payload: {payload}")
            try:
                response = requests.post(
                    PaySprintRoutes.WEB_ONBOARDING.value,
                    json=payload,
                    headers=get_pay_sprint_headers(),
                )
                logger.error(f"PaySprint onboarding response {response.text}")
                if response.status_code == 200:
                    api_data = response.json()
                    if api_data.get("onboard_pending") == 0:
                        messages.success(request, api_data.get("message"))
                        return redirect("dashboard")
                    redirect_url = api_data.get("redirecturl")
                    return render(
                        request,
                        "backend/Services/AEPS/AEPS_PaySprint.html",
                        {"url": redirect_url},
                    )
                else:
                    # logger.error("PaySprint onboarding failed", extra={"response": response.text})
                    try:
                        message = response.json().get("message", response.text)
                    except Exception as e:
                        logger.error(f"Error in {__name__}: {e}", exc_info=True)
                        message = response.text
                    messages.error(request, message=message, extra_tags="danger")
            except Exception as e:
                logger.exception(f"Unexpected error during PaySprint onboarding. {e}")
                messages.error(
                    request, "An unexpected error occurred. Please try again later."
                )
    except Wallet2.DoesNotExist:
            messages.error(request, message='User Wallet Not Found', extra_tags='danger')
    except Exception as e:
        logger.exception(f"Unexpected error in user_onboarding view. {e}")
        messages.error(request, "An unexpected error occurred. Please try again later.")

    return render(
        request,
        "backend/Pages/onboardingUserPaySprint.html",
        {"onboarding_details": onboarding_details},
    )


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def user_onboarding_status(request):
    bank_status = []

    try:
        user = UserAccount.objects.get(username=request.user)
        common_payload = {
          "merchantcode": user.platform_id,
          "mobile": user.mobile
        }
        bank_2_payload = {**common_payload, "pipe": "bank2"}
        bank_3_payload = {**common_payload, "pipe": "bank3"}

        bank_2_response = requests.post(
            PaySprintRoutes.ONBOARD_STATUS_CHECK.value, json=bank_2_payload, headers=get_pay_sprint_headers()
        )
        bank_3_response = requests.post(
            PaySprintRoutes.ONBOARD_STATUS_CHECK.value, json=bank_3_payload, headers=get_pay_sprint_headers()
        )

        bank_2_data = bank_2_response.json()
        bank_3_data = bank_3_response.json()

        bank_status.append({
            "bank": "Bank 2 (FINO)",
            "status": bank_2_data.get("status"),
            "is_approved": bank_2_data.get("is_approved"),
            "message": bank_2_data.get("message")
        })
        bank_status.append({
            "bank": "Bank 3 (NSDL)",
            "status": bank_3_data.get("status"),
            "is_approved": bank_3_data.get("is_approved"),
            "message": bank_3_data.get("message")
        })

    except Exception as e:
        logger.error(f"Unexpected error in user_onboarding_status view. {e}", exc_info=True)

    print(f"bank status: {json.dumps(bank_status)}")
    return render(
        request,
        "backend/Pages/onboardingUserPaySprintStatus.html",
        {"data": bank_status}
    )

def get_pay_sprint_aeps_bank_list():
    # logger.debug(f"API URL: {PaySprintRoutes.AEPS_BANK_LIST.value}")
    # logger.debug(f"Request Body: NONE")
    response = requests.post(
        PaySprintRoutes.AEPS_BANK_LIST.value, headers=get_pay_sprint_headers()
    )
    # logger.debug(f"Response Body: {response.json()}")
    if response.status_code == 200:
        bank_list = response.json().get("banklist", {}).get("data", [])
        return bank_list
    else:
        logger.error(
            "Failed to fetch AEPS bank list",
            extra={"status_code": response.status_code, "response": response.text},
        )
        return []


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
@user_passes_test(is_merchant_bank_registered, login_url="merchant_registration_with_bank_paysprint")
@user_passes_test(check_daily_kyc, login_url="daily_kyc_paysprint")
def balance_enquiry(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Balance Enquiry"
    if request.method == "POST":
        if request.POST.get("data") is None:
            messages.error(request, message=request.POST, extra_tags="danger")
            return render(
                request,
                "backend/Pages/balanceEnquiry.html",
                {"user": user, "heading": heading, "bank_list": bank_list},
            )
        data = get_pay_sprint_payload(request, user, "BE")
        response = make_post_request(
            url=PaySprintRoutes.BALANCE_ENQUIRY.value, data=data
        )
        logger.error(f"Response Body - Balance Enquiry: {response.json()}")
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
            aadhaar_no = request.POST.get("aadhar_no")
            masked_aadhaar_no = "XXXXXXXX" + aadhaar_no[-4:] if aadhaar_no and len(aadhaar_no) == 12 and aadhaar_no.isdigit() else "N/A"
            response_data = {
                "userAccount": user,
                "aadhaar_no": masked_aadhaar_no,
                "reference_no": response.get("clientrefno"),
                "txn_status": response.get("response_code"),
                "message": response.get("message"),
                "ack_no": response.get("ackno"),
                "amount": response.get("amount", 0),
                "balance_amount": response.get("balanceamount", 0),
                "bank_rrn": response.get("bankrrn"),
                "bank_iin": response.get("bankiin"),
                "service_type": "3",  # Balance Enquiry
            }

            merchant_auth = PaySprintAEPSTxnDetail.objects.create(**response_data)
            return render(
                request,
                "backend/Pages/balanceEnquiry.html",
                {
                    "user": user,
                    "heading": heading,
                    "bank_list": bank_list,
                    "data": response,
                },
            )
        else:
            messages.error(
                request, message=response.json().get("message"), extra_tags="danger"
            )

    return render(
        request,
        "backend/Pages/balanceEnquiry.html",
        {"user": user, "heading": heading, "bank_list": bank_list},
    )


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
@user_passes_test(is_merchant_bank_registered, login_url="merchant_registration_with_bank_paysprint")
@user_passes_test(check_daily_kyc, login_url="daily_kyc_paysprint")
# @transaction_required
def cash_withdrawal(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Cash Withdrawal"

    if request.method == "POST":
        with transaction.atomic():
            try:
                aeps_bank = request.POST.get('aeps_bank')
                
                amount = request.POST.get('amount', 0)

                merchant_wallet = Wallet2.objects.get(userAccount=user)
                if merchant_wallet.is_hold:
                    messages.error(request, f"Wallet is on hold. Reason: {merchant_wallet.hold_reason}.", extra_tags="danger")
                    transaction.set_rollback(True)
                    return redirect("cash_withdrawl_paysprint")
        
                if aeps_bank == 'bank2':
                    return process_bank2_withdrawal(request, user)
                elif aeps_bank == 'bank3':
                    return process_bank3_withdrawal(request, user)
                else:
                    transaction.set_rollback(True)
                    messages.error(request, message="Please select AEPS Bank Provider", extra_tags="danger")
            except Exception as e:
                transaction.set_rollback(True)
                logger.exception(f"Unexpected error in cash_withdrawal view. {e}",  exc_info=True)
    context = {
        "user": user, 
        "heading": heading, 
        "bank_list": bank_list,
        "action_url": "cash_withdrawl_paysprint"
    }

    return render(
        request,
        "backend/Pages/cashWithdrawl.html",
        context,
    )

def process_bank2_withdrawal(request, user):
    if not is_merchant_bank2_registered(user):
        return redirect("merchant_registration_with_bank_paysprint")

    if not is_bank2_last_authentication_valid(user):
        messages.error(request, "Bank 2 Daily KYC Pending.", extra_tags="danger")
        return redirect("daily_kyc_paysprint")

    # merchant_authenticity_response = merchant_authenticity_bank_2_api(request=request, user=user)

    # if merchant_authenticity_response.status_code == 200 and is_bank2_last_authentication_valid(user):
    #     merchant_auth_txn_id = PaySprintMerchantAuth.objects.get(userAccount=user).bank2_MerAuthTxnId
        # return perform_withdrawal(request, user, merchant_auth_txn_id)
    return perform_withdrawal(request, user)

    # return redirect("cash_withdrawl_paysprint")

def process_bank3_withdrawal(request, user):
    if not is_merchant_bank3_registered(user):
        return redirect("merchant_registration_with_bank_paysprint")

    if not is_bank3_last_authentication_valid(user):
        messages.error(request, "Bank 3 Daily KYC Pending.", extra_tags="danger")
        return redirect("daily_kyc_paysprint")

    # merchant_authenticity_response = merchant_authenticity_bank_3_api(request=request, user=user)

    # if merchant_authenticity_response.status_code == 200 and is_bank3_last_authentication_valid(user):
    #     merchant_auth_txn_id = PaySprintMerchantAuth.objects.get(userAccount=user).bank3_MerAuthTxnId
    #     return perform_withdrawal(request, user, merchant_auth_txn_id)
    return perform_withdrawal(request, user)

    # return redirect("cash_withdrawl_paysprint")

def perform_withdrawal(request, user, merchant_auth_txn_id=None):
    amount = float(request.POST.get("amount"))
    # commission = get_total_commission(request, user, amount, "AEPS")
    # amount += float(commission)
    data = get_pay_sprint_payload(request, user, "CW", merchant_auth_txn_id)
    response = make_post_request(url=PaySprintRoutes.CASH_WITHDRAWAL.value, data=data)

    if response.status_code == 200 and response.json().get("response_code") == 1:
        response_json = response.json()
        
        aadhaar_no = request.POST.get("aadhar_no")
        masked_aadhaar_no = "XXXXXXXX" + aadhaar_no[-4:] if aadhaar_no and len(aadhaar_no) == 12 and aadhaar_no.isdigit() else "N/A"
    
        # Create Transaction Record
        transaction_data = {
            "userAccount": user,
            "aadhaar_no": masked_aadhaar_no,
            "reference_no": data.get("referenceno", "N/A"),
            "txn_status": response_json.get("txnstatus", 2),
            "message": response_json.get("message", "N/A"),
            "ack_no": response_json.get("ackno", "N/A"),
            "amount": amount,
            "bank_rrn": response_json.get("bankrrn", "N/A"),
            "service_type": "2",  # Cash Withdrawal
        }
        txn_detail = PaySprintAEPSTxnDetail.objects.create(**transaction_data)

        txn_status = check_transaction_status(data.get("referenceno"))

        if txn_status == "1":
            # Credit AEPS commission before making the request
            if not credit_aeps_commission(request, user.id):
                transaction.set_rollback(True)
                messages.error(request, message="DONE", extra_tags="success")
                return redirect("cash_withdrawl_paysprint")

        
        txn_detail.txn_status = txn_status
        txn_detail.save()

        return render(
            request,
            "backend/Pages/paymentSuccess.html",
            {"cash_withdrawl_response": transaction_data},
        )
    else:
        transaction.set_rollback(True)
        messages.error(request, response.json().get("message"), extra_tags="danger")
        return redirect("cash_withdrawl_paysprint")


def check_transaction_status(reference_no):
    response = make_post_request(url=PaySprintRoutes.CASH_WITHDRAWAL_TXN_STATUS.value, data={"reference": reference_no})

    if response.status_code == 200:
        api_data = response.json()
        status = api_data.get("status", False)
        status_code = api_data.get("txnstatus", 0)
        response_code = api_data.get("response_code", 0)

        if status and status_code == "1" and response_code == 1:
            return "1"  # Success
        elif status and status_code == "3" and response_code == 0:
            return "0"  # Failed
        elif status and status_code == "2" and response_code == 2:
            return "2"  # Pending

    return "3"  # Transaction not found


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="merchant_registration_with_bank_paysprint")
@user_passes_test(is_merchant_bank_registered, login_url="merchant_registration_with_bank_paysprint")
@user_passes_test(check_daily_kyc, login_url="daily_kyc_paysprint")
# @transaction_required
def mini_statement(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Mini Statement"
    if request.method == "POST":
        with transaction.atomic():
            # Credit mini statement commission before making the request
            if not credit_mini_statement_commission(request, user.id):
                transaction.set_rollback(True)
                return redirect("mini_statement_paysprint")
            data = get_pay_sprint_payload(request, user, "MS")
            response = make_post_request(url=PaySprintRoutes.MINI_STATEMENT.value, data=data)
            logger.error(f"Response Body - Mini Statement: {response.json()}")
            if response.status_code == 200 and response.json().get("status"):
                response = response.json()
                aadhaar_no = request.POST.get("aadhar_no")
                masked_aadhaar_no = "XXXXXXXX" + aadhaar_no[-4:] if aadhaar_no and len(aadhaar_no) == 12 and aadhaar_no.isdigit() else "N/A"
                
                response_data = {
                    "userAccount": user,
                    "aadhaar_no": masked_aadhaar_no,
                    "reference_no": data.get("referenceno"),
                    "txn_status": response.get("response_code"),
                    "message": response.get("message"),
                    "ack_no": response.get("ackno"),
                    # 'amount': response.get('amount'),
                    "balance_amount": response.get("balanceamount", 0),
                    "bank_rrn": response.get("bankrrn"),
                    "bank_iin": response.get("bankiin"),
                    "service_type": "4",  # Mini Statement
                }

                merchant_auth = PaySprintAEPSTxnDetail.objects.create(**response_data)
            else:
                messages.error(request, response.json().get("message"), extra_tags="danger")
                transaction.set_rollback(True)

        return render(
            request,
            "backend/Pages/miniStatement.html",
            {
                "user": user,
                "heading": heading,
                "bank_list": bank_list,
                "data": response,
            },
        )

    return render(
        request,
        "backend/Pages/miniStatement.html",
        {"user": user, "heading": heading, "bank_list": bank_list},
    )


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
@user_passes_test(is_merchant_bank_registered, login_url="merchant_registration_with_bank_paysprint")
@user_passes_test(check_daily_kyc, login_url="daily_kyc_paysprint")
# @transaction_required
def aadhar_pay(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_pay_sprint_aeps_bank_list()
    heading = "Aadhaar Pay"
    if request.method == "POST":
        with transaction.atomic():
            # Debit Aadhaar Pay charges before making the request
            if not debit_aadhaar_pay_charges(request, user.id):
                transaction.set_rollback(True)
                return redirect('aadhar_pay_paysprint')

            amount = float(request.POST.get("amount"))
            # commission = get_total_commission(request, user, amount, heading)
            # amount += float(commission)
            data = get_pay_sprint_payload(request, user, "M")  # M OR FM OR IM
            response = make_post_request(url=PaySprintRoutes.AADHAR_PAY.value, data=data)
            logger.error(f"Aadhaar Pay Response Body: {response.json()}")
            if response.status_code == 200 and response.json().get("response_code") == 1:
                # if True:
                response = response.json()
                aadhaar_no = request.POST.get("aadhar_no")
                masked_aadhaar_no = "XXXXXXXX" + aadhaar_no[-4:] if aadhaar_no and len(aadhaar_no) == 12 and aadhaar_no.isdigit() else "N/A"
                
                response_data = {
                    "userAccount": user,
                    "aadhaar_no": masked_aadhaar_no,
                    "reference_no": data.get("referenceno"),
                    "ack_no": response.get("ackno"),
                    "amount": amount,
                    "balance_amount": response.get("balanceamount", 0),
                    "bank_rrn": response.get("bankrrn"),
                    "bank_iin": response.get("bankiin"),
                    "service_type": "1",  # Aadhaar Pay
                    "message": response.get("message"),
                }
                merchant_auth = PaySprintAEPSTxnDetail.objects.create(**response_data)
                merchant_auth.txn_status = get_aadhaar_pay_txn_status(
                    reference_no=data.get("referenceno")
                )
                merchant_auth.save()

                return render(
                    request,
                    "backend/Pages/paymentSuccess.html",
                    {"aadhar_pay_response": response_data},
                )
            else:
                messages.error(request, response.json().get("message"), extra_tags="danger")
                transaction.set_rollback(True)

    return render(
        request,
        "backend/Pages/aadharPay.html",
        {"user": user, "heading": heading, "bank_list": bank_list},
    )


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def aeps_report(request):
    start_date_str = request.POST.get("start_date", None)
    end_date_str = request.POST.get("end_date", None)
    page = request.GET.get("page", 1)

    try:
        update_aeps_txn_status()
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(
                end_date_str, "%Y-%m-%d"
            ).date() + timedelta(days=1)
            start_date = timezone.make_aware(
                datetime.combine(start_date, datetime.min.time())
            )
            end_date = timezone.make_aware(
                datetime.combine(end_date, datetime.max.time())
            )
            transactions = PaySprintAEPSTxnDetail.objects.filter(
                userAccount=request.user, timestamp__range=[start_date, end_date]
            ).order_by("-id")
        else:
            transactions = PaySprintAEPSTxnDetail.objects.filter(
                userAccount=request.user
            ).order_by("-id")

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

    context = {"transactions_page": transactions_page}
    return render(request, "backend/Services/AEPS/AEPS_Report_PaySprint.html", context)


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def merchant_registration_with_bank(request):
    user = UserAccount.objects.get(username=request.user)
    bank2_registered = False
    bank3_registered = False
    if request.method == "POST":
        bank2_registered = merchant_registration_bank_2(request)
        bank3_registered = merchant_registration_bank_3(request)


        # Redirect to the next URL if provided
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)

    context = {
        "user": user,
        "is_bank2_registered": bank2_registered,
        "is_bank3_registered": bank3_registered,
        "title": "Merchant Registration",
        "form_submit_url": "merchant_registration_with_bank_paysprint",
    }
    return render(
        request, "backend/Pages/merchantRegistrationPaySprint.html", context=context
    )


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
@user_passes_test(is_merchant_bank_registered, login_url="merchant_registration_with_bank_paysprint")
def daily_kyc(request):
    user = UserAccount.objects.get(username=request.user)
    heading = "Mini Statement"
    if request.method == "POST":
        try:
            with transaction.atomic():
                wallet = Wallet2.objects.get(userAccount=user)
                daily_kyc_charge = PaySprintCommissionCharge.objects.get(service_type='Daily KYC')
                if wallet.is_hold:
                    messages.error(request, f"Wallet 2 is on hold. Reason: {wallet.hold_reason}.", extra_tags="danger")
                    return redirect("daily_kyc_paysprint")
                elif wallet.balance < daily_kyc_charge.flat_charge:
                    messages.error(request, "Insufficient Wallet 2 balance to complete Daily KYC.", extra_tags="danger")
                    return redirect("daily_kyc_paysprint")
                
                daily_kyc_bank_2_status = daily_kyc_bank_2(request=request, user=user)
                daily_kyc_bank_3_status = daily_kyc_bank_3(request=request, user=user)

                if daily_kyc_bank_2_status or daily_kyc_bank_3_status:
                    wallet.balance -= daily_kyc_charge.flat_charge
                    wallet.save()
                    messages.success(request, "Daily KYC completed successfully.")
                else:
                    # messages.error(request, "Daily KYC failed for both banks.", extra_tags="danger")
                    raise Exception("Daily KYC failed")
        except Exception as e:
            messages.error(request, "Daily KYC failed for both banks.", extra_tags="danger")
            logger.error("Daily KYC Failed", exc_info=True)

        return redirect("dashboard")
    
    context = {
        "user": user,
        "title": "Merchant Daily KYC",
        "form_submit_url": "daily_kyc_paysprint",
    }
    return render(
        request, "backend/Pages/dailyKYCPaySprint.html", context=context
    )

def merchant_registration_bank_2(request):
    user = UserAccount.objects.get(username=request.user)

    data = get_pay_sprint_common_payload(request, user)
    response = make_post_request(url=PaySprintRoutes.BANK_2_REGISTRATION.value, data=data)
    # logger.error(f"Response Body: {response.json()}")
    api_data = response.json()
    if response.status_code == 200 and api_data.get("errorcode") == "0":
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        if not merchant_auth:
            merchant_auth = PaySprintMerchantAuth.objects.create(
                userAccount=user,
                is_bank2_registered=True,
                registration_date=datetime.now(),
            )
        else:
            merchant_auth.is_bank2_registered = True
            merchant_auth.save()
    else:
        messages.error(request, api_data.get("message"), extra_tags="danger")

    return is_merchant_bank2_registered(user)


def daily_kyc_bank_2(request, user):
    data = get_pay_sprint_common_payload(request, user)
    response = make_post_request(
        url=PaySprintRoutes.BANK_2_AUTHENTICATION.value, data=data
    )
    logger.error(f"daily_kyc_bank_2 Response Body: {response.text}")
    api_data = response.json()
    # api_data = {
    #     "response_code": 1,
    #     "status": True,
    #     "message": "Two Factor Verification Success",
    #     "errorcode": "0"
    # }
    if response.status_code == 200:
        # if api_data.get('response_code') == 1:
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        merchant_auth.bank2_last_authentication_date = datetime.now()
        merchant_auth.save()
        messages.success(request, f'Daily KYC Bank 2: {api_data.get("message")}', extra_tags="success")
        return True
    else:
        messages.error(request, f'Daily KYC Bank 2: {api_data.get("message")}', extra_tags="danger")
        return False


def merchant_authenticity_bank_2_api(request, user):
    data = get_pay_sprint_common_payload(request, user)
    data["adhaarnumber"] = request.POST.get("merchant_aadhar_no")
    data["data"] = request.POST.get("merchant_data")
    response = make_post_request(
        url=PaySprintRoutes.BANK_2_MERCHANT_AUTHENTICITY.value, data=data
    )
    logger.error(f"Response Body: {response.json()}")
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
        merchant_auth.bank2_MerAuthTxnId = api_data.get("MerAuthTxnId")
        merchant_auth.save()
    else:
        messages.error(request, api_data.get("message"), extra_tags="danger")
    return response
    # return api_data


def merchant_registration_bank_3(request):
    user = UserAccount.objects.get(username=request.user)

    data = get_pay_sprint_common_payload(request, user)
    response = make_post_request(url=PaySprintRoutes.BANK_3_REGISTRATION.value, data=data)
    # logger.error(f"Response Body: {response.json()}")
    api_data = response.json()
    if response.status_code == 200 and api_data.get("errorcode") == "0":
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        if not merchant_auth:
            merchant_auth = PaySprintMerchantAuth.objects.create(
                userAccount=user,
                is_bank2_registered=True,
                registration_date=datetime.now(),
            )
        else:
            merchant_auth.is_bank3_registered = True
            merchant_auth.save()
    else:
        messages.error(request, api_data.get("message"), extra_tags="danger")

    return is_merchant_bank3_registered(user)


def daily_kyc_bank_3(request, user):
    data = get_pay_sprint_common_payload(request, user)
    response = make_post_request(
        url=PaySprintRoutes.BANK_3_AUTHENTICATION.value, data=data
    )
    logger.error(f"daily_kyc_bank_3 Response Body: {response.text}")
    api_data = response.json()
    # api_data = {
    #     "response_code": 1,
    #     "status": True,
    #     "message": "Two Factor Verification Success",
    #     "errorcode": "0"
    # }
    if response.status_code == 200:
        # if api_data.get('response_code') == 1:
        merchant_auth = PaySprintMerchantAuth.objects.filter(userAccount=user).first()
        merchant_auth.bank3_last_authentication_date = datetime.now()
        merchant_auth.save()
        messages.success(request, f'Daily KYC Bank 3: {api_data.get("message")}', extra_tags="success")
        return True
    else:
        messages.error(request, f'Daily KYC Bank 3: {api_data.get("message")}', extra_tags="danger")
        return False


def merchant_authenticity_bank_3_api(request, user):
    data = get_pay_sprint_common_payload(request, user)
    data["adhaarnumber"] = request.POST.get("merchant_aadhar_no")
    data["data"] = request.POST.get("merchant_data")
    response = make_post_request(
        url=PaySprintRoutes.BANK_2_MERCHANT_AUTHENTICITY.value, data=data
    )
    logger.error(f"Response Body: {response.json()}")
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
        merchant_auth.bank3_MerAuthTxnId = api_data.get("MerAuthTxnId")
        merchant_auth.save()
    else:
        messages.error(request, api_data.get("message"), extra_tags="danger")
    return response
    # return api_data


##########
# PAYOUT
##########


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
@transaction_required
def do_transaction(request):
    userObj = UserAccount.objects.get(username=request.user)
    bank_list = get_payout_bank_list(merchant_id=userObj.platform_id)
    activated_banks = (
        [bank for bank in bank_list if bank["status"] == "1"] if bank_list else None
    )
    document_upload_pending_banks = (
        [bank for bank in bank_list if bank["status"] == "2"] if bank_list else None
    )
    document_verification_pending_banks = (
        [bank for bank in bank_list if bank["status"] == "3"] if bank_list else None
    )

    if request.method == "POST":
        amount = 0
        ref_id = generate_unique_id()
        try:
            # Debit Payout charges before making the request
            if not debit_payout_charges(request, userObj.id, request.POST.get("amount")):
                transaction.set_rollback(True)
                return redirect("do_transaction")
            amount = float(request.POST.get("amount"))
            # commission = get_total_commission(request, userObj, amount, "Payout")
            # amount += float(commission)
            # logger.error(f"amount: {amount}")
            data = {
                "bene_id": request.POST.get("bene_id"),
                "amount": amount,
                "refid": ref_id,
                "mode": request.POST.get("mode"),
            }
            # logger.debug(f"API URL: {PaySprintRoutes.DO_TRANSACTION.value}")
            # logger.debug(f"Request Body: {data}")
            response = requests.post(
                PaySprintRoutes.DO_TRANSACTION.value,
                json=data,
                headers=get_pay_sprint_headers(),
            )
            api_data = response.json()
            # logger.debug(f"Response Body: {api_data}")

            if response.status_code == 200 and api_data.get("status"):
                messages.success(request, api_data.get("message"))
                payload = {"refid": ref_id, "ackno": api_data.get("ackno")}
                # logger.debug(f"API URL: {PaySprintRoutes.TRANSACTION_STATUS.value}")
                # logger.debug(f"Request Body: {data}")
                # Check the Transaction Status
                response = requests.post(
                    PaySprintRoutes.TRANSACTION_STATUS.value,
                    json=payload,
                    headers=get_pay_sprint_headers(),
                )
                api_data = response.json()
                # logger.debug(f"Response Body: {api_data}")

                if response.status_code == 200 and api_data.get("status"):
                    data = api_data.get("data")

                    payout_details = {
                        "userAccount": request.user,
                        "ref_id": data.get("refid"),
                        "ack_no": data.get("ackno"),
                        "bank_name": data.get("bankname"),
                        "account_no": data.get("acno"),
                        "beneficiary_name": data.get("benename"),
                        "amount": data.get("amount"),
                        "ifsc": data.get("ifsccode"),
                        "mode": data.get("mode"),
                        "charges": data.get("charges"),
                        "utr": data.get("utr"),
                        "txn_status": PAYOUT_TRANSACTION_STATUS.get(
                            data.get("txn_status")
                        ),
                    }

                    # Create a transaction entry for wallet
                    PaySprintPayout.objects.create(**payout_details)

                    return redirect("do_transaction")

            messages.error(request, api_data.get("message"), extra_tags="danger")
            transaction.set_rollback(True)
            return redirect("do_transaction")
        except Exception as e:
            messages.error(request, f"Internal server error: {e}")
            logger.error(f"error in {__name__}: {e}", exc_info=True)
            transaction.set_rollback(True)
            return redirect("do_transaction")

    context = {
        "activated_banks": activated_banks,
        "document_upload_pending_banks": document_upload_pending_banks,
        "document_verification_pending_banks": document_verification_pending_banks,
    }
    return render(request, "backend/Services/Payout/PayoutPaySprint.html", context)


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def add_bank(request):
    user = UserAccount.objects.get(username=request.user)
    if request.method == "POST":
        data = {
            "merchant_code": user.platform_id,
            "account": request.POST.get("acc_no"),
            "bankid": request.POST.get("bank_id"),
            "ifsc": request.POST.get("ifsc").upper(),
            "name": request.POST.get("acc_name"),
            "account_type": request.POST.get("acc_type"),
        }
        # logger.debug(f"API URL: {PaySprintRoutes.ADD_ACCOUNT.value}")
        # logger.debug(f"Request Body: {data}")
        response = requests.post(
            PaySprintRoutes.ADD_ACCOUNT.value,
            json=data,
            headers=get_pay_sprint_headers(),
        )
        api_data = response.json()
        # logger.debug(f"Response Body: {api_data}")
        # api_data = {'response_code': 2, 'status': True, 'acc_status': 2, 'bene_id': 1258814, 'message': 'Account Detailed saved successfully. Please upload Supportive Document to activate'}
        if api_data.get("response_code") in (1, 2):
            # if True:
            bank_acc = PaySprintPayoutBankAccountDetails.objects.filter(
                bene_id=api_data.get("bene_id")
            ).first()
            if not bank_acc:
                data.pop("merchant_code")
                bank_acc = PaySprintPayoutBankAccountDetails.objects.create(
                    bene_id=api_data.get("bene_id"), userAccount=user, **data
                )
                bank_acc.save()
            messages.success(
                request, message=api_data.get("message"), extra_tags="success"
            )
            return redirect("do_transaction")
        else:
            messages.error(request, api_data.get("message"), extra_tags="danger")

    return render(
        request,
        "backend/Services/Payout/AddBankAccPaySprint.html",
        {"bank_list": DMT_BANK_LIST},
    )


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def upload_supporting_document(request):
    user = UserAccount.objects.get(username=request.user)
    bank_list = get_payout_bank_list(merchant_id=user.platform_id)
    bene_id = request.GET.get("bene_id")
    bank_details = next(
        (
            f"{bank['name']} - {bank['bankname']} - {bank['account']} - {bank['ifsc']}"
            for bank in bank_list
            if bank.get("status") == "2" and bank.get("beneid") == bene_id
        ),
        "",
    )

    if request.method == "POST":
        doctype = request.POST.get("doctype")
        payload = {
            "doctype": doctype,
            "bene_id": bene_id,
        }

        files = {
            "passbook": (
                "panimage.jpg",
                request.FILES.get("passbook").read(),
                "image/jpeg",
            )
        }

        if doctype == "PAN":
            files["panimage"] = (
                "panimage.jpg",
                request.FILES.get("panimage").read(),
                "image/jpeg",
            )
        elif doctype == "AADHAR":
            files["front_aadhar"] = (
                "front_aadhar.jpg",
                request.FILES.get("front_aadhar").read(),
                "image/jpeg",
            )
            files["back_aadhar"] = (
                "back_aadhar.jpg",
                request.FILES.get("back_aadhar").read(),
                "image/jpeg",
            )

        # logger.debug(f"API URL: {PaySprintRoutes.UPLOAD_DOCUMENT.value}")
        # logger.debug(f"Request Body: {payload} \n Files: {files}")
        response = requests.post(
            PaySprintRoutes.UPLOAD_DOCUMENT.value,
            data=payload,
            files=files,
            headers=get_pay_sprint_headers(),
        )
        # logger.debug(f"Response Body: {response.json()}")
        if response.json().get("status"):
            messages.success(
                request, response.json().get("message"), extra_tags="success"
            )
            return redirect("do_transaction")
        else:
            messages.error(request, response.json().get("message"), extra_tags="danger")
            return redirect(reverse("upload_documents") + f"?bene_id={bene_id}")

    return render(
        request,
        "backend/Services/Payout/UploadDocumentsPaySprint.html",
        {"bank_details": bank_details, "bene_id": bene_id},
    )


def get_payout_bank_list(merchant_id):
    data = {"merchantid": merchant_id}
    # logger.debug(f"API URL: {PaySprintRoutes.GET_LIST.value}")
    # logger.debug(f"Request Body: {data}")
    response = requests.post(
        PaySprintRoutes.GET_LIST.value, json=data, headers=get_pay_sprint_headers()
    )
    # logger.debug(f"Response Body: {response.json()}")
    return response.json().get("data")


@login_required(login_url="user_login")
@user_passes_test(is_kyc_completed, login_url="unauthorized")
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def payout_report(request):
    start_date_str = request.POST.get("start_date", None)
    end_date_str = request.POST.get("end_date", None)
    page = request.GET.get("page", 1)

    try:
        update_payout_statuses(user=request.user)
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(
                end_date_str, "%Y-%m-%d"
            ).date() + timedelta(days=1)
            start_date = timezone.make_aware(
                datetime.combine(start_date, datetime.min.time())
            )
            end_date = timezone.make_aware(
                datetime.combine(end_date, datetime.max.time())
            )
            transactions = PaySprintPayout.objects.filter(
                userAccount=request.user, timestamp__range=[start_date, end_date]
            ).order_by("-id")
        else:
            transactions = PaySprintPayout.objects.filter(
                userAccount=request.user
            ).order_by("-id")

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

    context = {"transactions_page": transactions_page}
    return render(
        request, "backend/Services/Payout/Payout_Report_PaySprint.html", context
    )


@login_required(login_url='user_login')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
@user_passes_test(is_user_registered_with_paysprint, login_url="onboarding_user_paysprint")
def wallet2_commission_report(request):
    start_date_str = request.POST.get('start_date', None)
    end_date_str = request.POST.get('end_date', None)
    page = request.GET.get('page', 1)

    try:
        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
            transactions = PaySprintCommissionTxn.objects.filter(userAccount=request.user, timestamp__range=[start_date, end_date]).order_by('-id')
        else:
            transactions = PaySprintCommissionTxn.objects.filter(userAccount=request.user).order_by('-id')

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


##########
# Admin
##########


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminTxnStatus(request):
    context = {}
    if request.method == 'POST':
        update_aeps_txn_status()
        txn_type = request.POST.get('txn_type')
        reference = request.POST.get('reference')

        if txn_type == 'aadhaar_pay':
            url = PaySprintRoutes.AADHAR_PAY_TXN_STATUS.value
        else:
            url = PaySprintRoutes.CASH_WITHDRAWAL_TXN_STATUS.value

        payload = {"reference": reference}

        response = make_post_request(url=url, data=payload)

        if response.status_code == 200:
            api_data = response.json()
            status = api_data.get("status", False)
            txn_status_code = api_data.get("txnstatus", "0")
            response_code = api_data.get("response_code", 0)
            txn_status_msg = "Transaction Not found in system"

            if status and txn_status_code == "1" and response_code == 1:
                txn_status_msg = "Success"
            elif status and txn_status_code == "3" and response_code == 0:
                txn_status_msg = "Failed"
            elif status and txn_status_code == "2" and response_code == 2:
                txn_status_msg = "Pending"
            elif not status and response_code == 3:
                txn_status_msg = "Transaction Not found in system"
            else:
                txn_status_msg = "Bad request, Try again"
            
            context = {
                "data": api_data,
                "txn_status_msg": txn_status_msg,
                "reference_no": reference
            }

            logger.error(f"AdminTxnStatus 2  Response: {context}")
                
        else:
            messages.error(request, response.json().get("message"), extra_tags="danger")

    return render(request, 'backend/Admin/AdminCheckTxnStatusPaySprint.html', context)
