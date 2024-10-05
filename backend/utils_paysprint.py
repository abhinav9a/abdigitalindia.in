from decimal import Decimal
from django.db.models import F
from django.contrib import messages
import logging

from core.models import UserAccount
from backend.models import Wallet2, PaySprintCommissionCharge, PaySprintCommissionTxn, Wallet2Transaction


logger = logging.getLogger(__name__)


def get_commission_charge(service_type, amount=None):
    query = PaySprintCommissionCharge.objects.filter(service_type=service_type)
    if amount is not None:
        query = query.filter(slab_min__lte=amount, slab_max__gte=amount)
    return query.first()


def calculate_commission(base_amount=0, commission_rate=0, is_percentage=0):
    if is_percentage:
        return Decimal(base_amount) * Decimal(commission_rate/100)
    return Decimal(commission_rate)


def credit_aeps_commission(request, user_id):
    try:
        amount = request.POST.get('amount', 0)
        if not amount:
            amount = 0
        merchant = UserAccount.objects.select_for_update().get(id=user_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)
        if merchant_wallet.is_hold:
            messages.error(request, f"Wallet is on hold. Reason: {merchant_wallet.hold_reason}.", extra_tags="danger")
            return False

        # Add the amount to the merchant's wallet
        logger.error(f"credit_aeps_commission: User: {merchant} - BEFORE adding balance: {merchant_wallet.balance}")
        merchant_wallet.balance += Decimal(amount)
        merchant_wallet.save()
        logger.error(f"credit_aeps_commission: User: {merchant} - AFTER adding balance: {merchant_wallet.balance}")

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('AEPS', amount)
        if not commission_charge:
            messages.error(request, f"No commission charge found for AEPS and amount {amount}.", extra_tags="danger")
            return False

        def add_commission(user, commission, desc, agent_name):
            logger.error(f"add_commission - Commission: {commission}")
            Wallet2.objects.filter(userAccount=user).update(balance=F('balance') + commission)
            PaySprintCommissionTxn.objects.create(userAccount=user, amount=commission, txn_status="Success", desc=desc, agent_name=agent_name)

        if merchant.userType == 'Retailer':
            retailer_commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)
            add_commission(merchant, retailer_commission, "AePS Commission", "Self")

            if merchant.userManager:
                distributor = UserAccount.objects.get(id=merchant.userManager)
                if distributor.userType == 'Distributor':
                    distributor_commission = calculate_commission(amount, commission_charge.distributor_commission, commission_charge.is_percentage)
                    add_commission(distributor, distributor_commission, "AePS Commission", merchant.username)

                    if distributor.userManager:
                        master_distributor = UserAccount.objects.get(id=distributor.userManager)
                        if master_distributor.userType == 'Master Distributor':
                            master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                            add_commission(master_distributor, master_distributor_commission, "AePS Commission", merchant.username)
                elif distributor.userType == 'Master Distributor':
                    master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                    add_commission(distributor, master_distributor_commission, "AePS Commission", merchant.username)

        elif merchant.userType == 'Distributor':
            distributor_commission = calculate_commission(amount, commission_charge.distributor_commission, commission_charge.is_percentage)
            add_commission(merchant, distributor_commission, "AePS Commission", "Self")

            if merchant.userManager:
                master_distributor = UserAccount.objects.get(id=merchant.userManager)
                if master_distributor.userType == 'Master Distributor':
                    master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                    add_commission(master_distributor, master_distributor_commission, "AePS Commission", merchant.username)

        elif merchant.userType == 'Master Distributor':
            master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
            add_commission(merchant, master_distributor_commission, "AePS Commission", "Self")

        else:
            messages.error(request, f"Invalid User type: {merchant.userType}", extra_tags="danger")
            return False

        return True

    except UserAccount.DoesNotExist:
        messages.error(request, "User Not Found.", extra_tags="danger")
        return False
    except Wallet2.DoesNotExist:
        messages.error(request, "Wallet 2 Not Found.", extra_tags="danger")
        return False
    except Exception as e:
        logger.error(f"Error occurred in {__name__}: {str(e)}", exc_info=True)
        messages.error(request, "Something Went Wrong.", extra_tags="danger")
        return False


def credit_mini_statement_commission(request, merchant_id):
    try:
        merchant = UserAccount.objects.select_for_update().get(id=merchant_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)

        if merchant_wallet.is_hold:
            messages.error(request, f"Wallet is on hold. Reason: {merchant_wallet.hold_reason}.", extra_tags="danger")
            return False

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('Mini Statement')
        if not commission_charge:
            messages.error(request, "No commission charge found for Mini Statement.", extra_tags="danger")
            return False

        # Add commission to merchant's wallet only
        commission = calculate_commission(0, commission_charge.retailer_commission, commission_charge.is_percentage)
        Wallet2.objects.filter(userAccount=merchant).update(balance=F('balance') + commission)
        # Log Commission Transaction
        PaySprintCommissionTxn.objects.create(userAccount=merchant, amount=commission, txn_status="Success", desc="Mini Statement Commission", agent_name="Self")

        return True

    except UserAccount.DoesNotExist:
        messages.error(request, "User Not Found.", extra_tags="danger")
        return False
    except Wallet2.DoesNotExist:
        messages.error(request, "Wallet 2 Not Found.", extra_tags="danger")
        return False
    except Exception as e:
        logger.error(f"Error occurred in {__name__}: {str(e)}", exc_info=True)
        messages.error(request, "Something Went Wrong.", extra_tags="danger")
        return False


def debit_aadhaar_pay_charges(request, merchant_id):
    try:
        amount = request.POST.get('amount', 0)
        if not amount:
            amount = 0
        merchant = UserAccount.objects.select_for_update().get(id=merchant_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)

        if merchant_wallet.is_hold:
            messages.error(request, f"Wallet is on hold. Reason: {merchant_wallet.hold_reason}.", extra_tags="danger")
            return False

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('Aadhaar Pay')
        if not commission_charge:
            messages.error(request, "No commission charge found for Aadhaar Pay.", extra_tags="danger")
            return False

        # Calculate commission
        commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)
        logger.error(f"Aadhaar Pay=> Amoount: {amount} - Commission: {commission} - Wallet2 Balance: {merchant_wallet.balance}")
        # Check if merchant has sufficient balance
        if merchant_wallet.balance < commission:
            messages.error(request, "Insufficient balance.", extra_tags="danger")
            return False

        # Subtract amount and commission from merchant's wallet
        merchant_wallet.balance -= commission
        merchant_wallet.save()

        return True

    except UserAccount.DoesNotExist:
        messages.error(request, "User Not Found.", extra_tags="danger")
        return False
    except Wallet2.DoesNotExist:
        messages.error(request, "Wallet 2 Not Found.", extra_tags="danger")
        return False
    except Exception as e:
        logger.error(f"Error occurred in {__name__}: {str(e)}", exc_info=True)
        messages.error(request, "Something Went Wrong.", extra_tags="danger")
        return False


def debit_payout_charges(request, merchant_id, amount):
    try:
        merchant = UserAccount.objects.select_for_update().get(id=merchant_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)

        if merchant_wallet.is_hold:
            messages.error(request, f"Wallet is on hold. Reason: {merchant_wallet.hold_reason}.", extra_tags="danger")
            logger.error(f"Wallet is on hold. Reason: {merchant_wallet.hold_reason}.")
            return False

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('Payout', amount)
        if not commission_charge:
            messages.error(request, "No commission charge found for Payout", extra_tags="danger")
            logger.error("No commission charge found for Payout")
            return False

        # For Payout, we use flat_charge
        charge = commission_charge.flat_charge

        # Check if merchant has sufficient balance
        if merchant_wallet.balance < Decimal(amount) + charge:
            messages.error(request, "Insufficient balance.", extra_tags="danger")
            logger.error("Insufficient balance.")
            return False

        # Subtract amount and charge from merchant's wallet
        merchant_wallet.balance -= (Decimal(amount) + charge)
        merchant_wallet.save()

        utr = request.data.get("param").get("utr")
        ref_id = request.data.get("param").get("refid")

        # Log Transaction
        Wallet2Transaction.objects.create(
            wallet2=merchant_wallet,
            txnId=utr,
            amount=(Decimal(amount) + charge),
            txn_status='Success',
            client_ref_id=ref_id,
            description="Payout Amount and charges",
            transaction_type="Payout Deduct"
        )
        return True

    except UserAccount.DoesNotExist:
        messages.error(request, "User Not Found.", extra_tags="danger")
        return False
    except Wallet2.DoesNotExist:
        messages.error(request, "Wallet 2 Not Found.", extra_tags="danger")
        return False
    except Exception as e:
        logger.error(f"Error occurred in {__name__}: {str(e)}", exc_info=True)
        messages.error(request, "Something Went Wrong.", extra_tags="danger")
        return False


def get_total_commission(request, user, amount, service_type):
    try:
        commission_charge = Decimal(0)
        total_commission = Decimal(0)

        if service_type == 'Aadhaar Pay':
            commission_charge = get_commission_charge(service_type)
        else:
            commission_charge = get_commission_charge(service_type, amount)
        if not commission_charge:
            messages.error(request, f"No commission charge found for {service_type} and amount {amount}.", extra_tags="danger")
            return Decimal(0)


        if service_type == 'AEPS':
            if user.userType == 'Retailer':
                retailer_commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)
                total_commission += retailer_commission

                if user.userManager:
                    distributor = UserAccount.objects.get(id=user.userManager)
                    if distributor.userType == 'Distributor':
                        distributor_commission = calculate_commission(amount, commission_charge.distributor_commission, commission_charge.is_percentage)
                        total_commission += distributor_commission

                        if distributor.userManager:
                            master_distributor = UserAccount.objects.get(id=distributor.userManager)
                            if master_distributor.userType == 'Master Distributor':
                                master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                                total_commission += master_distributor_commission
                    elif distributor.userType == 'Master Distributor':
                        master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                        total_commission += master_distributor_commission

            elif user.userType == 'Distributor':
                distributor_commission = calculate_commission(amount, commission_charge.distributor_commission, commission_charge.is_percentage)
                total_commission += distributor_commission

                if user.userManager:
                    master_distributor = UserAccount.objects.get(id=user.userManager)
                    if master_distributor.userType == 'Master Distributor':
                        master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                        total_commission += master_distributor_commission

            elif user.userType == 'Master Distributor':
                master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                total_commission += master_distributor_commission

            else:
                messages.error(request, f"Invalid User type: {user.userType}", extra_tags="danger")
                return Decimal(0)
        elif service_type == 'Mini Statement':
            retailer_commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)
            total_commission += retailer_commission
        elif service_type == 'Aadhaar Pay':
            if user.userType == 'Retailer':
                retailer_commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)
                total_commission += retailer_commission
            elif user.userType == 'Distributor':
                distributor_commission = calculate_commission(amount, commission_charge.distributor_commission, commission_charge.is_percentage)
                total_commission += distributor_commission
            elif user.userType == 'Master Distributor':
                master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                total_commission += master_distributor_commission
            else:
                messages.error(request, f"Invalid User type: {user.userType}", extra_tags="danger")
                return Decimal(0)
        elif service_type == 'Payout':
            total_commission += commission_charge.flat_charge

        return total_commission

    except UserAccount.DoesNotExist:
        messages.error(request, "User Not Found.", extra_tags="danger")
        return Decimal(0)
    except Exception as e:
        logger.error(f"Error occurred in {__name__}: {str(e)}", exc_info=True)
        messages.error(request, "Something Went Wrong.", extra_tags="danger")
        return Decimal(0)