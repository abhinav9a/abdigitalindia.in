import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from core.models import UserAccount
from django.dispatch import receiver

class DMTBankList(models.Model):
    bank_name = models.CharField(max_length=255)
    bank_id = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.bank_name
    
    @classmethod
    def create_from_excel(cls, excel_file_path):
        import pandas as pd

        # Read the Excel file, skip the first row (header)
        df = pd.read_excel(excel_file_path)

        # Iterate through rows and create Bank objects
        banks = []
        for _, row in df[::-1].iterrows():
            bank = cls(bank_id=row[' BankID '], bank_name=row[' BANK_NAME                                                                 '], bank_code=row['BANK CODE'],)
            banks.append(bank)

        # Bulk create the Bank objects
        cls.objects.bulk_create(banks)
        

def document_file_path(instance, filename):
    base_path = 'media/KycDocuments'
    username = instance.userAccount.username
    timestamp_now = timezone.now().strftime('%Y%m%d%H%M%S')
    cleaned_filename = f"{slugify(os.path.splitext(filename)[0])}_{timestamp_now}{os.path.splitext(filename)[1]}"
    user_folder = os.path.join(base_path, username)
    return os.path.join(user_folder, cleaned_filename)


class UserKYCDocument(models.Model):
    userAccount = models.OneToOneField(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    aadharFront = models.FileField(_("Aadhar Front"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    aadharBack = models.FileField(_("Aadhar Back"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    pancard = models.FileField(_("Pancard"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    cancelChequePassbook = models.FileField(_("Cancel Cheque/Passbook"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    declarationForm = models.FileField(_("Self Declaration Form"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    photo = models.FileField(_("Passport Size Photo"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    policeVerification = models.FileField(_("Police Verification"), upload_to=document_file_path, max_length=100, null=True, blank=True)
    documentComment = models.CharField(_("Document Comment"), max_length=150, null=True, blank=True)

    def __str__(self):
        return self.userAccount.username


class ServiceActivation(models.Model):
    userAccount = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    QrPaymentService = models.BooleanField(
        _("QR Payment Status"), default=False)
    AepsService = models.BooleanField(_("AEPS Status"), default=False)

    def __str__(self):
        return self.userAccount.username


def other_service_file_path(instance, filename):
    print(instance, filename)
    base_path = 'media/otherServices'
    username = instance.userAccount.username
    timestamp_now = timezone.now().strftime('%Y%m%d%H%M%S')
    cleaned_filename = f"{slugify(os.path.splitext(filename)[0])}_{timestamp_now}{os.path.splitext(filename)[1]}"
    user_folder = os.path.join(base_path, username)
    return os.path.join(user_folder, cleaned_filename)

class OtherServices(models.Model):
    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=100, blank=True)
    gender = models.CharField(_("Gender"), max_length=100, blank=True)
    father_name = models.CharField(_("Father's name"), max_length=100, blank=True)
    dob = models.CharField(_("DOB"), max_length=100, blank=True)
    address = models.CharField(_("Address"), max_length=100, blank=True)
    mobile = models.CharField(_("Mobile"), max_length=100, blank=True)
    email = models.CharField(_("Email"), max_length=100, blank=True)
    adhaar = models.CharField(_("Adhaar"), max_length=100, blank=True)
    pan = models.CharField(_("pan"), max_length=100, blank=True)
    serviceName = models.CharField(_("Service Name"), max_length=150)
    serviceDescription = models.CharField(_("Service Description"), max_length=150)
    doc1 = models.FileField(_("Supporting Document 1"), upload_to=other_service_file_path, max_length=100, blank=True)
    doc2 = models.FileField(_("Supporting Document 2"), upload_to=other_service_file_path, max_length=100, blank=True)
    doc3 = models.FileField(_("Supporting Document 3"), upload_to=other_service_file_path, max_length=100, blank=True)
    doc4 = models.FileField(_("Supporting Document 4"), upload_to=other_service_file_path, max_length=100, blank=True)


    def __str__(self):
        return self.serviceName


class OtherServices2(models.Model):
    serviceName = models.CharField(_("Service Name"), max_length=150)
    serviceUrl = models.CharField(_("Service URL"), max_length=500)

    def __str__(self):
        return self.serviceName


class Wallet(models.Model):
    userAccount = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.userAccount.username


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    txnId = models.CharField(_("Bank Transaction Id"), max_length=500, blank=True)
    client_ref_id = models.CharField(_("Client Ref Id"), max_length=500, blank=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(_("Transaction Type"), max_length=500, null=True, blank=True)
    txn_status = models.CharField(_("Transaction Status"), max_length=500, blank=True)

    def __str__(self):
        return str(self.amount)
    

class DmtTxn(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txn_status = models.CharField(_("Transaction Status"), max_length=500, blank=True)
    sender_name = models.CharField(_("Sender Name"), max_length=500, blank=True)
    txnId = models.CharField(_("Bank Transaction Id"), max_length=500, blank=True)
    bank = models.CharField(_("Bank Name"), max_length=500, blank=True)
    currency = models.CharField(_("Currency"), max_length=500, blank=True)
    bank_ref_num = models.CharField(_("Bank Ref Num"), max_length=500, blank=True)
    recipient_id = models.CharField(_("Recipient Id"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    channel_desc = models.CharField(_("Channel Desc"), max_length=500, blank=True)
    client_ref_id = models.CharField(_("Client Ref Id"), max_length=500, blank=True)
    recipient_name = models.CharField(_("Recipient Name"), max_length=500, blank=True)
    customer_id = models.CharField(_("Customer Id"), max_length=500, blank=True)
    account = models.CharField(_("Account Number"), max_length=500, blank=True)
    description = models.CharField(max_length=255)
    commission = models.CharField(_("DMT Commission"), max_length=500, blank=True)


class CreditCardTxn(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txn_status = models.CharField(_("Transaction Status"), max_length=500, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender_name = models.CharField(_("Sender Name"), max_length=500, blank=True)
    txnId = models.CharField(_("Bank Transaction Id"), max_length=500, blank=True)
    client_ref_id = models.CharField(_("Client Ref Id"), max_length=500, blank=True)
    recipient_name = models.CharField(_("Recipient Name"), max_length=500, blank=True)
    ifsc = models.CharField(_("IFSC"), max_length=500, blank=True)
    bank_ref_num = models.CharField(_("Bank Ref Num"), max_length=500, blank=True)
    account = models.CharField(_("Account Number"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    # commission = models.CharField(_("Credit Card Commission"), max_length=500, blank=True)

    def __str__(self):
        return str(self.amount)
    

class BankVerificationTxn(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    txnId = models.CharField(_("Bank Transaction Id"), max_length=500, blank=True)
    client_ref_id = models.CharField(_("Client Ref Id"), max_length=500, blank=True)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    txn_status = models.CharField(_("Transaction Status"), max_length=500, blank=True)

    def __str__(self):
        return str(self.amount)
    

class PanVerificationTxn(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    txn_status = models.CharField(_("Transaction Status"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class AdhaarVerificationTxn(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    txn_status = models.CharField(_("Transaction Status"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class QRTxnCallbackByEko(models.Model):
    # tx_status = models.CharField(_("tx_status"), max_length=50)
    # amount = models.CharField(_("amount"), max_length=50)
    # tds = models.CharField(_("tds"), max_length=50)
    # txstatus_desc = models.CharField(_("txstatus_desc"), max_length=50)
    # fee = models.CharField(_("fee"), max_length=50)
    # gst = models.CharField(_("gst"), max_length=50)
    # tid = models.CharField(_("tid"), max_length=50)
    # client_ref_id = models.CharField(_("client_ref_id"), max_length=50)
    # old_tx_status = models.CharField(_("old_tx_status"), max_length=50)
    # partners_commision = models.CharField(
    #     _("partners_commision"), max_length=50)
    # service_code = models.CharField(_("service_code"), max_length=50)
    # old_tx_status_desc = models.CharField(
    #     _("old_tx_status_desc"), max_length=50)
    # bank_ref_num = models.CharField(_("bank_ref_num"), max_length=50)
    # timestamp = models.CharField(_("timestamp"), max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    txn_detail = models.JSONField(_("Transaction JSON"))

    def save(self, *args, **kwargs):
        if not self.timestamp:
            # Set the timestamp to the current time in the default time zone
            self.timestamp = timezone.now()

        super().save(*args, **kwargs)


class BbpsTxn(models.Model):
    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    txstatus_desc = models.CharField(_("txstatus_desc"), max_length=50, blank=True)
    utilitycustomername = models.CharField(_("utilitycustomername"), max_length=50, blank=True)
    tid = models.CharField(_("tid"), max_length=50, blank=True)
    sender_id = models.CharField(_("sender_id"), max_length=50, blank=True)
    recipient_id = models.CharField(_("recipient_id"), max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(_("amount"), max_length=50, blank=True)
    customermobilenumber = models.CharField(_("customermobilenumber"), max_length=50, blank=True)
    operator_name = models.CharField(_("operator_name"), max_length=50, blank=True)
    totalamount = models.CharField(_("totalamount"), max_length=50, blank=True)
    approvalreferencenumber = models.CharField(_("approvalreferencenumber"), max_length=50, blank=True)
    account = models.CharField(_("account"), max_length=50, blank=True)

    def __str__(self):
        return self.amount


class AepsTxnCallbackByEko(models.Model):

    class Tx_Status(models.TextChoices):
        Pending = "P", _("Pending")
        Success = "0", _("Success")
        Failed = "1", _("Failed")
        Do_Inquiry = "2", _("Do_Inquiry")
        Suspicious = "other", _("Suspicious")
    
    class Service_Type(models.TextChoices):
        Cash_Withdrawal = "2", _("Cash Withdrawal")
        Balance_Inquiry = "3", _("Balance Inquiry")
        Mini_Statement = "4", _("Mini Statement")

    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    tx_status = models.CharField(max_length=20, choices=Tx_Status.choices)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2, blank=True, default=0.0)
    commission = models.DecimalField(_("Commission"), max_digits=10, decimal_places=2, blank=True, default=0.0)
    client_ref_id = models.CharField(_("client_ref_id"), max_length=500)
    tid = models.CharField(_("tid"), max_length=500, blank=True)
    aadhar_no = models.CharField(_("aadhar_no"), max_length=500, blank=True)
    service_type = models.CharField(max_length=20, choices=Service_Type.choices)
    txn_detail = models.JSONField(_("Transaction JSON"))
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            # Set the timestamp to the current time in the default time zone
            self.timestamp = timezone.now()

        super().save(*args, **kwargs)
    
    def get_status_display(self):
        return dict(AepsTxnCallbackByEko.Tx_Status.choices).get(self.tx_status, '')

    def get_service_display(self):
        return dict(AepsTxnCallbackByEko.Service_Type.choices).get(self.service_type, '')


class CMSTxnCallbackByEko(models.Model):
    # userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    # tx_status = models.CharField(max_length=20, blank=True)
    # amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2, blank=True, default=0.0)
    # client_ref_id = models.CharField(_("client_ref_id"), max_length=500)
    # tid = models.CharField(_("tid"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # commission = models.DecimalField(_("Commission"), max_digits=10, decimal_places=2, blank=True, default=0.0)
    txn_detail = models.JSONField(_("Transaction JSON"))

    def save(self, *args, **kwargs):
        if not self.timestamp:
            # Set the timestamp to the current time in the default time zone
            self.timestamp = timezone.now()

        super().save(*args, **kwargs)


class Commission(models.Model):
    userAccount = models.OneToOneField(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)

    # Aeps Commission Slab
    AepsCommissionSlab1 = models.DecimalField(_("Aeps 100-199 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlab2 = models.DecimalField(_("Aeps 200-999 (Rs)"), max_digits=5, decimal_places=2, default=0.50)
    AepsCommissionSlab3 = models.DecimalField(_("Aeps 1000-1499 (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    AepsCommissionSlab4 = models.DecimalField(_("Aeps 1500-1999 (Rs)"), max_digits=5, decimal_places=2, default=3.0)
    AepsCommissionSlab5 = models.DecimalField(_("Aeps 2000-2499 (Rs)"), max_digits=5, decimal_places=2, default=4.0)
    AepsCommissionSlab6 = models.DecimalField(_("Aeps 2500-2999 (Rs)"), max_digits=5, decimal_places=2, default=5.0)
    AepsCommissionSlab7 = models.DecimalField(_("Aeps 3000-7999 (Rs)"), max_digits=5, decimal_places=2, default=7.0)
    AepsCommissionSlab8 = models.DecimalField(_("Aeps 8000 & above (Rs)"), max_digits=5, decimal_places=2, default=10.0)

    AepsCommissionSlabDistributor1 = models.DecimalField(_("Distributor Aeps 100-199 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlabDistributor2 = models.DecimalField(_("Distributor Aeps 200-999 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlabDistributor3 = models.DecimalField(_("Distributor Aeps 1000-1499 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlabDistributor4 = models.DecimalField(_("Distributor Aeps 1500-1999 (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    AepsCommissionSlabDistributor5 = models.DecimalField(_("Distributor Aeps 2000-2499 (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    AepsCommissionSlabDistributor6 = models.DecimalField(_("Distributor Aeps 2500-2999 (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    AepsCommissionSlabDistributor7 = models.DecimalField(_("Distributor Aeps 3000-7999 (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    AepsCommissionSlabDistributor8 = models.DecimalField(_("Distributor Aeps 8000 & above (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    
    AepsCommissionSlabMaster1 = models.DecimalField(_("Master Distributor Aeps 100-199 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlabMaster2 = models.DecimalField(_("Master Distributor Aeps 200-999 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlabMaster3 = models.DecimalField(_("Master Distributor Aeps 1000-1499 (Rs)"), max_digits=5, decimal_places=2, default=0.0)
    AepsCommissionSlabMaster4 = models.DecimalField(_("Master Distributor Aeps 1500-1999 (Rs)"), max_digits=5, decimal_places=2, default=0.50)
    AepsCommissionSlabMaster5 = models.DecimalField(_("Master Distributor Aeps 2000-2499 (Rs)"), max_digits=5, decimal_places=2, default=0.50)
    AepsCommissionSlabMaster6 = models.DecimalField(_("Master Distributor Aeps 2500-2999 (Rs)"), max_digits=5, decimal_places=2, default=0.50)
    AepsCommissionSlabMaster7 = models.DecimalField(_("Master Distributor Aeps 3000-7999 (Rs)"), max_digits=5, decimal_places=2, default=0.50)
    AepsCommissionSlabMaster8 = models.DecimalField(_("Master Distributor Aeps 8000 & above (Rs)"), max_digits=5, decimal_places=2, default=0.50)

    # DMT Commission Slab
    DmtCommission = models.DecimalField(_("DMT %"), max_digits=5, decimal_places=2, default=0.0)

    # BBPS Commission Slab Fixed HCC=0
    BbpsInstantElectricity = models.DecimalField(_("Electricity (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    BbpsInstantLoan = models.DecimalField(_("Loan (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    BbpsInstantRechargePrepaid = models.DecimalField(_("Recharge Prepaid (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    BbpsInstantRechargePostpaid = models.DecimalField(_("Recharge Postpaid (Rs)"), max_digits=5, decimal_places=2, default=1.0)
    BbpsInstantDTH = models.DecimalField(_("DTH (Rs)"), max_digits=5, decimal_places=2, default=1.0)

    BbpsInstantElectricityDistributor = models.DecimalField(_("Distributor Electricity (Rs)"), max_digits=5, decimal_places=2, default=0.30)
    BbpsInstantLoanDistributor = models.DecimalField(_("Distributor Loan (Rs)"), max_digits=5, decimal_places=2, default=0.30)
    BbpsInstantRechargePrepaidDistributor = models.DecimalField(_("Distributor Recharge Prepaid (Rs)"), max_digits=5, decimal_places=2, default=0.30)
    BbpsInstantRechargePostpaidDistributor = models.DecimalField(_("Distributor Recharge Postpaid (Rs)"), max_digits=5, decimal_places=2, default=0.30)
    BbpsInstantDTHDistributor = models.DecimalField(_("Distributor DTH (Rs)"), max_digits=5, decimal_places=2, default=0.30)

    BbpsInstantElectricityMaster = models.DecimalField(_("Master Distributor Electricity (Rs)"), max_digits=5, decimal_places=2, default=0.20)
    BbpsInstantLoanMaster = models.DecimalField(_("Master Distributor Loan (Rs)"), max_digits=5, decimal_places=2, default=0.20)
    BbpsInstantRechargePrepaidMaster = models.DecimalField(_("Master Distributor Recharge Prepaid (Rs)"), max_digits=5, decimal_places=2, default=0.20)
    BbpsInstantRechargePostpaidMaster = models.DecimalField(_("Master Distributor Recharge Postpaid (Rs)"), max_digits=5, decimal_places=2, default=0.20)
    BbpsInstantDTHMaster = models.DecimalField(_("Master Distributor DTH (Rs)"), max_digits=5, decimal_places=2, default=0.20)

    # BBPS Commission Slab HCC=1
    # Electricity
    BbpsHCElectricitySlab1 = models.DecimalField(_("High Commission Electricity 0-1000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCElectricitySlab2 = models.DecimalField(_("High Commission Electricity 1001-2000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCElectricitySlab3 = models.DecimalField(_("High Commission Electricity 2001-10000 (%)"), max_digits=10, decimal_places=2, default=0.15)
    BbpsHCElectricitySlab4 = models.DecimalField(_("High Commission Electricity 10001-15000 (%)"), max_digits=10, decimal_places=2, default=0.15)
    BbpsHCElectricitySlab5 = models.DecimalField(_("High Commission Electricity 15001-25000 (%)"), max_digits=10, decimal_places=2, default=0.20)
    BbpsHCElectricitySlab6 = models.DecimalField(_("High Commission Electricity 25001-100000 (%)"), max_digits=10, decimal_places=2, default=0.20)
    BbpsHCElectricitySlab7 = models.DecimalField(_("High Commission Electricity 100001-2L (%)"), max_digits=10, decimal_places=2, default=0.20)

    BbpsHCElectricitySlabDistributor1 = models.DecimalField(_("High Commission Distributor Electricity 0-1000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCElectricitySlabDistributor2 = models.DecimalField(_("High Commission Distributor Electricity 1001-2000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCElectricitySlabDistributor3 = models.DecimalField(_("High Commission Distributor Electricity 2001-10000 (%)"), max_digits=10, decimal_places=2, default=0.04)
    BbpsHCElectricitySlabDistributor4 = models.DecimalField(_("High Commission Distributor Electricity 10001-15000 (%)"), max_digits=10, decimal_places=2, default=0.04)
    BbpsHCElectricitySlabDistributor5 = models.DecimalField(_("High Commission Distributor Electricity 15001-25000 (%)"), max_digits=10, decimal_places=2, default=0.05)
    BbpsHCElectricitySlabDistributor6 = models.DecimalField(_("High Commission Distributor Electricity 25001-100000 (%)"), max_digits=10, decimal_places=2, default=0.05)
    BbpsHCElectricitySlabDistributor7 = models.DecimalField(_("High Commission Distributor Electricity 100001-2L (%)"), max_digits=10, decimal_places=2, default=0.05)

    BbpsHCElectricitySlabMaster1 = models.DecimalField(_("High Commission Master Electricity 0-1000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCElectricitySlabMaster2 = models.DecimalField(_("High Commission Master Electricity 1001-2000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCElectricitySlabMaster3 = models.DecimalField(_("High Commission Master Electricity 2001-10000 (%)"), max_digits=10, decimal_places=2, default=0.04)
    BbpsHCElectricitySlabMaster4 = models.DecimalField(_("High Commission Master Electricity 10001-15000 (%)"), max_digits=10, decimal_places=2, default=0.04)
    BbpsHCElectricitySlabMaster5 = models.DecimalField(_("High Commission Master Electricity 15001-25000 (%)"), max_digits=10, decimal_places=2, default=0.05)
    BbpsHCElectricitySlabMaster6 = models.DecimalField(_("High Commission Master Electricity 25001-100000 (%)"), max_digits=10, decimal_places=2, default=0.05)
    BbpsHCElectricitySlabMaster7 = models.DecimalField(_("High Commission Master Electricity 100001-2L (%)"), max_digits=10, decimal_places=2, default=0.05)

    # Water n Gas
    BbpsHCWaterNGasSlab1 = models.DecimalField(_("High Commission Water & Piped Gas Bill 0-1000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCWaterNGasSlab2 = models.DecimalField(_("High Commission Water & Piped Gas Bill 1001-10000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCWaterNGasSlab3 = models.DecimalField(_("High Commission Water & Piped Gas Bill 10001-15000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCWaterNGasSlab4 = models.DecimalField(_("High Commission Water & Piped Gas Bill 15001-25000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCWaterNGasSlab5 = models.DecimalField(_("High Commission Water & Piped Gas Bill 25001-100000 (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCWaterNGasSlab6 = models.DecimalField(_("High Commission Water & Piped Gas Bill 100001-2L (%)"), max_digits=10, decimal_places=2, default=0.10)

    BbpsHCWaterNGasSlabDistributor1 = models.DecimalField(_("High Commission Distributor Water & Piped Gas Bill 0-1000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCWaterNGasSlabDistributor2 = models.DecimalField(_("High Commission Distributor Water & Piped Gas Bill 1001-10000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCWaterNGasSlabDistributor3 = models.DecimalField(_("High Commission Distributor Water & Piped Gas Bill 10001-15000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCWaterNGasSlabDistributor4 = models.DecimalField(_("High Commission Distributor Water & Piped Gas Bill 15001-25000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCWaterNGasSlabDistributor5 = models.DecimalField(_("High Commission Distributor Water & Piped Gas Bill 25001-100000 (%)"), max_digits=10, decimal_places=2, default=0.03)
    BbpsHCWaterNGasSlabDistributor6 = models.DecimalField(_("High Commission Distributor Water & Piped Gas Bill 100001-2L (%)"), max_digits=10, decimal_places=2, default=0.03)

    BbpsHCWaterNGasSlabMaster1 = models.DecimalField(_("High Commission Master Water & Piped Gas Bill 0-1000 (%)"), max_digits=10, decimal_places=2, default=0.02)
    BbpsHCWaterNGasSlabMaster2 = models.DecimalField(_("High Commission Master Water & Piped Gas Bill 1001-10000 (%)"), max_digits=10, decimal_places=2, default=0.02)
    BbpsHCWaterNGasSlabMaster3 = models.DecimalField(_("High Commission Master Water & Piped Gas Bill 10001-15000 (%)"), max_digits=10, decimal_places=2, default=0.02)
    BbpsHCWaterNGasSlabMaster4 = models.DecimalField(_("High Commission Master Water & Piped Gas Bill 15001-25000 (%)"), max_digits=10, decimal_places=2, default=0.02)
    BbpsHCWaterNGasSlabMaster5 = models.DecimalField(_("High Commission Master Water & Piped Gas Bill 25001-100000 (%)"), max_digits=10, decimal_places=2, default=0.02)
    BbpsHCWaterNGasSlabMaster6 = models.DecimalField(_("High Commission Master Water & Piped Gas Bill 100001-2L (%)"), max_digits=10, decimal_places=2, default=0.02)

    # Mobile Recharge Postpaid
    BbpsHCMobilePostpaid = models.DecimalField(_("High Commission Mobile Postpaid & Fixed Landline - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.15)
    BbpsHCMobilePostpaidDistributor = models.DecimalField(_("High Commission Distributor Mobile Postpaid & Fixed Landline - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.05)
    BbpsHCMobilePostpaidMaster = models.DecimalField(_("High Commission Master Mobile Postpaid & Fixed Landline - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.05)

    # Mobile Recharge Prepaid Individually
    BbpsHCAirtelMobilePrepaid = models.DecimalField(_("High Commission Airtel Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=1.0)
    BbpsHCBSNLMobilePrepaid = models.DecimalField(_("High Commission BSNL Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=1.0)
    BbpsHCJioMobilePrepaid = models.DecimalField(_("High Commission JIO Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=1.0)
    BbpsHCVIMobilePrepaid = models.DecimalField(_("High Commission VI Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=1.0)
    BbpsHCMTNLMobilePrepaid = models.DecimalField(_("High Commission MTNL Delhi & Mumbai Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=1.0)

    BbpsHCAirtelMobilePrepaidDistributor = models.DecimalField(_("High Commission Distributor Airtel Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCBSNLMobilePrepaidDistributor = models.DecimalField(_("High Commission Distributor BSNL Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCJioMobilePrepaidDistributor = models.DecimalField(_("High Commission Distributor JIO Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCVIMobilePrepaidDistributor = models.DecimalField(_("High Commission Distributor VI Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCMTNLMobilePrepaidDistributor = models.DecimalField(_("High Commission Distributor MTNL Delhi & Mumbai Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    
    BbpsHCAirtelMobilePrepaidMaster = models.DecimalField(_("High Commission Master Airtel Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCBSNLMobilePrepaidMaster = models.DecimalField(_("High Commission Master BSNL Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCJioMobilePrepaidMaster = models.DecimalField(_("High Commission Master JIO Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCVIMobilePrepaidMaster = models.DecimalField(_("High Commission Master VI Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)
    BbpsHCMTNLMobilePrepaidMaster = models.DecimalField(_("High Commission Master MTNL Delhi & Mumbai Mobile Prepaid - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.10)

    # DTH
    BbpsHCDTHAirtelDTv = models.DecimalField(_("High Commission Airtel Dish TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHDishTv = models.DecimalField(_("High Commission Dish TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHTataSky = models.DecimalField(_("High Commission TataSky - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHVideoconTv = models.DecimalField(_("High Commission Videocon TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHBigTv = models.DecimalField(_("High Commission Big TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)

    BbpsHCDTHAirtelDTvDistributor = models.DecimalField(_("High Commission Distributor Airtel Dish TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHDishTvDistributor = models.DecimalField(_("High Commission Distributor Dish TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHTataSkyDistributor = models.DecimalField(_("High Commission Distributor TataSky - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHVideoconTvDistributor = models.DecimalField(_("High Commission Distributor Videocon TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHBigTvDistributor = models.DecimalField(_("High Commission Distributor Big TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)

    BbpsHCDTHAirtelDTvMaster = models.DecimalField(_("High Commission Master Airtel Dish TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHDishTvMaster = models.DecimalField(_("High Commission Master Dish TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHTataSkyMaster = models.DecimalField(_("High Commission Master TataSky - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHVideoconTvMaster = models.DecimalField(_("High Commission Master Videocon TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)
    BbpsHCDTHBigTvMaster = models.DecimalField(_("High Commission Master Big TV - Any Amount (%)"), max_digits=10, decimal_places=2, default=0.50)

    def __str__(self):
        return self.userAccount.username
    

class Payout(models.Model):
    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    amount = models.CharField(_("Amount"), max_length=500, blank=True)
    txn_status = models.CharField(_("Txn Status"), max_length=50, blank=True)
    tid = models.CharField(_("Tid"), max_length=500, blank=True)
    client_ref_id = models.CharField(_("Client Ref Id"), max_length=500, blank=True)
    recipient_name = models.CharField(_("Recipient Name"), max_length=500, blank=True)
    ifsc = models.CharField(_("IFSC"), max_length=500, blank=True)
    account = models.CharField(_("Account"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userAccount.username


class PaySprintPayout(models.Model):
    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    ref_id = models.CharField(_("Reference ID"), max_length=500, blank=True, null=True)
    ack_no = models.CharField(_("Acknowledgement Number"), max_length=500, blank=True, null=True)
    bank_name = models.CharField(_("Bank Name"), max_length=500, blank=True, null=True)
    account_no = models.CharField(_("Account Number"), max_length=500, blank=True, null=True)
    beneficiary_name = models.CharField(_("Beneficiary Name"), max_length=500, blank=True, null=True)
    amount = models.CharField(_("Amount"), max_length=500, blank=True, null=True)
    ifsc = models.CharField(_("IFSC"), max_length=500, blank=True, null=True)
    mode = models.CharField(_("Mode"), max_length=500, blank=True, null=True)
    charges = models.CharField(_("Charges"), max_length=500, blank=True, null=True)
    utr = models.CharField(_("UTR"), max_length=500, blank=True, null=True)
    txn_status = models.CharField(_("Txn Status"), max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userAccount.username
    

class CommissionTxn(models.Model):
    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    amount = models.CharField(_("Amount"), max_length=500, blank=True)
    txn_status = models.CharField(_("Txn Status"), max_length=50, blank=True)
    desc = models.CharField(_("Commission Description"), max_length=50)
    agent_name = models.CharField(_("Agent Name"), max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userAccount.username


class PaySprintMerchantAuth(models.Model):
    userAccount = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    is_bank2_registered = models.BooleanField(default=False)
    is_bank3_registered = models.BooleanField(default=False)
    registration_date = models.DateTimeField(null=True, blank=True)
    bank2_last_authentication_date = models.DateTimeField(null=True, blank=True)
    bank3_last_authentication_date = models.DateTimeField(null=True, blank=True)
    bank2_MerAuthTxnId = models.CharField(max_length=255, null=True, blank=True)
    bank3_MerAuthTxnId = models.CharField(max_length=255, null=True, blank=True)


class PaySprintPayoutBankAccountDetails(models.Model):
    class AccountTypes(models.TextChoices):
        Primary = "PRIMARY", _("Primary")
        Relative = "RELATIVE", _("Relative")

    class AccountStatus(models.TextChoices):
        Deactivated = 0, _("Account Deactivated")
        Activated = 1, _("Account Activated")
        DocumentUploadPending = 2, _("Document Upload Pending")
        DocumentVerificationPending = 3, _("Document Verification pending at admin end")

    userAccount = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    bene_id = models.CharField(_("Beneficiary Id"), max_length=255, unique=True, null=True)
    account = models.CharField(_("Account Number"), max_length=255, null=True)
    bankid = models.CharField(_("DMT Bank Id"), max_length=255, null=True)
    ifsc = models.CharField(_("IFSC Code"), max_length=255, null=True)
    name = models.CharField(_("Beneficiary Name"), max_length=255, null=True)
    account_type = models.CharField(_("Account Type"), max_length=10, choices=AccountTypes.choices, default=AccountTypes.Primary)
    acc_status = models.CharField(_("Account Status"), max_length=10, choices=AccountStatus.choices, default=AccountStatus.DocumentUploadPending)


class PaySprintAEPSTxnDetail(models.Model):
    class Txn_Status(models.TextChoices):
        Failed = "0", _("Failed")
        Success = "1", _("Success")
        Pending = "2", _("Pending")
        Txn_Not_Found = "3", _("Transaction Not found in system")
        Bad_Request = "other", _("Bad request, Try again")

    class Service_Type(models.TextChoices):
        Aadhaar_Pay = "1", _("Aadhaar Pay")
        Cash_Withdrawal = "2", _("Cash Withdrawal")
        Balance_Inquiry = "3", _("Balance Inquiry")
        Mini_Statement = "4", _("Mini Statement")

    userAccount = models.ForeignKey(UserAccount, verbose_name=_("Linked User"), on_delete=models.CASCADE)
    reference_no = models.CharField(_("Reference No"), max_length=500, blank=True, default="N/A")
    txn_status = models.CharField(max_length=20, choices=Txn_Status.choices, default=Txn_Status.Pending)
    message = models.CharField(_("Message"), max_length=500, blank=True, default="N/A")
    ack_no = models.CharField(_("ack_no"), max_length=500, blank=True, null=True)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2, blank=True, default=0.0)
    balance_amount = models.CharField(_("Balance Amount"), max_length=20, blank=True, default="N/A")
    bank_rrn = models.CharField(_("bank_rrn"), max_length=500, blank=True, default="N/A")
    bank_iin = models.CharField(_("bank_iin"), max_length=255, blank=True, default="N/A")
    service_type = models.CharField(max_length=20, choices=Service_Type.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            # Set the timestamp to the current time in the default time zone
            self.timestamp = timezone.now()

        super().save(*args, **kwargs)

    def get_status_display(self):
        return dict(PaySprintAEPSTxnDetail.Txn_Status.choices).get(self.txn_status, '')

    def get_service_display(self):
        return dict(PaySprintAEPSTxnDetail.Service_Type.choices).get(self.service_type, '')



# signals
@receiver(models.signals.pre_delete, sender=UserKYCDocument)
def delete_document_files(sender, instance, **kwargs):
    # Remove the file when the UserKYCDocument instance is deleted
    for field in instance._meta.fields:
        if isinstance(field, models.FileField):
            file_field = getattr(instance, field.name)
            if file_field:
                file_path = file_field.path
                if os.path.exists(file_path):
                    os.remove(file_path)
