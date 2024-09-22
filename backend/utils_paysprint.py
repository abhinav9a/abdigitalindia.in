from decimal import Decimal
from django.db.models import F
from django.contrib import messages
import logging

from core.models import UserAccount
from backend.models import Wallet2, PaySprintCommissionCharge, PaySprintCommissionTxn


logger = logging.getLogger(__name__)


def get_commission_charge(service_type, amount=None):
    query = PaySprintCommissionCharge.objects.filter(service_type=service_type)
    if amount is not None:
        query = query.filter(slab_min__lte=amount, slab_max__gte=amount)
    return query.first()


def calculate_commission(base_amount, commission_rate, is_percentage):
    if is_percentage:
        return Decimal(base_amount) * (Decimal(commission_rate) / 100)
    return Decimal(commission_rate)


def credit_aeps_commission(request, user_id, amount):
    try:
        merchant = UserAccount.objects.select_for_update().get(id=user_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)

        # Add the amount to the merchant's wallet
        merchant_wallet.balance += Decimal(amount)
        merchant_wallet.save()

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('AEPS', amount)
        if not commission_charge:
            messages.error(request, f"No commission charge found for AEPS and amount {amount}.", extra_tags="danger")
            return False

        def add_commission(user, commission, desc, agent_name):
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
                elif distributor.userType == 'Master Distributor' or distributor.userType == 'Admin':
                    master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                    add_commission(distributor, master_distributor_commission, "AePS Commission", merchant.username)

        elif merchant.userType == 'Distributor':
            distributor_commission = calculate_commission(amount, commission_charge.distributor_commission, commission_charge.is_percentage)
            add_commission(merchant, distributor_commission, "AePS Commission", "Self")

            if merchant.userManager:
                master_distributor = UserAccount.objects.get(id=merchant.userManager)
                if master_distributor.userType == 'Master Distributor' or master_distributor.userType == 'Admin':
                    master_distributor_commission = calculate_commission(amount, commission_charge.master_distributor_commission, commission_charge.is_percentage)
                    add_commission(master_distributor, master_distributor_commission, "AePS Commission", merchant.username)

        elif merchant.userType in ['Master Distributor', 'Admin']:
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


def credit_mini_statement_commission(request, merchant_id, amount):
    try:
        merchant = UserAccount.objects.select_for_update().get(id=merchant_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('Mini Statement')
        if not commission_charge:
            messages.error(request, "No commission charge found for Mini Statement.", extra_tags="danger")
            return False

        # Add commission to merchant's wallet only
        commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)
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


def debit_aadhaar_pay_charges(request, merchant_id, amount):
    try:
        merchant = UserAccount.objects.select_for_update().get(id=merchant_id)
        merchant_wallet = Wallet2.objects.get(userAccount=merchant)

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('Aadhaar Pay')
        if not commission_charge:
            messages.error(request, "No commission charge found for Aadhaar Pay.", extra_tags="danger")
            return False

        # Calculate commission
        commission = calculate_commission(amount, commission_charge.retailer_commission, commission_charge.is_percentage)

        # Check if merchant has sufficient balance
        if merchant_wallet.balance < Decimal(amount) + commission:
            messages.error(request, "Insufficient balance.", extra_tags="danger")
            return False

        # Subtract amount and commission from merchant's wallet
        merchant_wallet.balance -= (Decimal(amount) + commission)
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

        # Get the appropriate commission charge
        commission_charge = get_commission_charge('Payout', amount)
        if not commission_charge:
            messages.error(request, "No commission charge found for Payout", extra_tags="danger")
            return False

        # For Payout, we use flat_charge
        charge = commission_charge.flat_charge

        # Check if merchant has sufficient balance
        if merchant_wallet.balance < Decimal(amount) + charge:
            messages.error(request, "Insufficient balance.", extra_tags="danger")
            return False

        # Subtract amount and charge from merchant's wallet
        merchant_wallet.balance -= (Decimal(amount) + charge)
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

# Usage example
def process_transaction(request, merchant_id, amount, service_type):
    if service_type == 'AEPS':
        return credit_aeps_commission(request, merchant_id, amount)
    elif service_type == 'Mini Statement':
        return credit_mini_statement_commission(request, merchant_id, amount)
    elif service_type == 'Aadhaar Pay':
        return debit_aadhaar_pay_charges(request, merchant_id, amount)
    elif service_type == 'Payout':
        return debit_payout_charges(request, merchant_id, amount)
    else:
        raise ValueError(f"Invalid service type: {service_type}")