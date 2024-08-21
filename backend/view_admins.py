from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserKYCDocument, Wallet, WalletTransaction, ServiceActivation, AepsTxnCallbackByEko, DmtTxn, PanVerificationTxn, BankVerificationTxn, Payout, BbpsTxn, CreditCardTxn
from core.models import UserAccount
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from decimal import Decimal
from django.utils import timezone
from backend.utils import is_admin_user, generate_unique_id, is_kyc_completed, is_user_onboard, is_master_distributor_access, is_distributor_access, generate_platform_id, generate_key
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.forms import CreateCustomUserForm
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
import requests


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminGetUser(request):
    try:
        username = request.GET.get('username')
        userType = request.GET.get('userType')
        userExist = UserAccount.objects.filter(userType=userType, username=username).exists()
        if userExist:
            return JsonResponse({'success': True, 'message':'available'})
        else:
            return JsonResponse({'success': False, 'message':'Not available'})

    except:
        return JsonResponse({'success': False,'message':'Internal server error'})

@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminPendingKycList(request):
    pendingKycList = UserAccount.objects.filter(
        kycStatus='P', ).exclude(userType='Admin').order_by('-id')
    return render(request, 'backend/Admin/AdminPendingKycList.html', {'pendingKycList': pendingKycList})

@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminRejectedKycList(request):
    pendingKycList = UserAccount.objects.filter(
        kycStatus='R', ).exclude(userType='Admin').order_by('-id')
    return render(request, 'backend/Admin/AdminRejectedKycList.html', {'pendingKycList': pendingKycList})


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminExplorePendingKyc(request, id):
    if request.method == 'POST':
        kycStatus = request.POST.get('kycStatus', None)
        if kycStatus is None:
            messages.error(request, 'Please select a valid choice.')
            return redirect('AdminExplorePendingKyc', id)

        obj = UserAccount.objects.get(id=id)

        if kycStatus == 'Complete':
            messages.success(request, f'KYC Completed for user {obj.username}.')
            obj.kycStatus = 'C'
        elif kycStatus == 'Rejected':
            messages.success(request, f'KYC Rejected for user {obj.username}.')
            obj.kycStatus = 'R'

        obj.save()

        return redirect('AdminPendingKycList')

    userDetails = UserAccount.objects.get(id=id)
    reviewDocumentList = UserKYCDocument.objects.filter(userAccount=id)
    return render(request, 'backend/Admin/AdminExplorePendingKyc.html', {'userDetails': userDetails, 'reviewDocumentList': reviewDocumentList})

@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminWalletAction(request):
    if request.method == 'POST':
        actionType = request.POST.get('actionType')
        userType = request.POST.get('userType')
        username = request.POST.get('username').lower()
        txnid = request.POST.get('txnid')
        amount = Decimal(request.POST.get('amount'))
        description = request.POST.get('description')

        try:
            # Check if the user exists
            user_account = UserAccount.objects.get(userType=userType, username=username)
            # Get the user's wallet
            wallet = Wallet.objects.get(userAccount=user_account)
            if actionType == 'addWallet':
                # Add amount to the wallet
                wallet.balance += amount
                wallet.save()
                # Create a transaction entry for wallet
                WalletTransaction.objects.create(wallet=wallet, txnId=txnid, amount=amount, txn_status='Success', client_ref_id=generate_unique_id(), description=description, transaction_type='Admin Deposit')
            else:
                wallet.balance -= amount
                wallet.save()
                # Create a transaction entry for wallet
                WalletTransaction.objects.create(wallet=wallet, txnId=txnid, amount=amount, txn_status='Success', client_ref_id=generate_unique_id(), description=description, transaction_type='Admin Deduct')
            
            messages.success(request, message=f'{actionType} Action for {username} Successful.', extra_tags='success')
            return redirect('AdminWalletAction')
        except UserAccount.DoesNotExist:
            messages.error(request, message='User Not Found, Please Check Details', extra_tags='danger')
            return redirect('AdminWalletAction')
        
        except Wallet.DoesNotExist:
            messages.error(request, message='User Wallet Not Found', extra_tags='danger')
            return redirect('AdminWalletAction')

    return render(request, 'backend/Admin/AdminWalletAction.html')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
def allRetailers(request):
    current_user = UserAccount.objects.get(username=request.user)
    if current_user.groups.filter(name='Admin').exists():
        retailers = UserAccount.objects.filter(userType='Retailer', groups__name='Retailer').exclude(Q(kycStatus='P') | Q(kycStatus='R')).order_by('-id')
    else:
        retailers = UserAccount.objects.filter(userType='Retailer', userManager=request.user.id, groups__name='Retailer').exclude(Q(kycStatus='P') | Q(kycStatus='R')).order_by('-id')
    return render(request, 'backend/Admin/AdminAllRetailers.html', {'retailers': retailers})

@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
def create_retailer(request):
    if request.method == 'POST':
        form = CreateCustomUserForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            username = form.cleaned_data.get('username').lower()
            pancard_no = form.cleaned_data.get('pancard_no').upper()
            newUser.username = username
            newUser.pancard_no = pancard_no.upper()
            newUser.userManager = request.user.id
            newUser.is_active = True
            newUser.userType = 'Retailer'

            serial_number, platform_id = generate_platform_id(newUser.userType)       
            newUser.unique_sequence = serial_number
            newUser.platform_id = platform_id

            newUser.save()

            defaultGroup = Group.objects.get(name=newUser.userType)
            newUser.groups.add(defaultGroup)

            messages.success(request, 'Retailer Created, Ask them to complete their KYC.')
            return redirect('allRetailers')
    else:
        form = CreateCustomUserForm()
    return render(request, 'backend/Admin/AdminCreateRetailer.html', {'form': form})


@login_required(login_url='user_login')
@user_passes_test(is_master_distributor_access, login_url='unauthorized')
def allDistributors(request):
    current_user = UserAccount.objects.get(username=request.user)
    if current_user.groups.filter(name='Admin').exists():
        distributors = UserAccount.objects.filter(userType='Distributor', groups__name='Distributor').exclude(Q(kycStatus='P') | Q(kycStatus='R')).order_by('-id')
    else:
        distributors = UserAccount.objects.filter(userType='Distributor', userManager=request.user.id, groups__name='Distributor').exclude(Q(kycStatus='P') | Q(kycStatus='R')).order_by('-id')

    return render(request, 'backend/Admin/AdminAllDistributors.html', {'distributors': distributors})


@login_required(login_url='user_login')
@user_passes_test(is_master_distributor_access, login_url='unauthorized')
def create_distributor(request):
    if request.method == 'POST':
        form = CreateCustomUserForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            username = form.cleaned_data.get('username').lower()
            pancard_no = form.cleaned_data.get('pancard_no').upper()
            newUser.username = username
            newUser.pancard_no = pancard_no.upper()
            newUser.userManager = request.user.id
            newUser.is_active = True
            newUser.userType = 'Distributor'

            serial_number, platform_id = generate_platform_id(newUser.userType)       
            newUser.unique_sequence = serial_number
            newUser.platform_id = platform_id

            newUser.save()

            defaultGroup = Group.objects.get(name=newUser.userType)
            newUser.groups.add(defaultGroup)

            messages.success(request, 'Distributor Created, Ask them to complete their KYC.')
            return redirect('allDistributors')
    else:
        form = CreateCustomUserForm()
    return render(request, 'backend/Admin/AdminCreateDistributor.html', {'form': form})


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def allMasterDistributors(request):
    current_user = UserAccount.objects.get(username=request.user)
    if current_user.groups.filter(name='Admin').exists():
        md = UserAccount.objects.filter(userType='Master Distributor', groups__name='Master Distributor').exclude(Q(kycStatus='P') | Q(kycStatus='R')).order_by('-id')
    else:
        md = UserAccount.objects.filter(userType='Master Distributor', userManager=request.user.id, groups__name='Master Distributor').exclude(Q(kycStatus='P') | Q(kycStatus='R')).order_by('-id')
    return render(request, 'backend/Admin/AdminAllMDs.html', {'md': md})


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def create_master_distributor(request):
    if request.method == 'POST':
        form = CreateCustomUserForm(request.POST)
        if form.is_valid():
            newUser = form.save(commit=False)
            username = form.cleaned_data.get('username').lower()
            pancard_no = form.cleaned_data.get('pancard_no').upper()
            newUser.username = username
            newUser.pancard_no = pancard_no.upper()
            newUser.userManager = request.user.id
            newUser.is_active = True
            newUser.userType = 'Master Distributor'

            serial_number, platform_id = generate_platform_id(newUser.userType)       
            newUser.unique_sequence = serial_number
            newUser.platform_id = platform_id

            newUser.save()

            defaultGroup = Group.objects.get(name=newUser.userType)
            newUser.groups.add(defaultGroup)

            messages.success(request, 'Master Distributor Created, Ask them to complete their KYC.')
            return redirect('allMasterDistributors')
    else:
        form = CreateCustomUserForm()
    return render(request, 'backend/Admin/AdminCreateMD.html', {'form': form})


@login_required(login_url='user_login')
def AdminExploreUser(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        user = UserAccount.objects.get(id=id)
        wallet = Wallet.objects.get_or_create(userAccount=user)[0]
        kycDoc = UserKYCDocument.objects.get(userAccount=id)
        return render(request, 'backend/Admin/AdminExploreUser.html', {'user': user, 'kycDoc':kycDoc, "wallet":wallet})
    else:
        return redirect('unauthorized')


# Reports
@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExploreAepsReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = AepsTxnCallbackByEko.objects.filter(userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = AepsTxnCallbackByEko.objects.filter(userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExploreAepsReport.html', context)
    else:
        return redirect('unauthorized')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExploreDmtReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = DmtTxn.objects.filter(wallet__userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = DmtTxn.objects.filter(wallet__userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExploreDmtReport.html', context)
    else:
        return redirect('unauthorized')

@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExploreWalletReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = WalletTransaction.objects.filter(wallet__userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = WalletTransaction.objects.filter(wallet__userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExploreWalletReport.html', context)
    else:
        return redirect('unauthorized')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExplorePanVerificationReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = PanVerificationTxn.objects.filter(wallet__userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = PanVerificationTxn.objects.filter(wallet__userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExplorePanVerificationReport.html', context)
    else:
        return redirect('unauthorized')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExploreBankVerificationReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = BankVerificationTxn.objects.filter(wallet__userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = BankVerificationTxn.objects.filter(wallet__userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExploreBankVerificationReport.html', context)
    else:
        return redirect('unauthorized')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExplorePayoutReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = Payout.objects.filter(userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = Payout.objects.filter(userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExplorePayoutReport.html', context)
    else:
        return redirect('unauthorized')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExploreBBPSReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = BbpsTxn.objects.filter(userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = BbpsTxn.objects.filter(userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExploreBBPSReport.html', context)
    else:
        return redirect('unauthorized')


@login_required(login_url='user_login')
@user_passes_test(is_distributor_access, login_url='unauthorized')
@user_passes_test(is_kyc_completed, login_url='unauthorized')
def AdminExploreCreditCardReport(request, id):
    current_user = UserAccount.objects.get(username=request.user)
    sub_current_user = UserAccount.objects.get(id=id)

    if sub_current_user.userManager == str(current_user.id) or current_user.groups.filter(name='Admin').exists():
        start_date_str = request.POST.get('start_date', None)
        end_date_str = request.POST.get('end_date', None)
        page = request.GET.get('page', 1)

        try:
            if start_date_str and end_date_str:
                start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
                start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                transactions = CreditCardTxn.objects.filter(wallet__userAccount=id, timestamp__range=[start_date, end_date]).order_by('-id')
            else:
                transactions = CreditCardTxn.objects.filter(wallet__userAccount=id).order_by('-id')

        except ValueError as e:
            messages.error(request, str(e))
            transactions = []

        paginator = Paginator(transactions, 20)

        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        context = {'transactions_page': transactions_page}
        return render(request, 'backend/Admin/Reports/AdminExploreCreditCardReport.html', context)
    else:
        return redirect('unauthorized')



@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminTxnStatus(request):
    api_data = None
    if request.method == 'POST':
        secret_key, secret_key_timestamp = generate_key()

        id_type = request.POST.get('id_type')
        txnid = request.POST.get('txnid')

        if id_type == 'tid':
            url = f"https://api.eko.in/ekoicici/v1/transactions/{txnid}?initiator_id=9568855837"
        else:
            url = f"https://api.eko.in/ekoicici/v1/transactions/client_ref_id:{txnid}?initiator_id=9568855837"

        payload = {}
        headers = {
            'developer_key': '552d8d5d982965b60f8fb4c618f95f4e',
            'secret-key': secret_key,
            'secret-key-timestamp': secret_key_timestamp
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        api_data = response.json()
        print(response.text)

    return render(request, 'backend/Admin/AdminCheckTxnStatus.html', {'api_data': api_data})


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def balance_sheet(request, id):
    user = UserAccount.objects.get(id=id)
    walletObj = Wallet.objects.get(userAccount=user)

    '''
    Pending Txns from DMT, Aeps, BBPS
    Credit from Aeps, Commission, Wallet
    Debit from DMT, Payout, Pan Verification, Bank Verification, BBPS
    '''

    dmt_txn_pending = DmtTxn.objects.filter(wallet=walletObj).exclude(txn_status__in=["Success", "Fail"])
    aeps_txn_pending = AepsTxnCallbackByEko.objects.filter(userAccount=user).exclude(tx_status__in=["Success", "Failed"])
    bbps_txn_pending = BbpsTxn.objects.filter(userAccount=user).exclude(txstatus_desc__in=["Success", "Fail", "Refunded"])
    payout_txn_pending = Payout.objects.filter(userAccount=user).exclude(txn_status__in=["Success", "Fail", "Refunded"])

    context = {
        "user": user,
        "dmt_txn_pending": dmt_txn_pending,
        "dmt_txn_pending_count": dmt_txn_pending.count(),
        "aeps_txn_pending": aeps_txn_pending,
        "aeps_txn_pending_count": aeps_txn_pending.count(),
        "bbps_txn_pending": bbps_txn_pending,
        "bbps_txn_pending_count": bbps_txn_pending.count(),
        "payout_txn_pending": payout_txn_pending,
        "payout_txn_pending_count": payout_txn_pending.count(),
    }

    return render(request, 'backend/Admin/BalanceSheet.html', {"context": context})


@login_required(login_url='user_login')
@user_passes_test(is_admin_user, login_url='unauthorized')
def AdminChangeUserPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        newPassword1 = request.POST.get('newPassword1')
        newPassword2 = request.POST.get('newPassword2')
        
        if newPassword1 == newPassword2:
            usr = UserAccount.objects.get(username=username)
            usr.set_password(newPassword1)
            usr.save()
            messages.success(request, 'Password Changed successfully.', extra_tags='success')
        else:
            messages.error(request, 'Password do not match.', extra_tags='danger')

    return render(request, 'backend/Admin/AdminUserPasswordChange.html')