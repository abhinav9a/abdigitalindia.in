from django.contrib import admin
from .models import (UserKYCDocument, OtherServices, Wallet, WalletTransaction, QRTxnCallbackByEko, ServiceActivation,
                     AepsTxnCallbackByEko, DMTBankList, PanVerificationTxn, BankVerificationTxn, DmtTxn, Commission,
                     Payout, PaySprintPayout, BbpsTxn, CommissionTxn, CMSTxnCallbackByEko, CreditCardTxn,
                     AdhaarVerificationTxn, OtherServices2)
from django.utils.translation import gettext_lazy as _

# Register your models here.

class UserKYCDocumentAdmin(admin.ModelAdmin):
    list_display = ('id','userAccount', 'aadharFront','aadharBack', 'pancard', 'cancelChequePassbook', 'declarationForm', 'photo', 'policeVerification')


class OtherServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'name', 'mobile', 'email', 'serviceName', 'serviceDescription')

class OtherServices2Admin(admin.ModelAdmin):
    list_display = ('id', 'serviceName', 'serviceUrl')

class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'balance')

class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'transaction_type', 'client_ref_id', 'txnId', 'txn_status', 'description', 'timestamp')

class QRTxnCallbackByEkoAdmin(admin.ModelAdmin):
    list_display = ('id', 'txn_detail', 'timestamp')

class AepsTxnCallbackByEkoAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'client_ref_id', 'amount', 'tid', 'aadhar_no', 'tx_status', 'service_type', 'timestamp')
    
class PanVerificationTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'txn_status', 'description', 'timestamp')

class AdhaarVerificationTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'txn_status', 'description', 'timestamp')

class BankVerificationTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'txnId', 'client_ref_id', 'txn_status', 'description', 'timestamp')

class DmtTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'txnId', 'client_ref_id', 'txn_status', 'description', 'timestamp')

class CreditCardTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'client_ref_id', 'txn_status', 'description', 'timestamp')

class PayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'amount', 'tid', 'client_ref_id', 'txn_status', 'recipient_name', 'timestamp')

class PaySprintPayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'amount', 'utr', 'ref_id', 'txn_status', 'beneficiary_name', 'timestamp')

    def get_model_name(self, obj=None):
        return "Payouts 2"


class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'QrPaymentService', 'AepsService')

class DMTBankListAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_name', 'bank_id', 'bank_code')

class BbpsTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'tid', 'customermobilenumber', 'operator_name', 'txstatus_desc', 'amount')
    
class CommissionTxnAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'txn_status', 'amount', 'desc', "agent_name")

class CMSTxnCallbackByEkoAdmin(admin.ModelAdmin):
    list_display = ('id', 'txn_detail', "timestamp")

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'userAccount', 'AepsCommissionSlab1', 'AepsCommissionSlab2', 'AepsCommissionSlab3', "AepsCommissionSlab4", 'AepsCommissionSlab5', 'AepsCommissionSlab6', 'AepsCommissionSlab7', 'AepsCommissionSlab8')

    fieldsets = [
        (
            None,
            {
                "fields": ["userAccount"],
            },
        ),
        (
            "AePS - User Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "AepsCommissionSlab1", 
                    "AepsCommissionSlab2", 
                    "AepsCommissionSlab3",
                    "AepsCommissionSlab4",
                    "AepsCommissionSlab5",
                    "AepsCommissionSlab6",
                    "AepsCommissionSlab7",
                    "AepsCommissionSlab8",
                    ]
            },
        ),
        (
            "AePS - Distributor Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "AepsCommissionSlabDistributor1",
                    "AepsCommissionSlabDistributor2",
                    "AepsCommissionSlabDistributor3",
                    "AepsCommissionSlabDistributor4",
                    "AepsCommissionSlabDistributor5",
                    "AepsCommissionSlabDistributor6",
                    "AepsCommissionSlabDistributor7",
                    "AepsCommissionSlabDistributor8",
                    ]
            },
        ),
        (
            "AePS - Master Distributor Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "AepsCommissionSlabMaster1",
                    "AepsCommissionSlabMaster2",
                    "AepsCommissionSlabMaster3",
                    "AepsCommissionSlabMaster4",
                    "AepsCommissionSlabMaster5",
                    "AepsCommissionSlabMaster6",
                    "AepsCommissionSlabMaster7",
                    "AepsCommissionSlabMaster8",
                    ]
            },
        ),
        (
            "DMT - Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "DmtCommission",
                    ]
            },
        ),
        (
            "BBPS - Instant Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsInstantElectricity",
                    "BbpsInstantLoan",
                    "BbpsInstantRechargePrepaid",
                    "BbpsInstantRechargePostpaid",
                    "BbpsInstantDTH"               
                    ]
            },
        ),
        (
            "BBPS - Distributor Instant Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsInstantElectricityDistributor",
                    "BbpsInstantLoanDistributor",
                    "BbpsInstantRechargePrepaidDistributor",
                    "BbpsInstantRechargePostpaidDistributor",
                    "BbpsInstantDTHDistributor",             
                    ]
            },
        ),
        (
            "BBPS - Master Distributor Instant Commision",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsInstantElectricityMaster",
                    "BbpsInstantLoanMaster",
                    "BbpsInstantRechargePrepaidMaster",
                    "BbpsInstantRechargePostpaidMaster",
                    "BbpsInstantDTHMaster",             
                    ]
            },
        ),
        (
            "BBPS - High Commision Electricity",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCElectricitySlab1",
                    "BbpsHCElectricitySlab2",
                    "BbpsHCElectricitySlab3",
                    "BbpsHCElectricitySlab4",
                    "BbpsHCElectricitySlab5",
                    "BbpsHCElectricitySlab6",
                    "BbpsHCElectricitySlab7",             
                    ]
            },
        ),
        (
            "BBPS - Distributor High Commision Electricity",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCElectricitySlabDistributor1",
                    "BbpsHCElectricitySlabDistributor2",
                    "BbpsHCElectricitySlabDistributor3",
                    "BbpsHCElectricitySlabDistributor4",
                    "BbpsHCElectricitySlabDistributor5",
                    "BbpsHCElectricitySlabDistributor6",
                    "BbpsHCElectricitySlabDistributor7",            
                    ]
            },
        ),
        (
            "BBPS - Master Distributor High Commision Electricity",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCElectricitySlabMaster1",
                    "BbpsHCElectricitySlabMaster2",
                    "BbpsHCElectricitySlabMaster3",
                    "BbpsHCElectricitySlabMaster4",
                    "BbpsHCElectricitySlabMaster5",
                    "BbpsHCElectricitySlabMaster6",
                    "BbpsHCElectricitySlabMaster7",
                    ]
            },
        ),
        (
            "BBPS - High Commision Water & Piped Gas Bill",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCWaterNGasSlab1",
                    "BbpsHCWaterNGasSlab2",
                    "BbpsHCWaterNGasSlab3",
                    "BbpsHCWaterNGasSlab4",
                    "BbpsHCWaterNGasSlab5",
                    "BbpsHCWaterNGasSlab6",
                    ]
            },
        ),
        (
            "BBPS - Distributor High Commision Water & Piped Gas Bill",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCWaterNGasSlabDistributor1",
                    "BbpsHCWaterNGasSlabDistributor2",
                    "BbpsHCWaterNGasSlabDistributor3",
                    "BbpsHCWaterNGasSlabDistributor4",
                    "BbpsHCWaterNGasSlabDistributor5",
                    "BbpsHCWaterNGasSlabDistributor6",
                    ]
            },
        ),
        (
            "BBPS - Master Distributor High Commision Water & Piped Gas Bill",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCWaterNGasSlabMaster1",
                    "BbpsHCWaterNGasSlabMaster2",
                    "BbpsHCWaterNGasSlabMaster3",
                    "BbpsHCWaterNGasSlabMaster4",
                    "BbpsHCWaterNGasSlabMaster5",
                    "BbpsHCWaterNGasSlabMaster6",
                    ]
            },
        ),
        (
            "BBPS - High Commision Mobile Postpaid & Fixed Landline",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCMobilePostpaid",
                    "BbpsHCMobilePostpaidDistributor",
                    "BbpsHCMobilePostpaidMaster",
                    ]
            },
        ),
        (
            "BBPS - High Commision Mobile Prepaid",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCAirtelMobilePrepaid",
                    "BbpsHCBSNLMobilePrepaid",
                    "BbpsHCJioMobilePrepaid",
                    "BbpsHCVIMobilePrepaid",
                    "BbpsHCMTNLMobilePrepaid",
                    ]
            },
        ),
        (
            "BBPS - Distributor High Commision Mobile Prepaid",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCAirtelMobilePrepaidDistributor",
                    "BbpsHCBSNLMobilePrepaidDistributor",
                    "BbpsHCJioMobilePrepaidDistributor",
                    "BbpsHCVIMobilePrepaidDistributor",
                    "BbpsHCMTNLMobilePrepaidDistributor",
                    ]
            },
        ),
        (
            "BBPS - Master Distributor High Commision Mobile Prepaid",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCAirtelMobilePrepaidMaster",
                    "BbpsHCBSNLMobilePrepaidMaster",
                    "BbpsHCJioMobilePrepaidMaster",
                    "BbpsHCVIMobilePrepaidMaster",
                    "BbpsHCMTNLMobilePrepaidMaster",
                    ]
            },
        ),
        (
            "BBPS - High Commision DTH Prepaid",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCDTHAirtelDTv",
                    "BbpsHCDTHDishTv",
                    "BbpsHCDTHTataSky",
                    "BbpsHCDTHVideoconTv",
                    "BbpsHCDTHBigTv",
                    ]
            },
        ),
        (
            "BBPS - Distributor High Commision DTH Prepaid",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCDTHAirtelDTvDistributor",
                    "BbpsHCDTHDishTvDistributor",
                    "BbpsHCDTHTataSkyDistributor",
                    "BbpsHCDTHVideoconTvDistributor",
                    "BbpsHCDTHBigTvDistributor",
                    ]
            },
        ),
        (
            "BBPS - Master Distributor High Commision DTH Prepaid",
            {
                "classes": ["collapse"],
                "fields": [
                    "BbpsHCDTHAirtelDTvMaster",
                    "BbpsHCDTHDishTvMaster",
                    "BbpsHCDTHTataSkyMaster",
                    "BbpsHCDTHVideoconTvMaster",
                    "BbpsHCDTHBigTvMaster",
                    ]
            },
        ),
    ]

    

admin.site.register(UserKYCDocument, UserKYCDocumentAdmin)
admin.site.register(OtherServices, OtherServicesAdmin)
admin.site.register(OtherServices2, OtherServices2Admin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(QRTxnCallbackByEko, QRTxnCallbackByEkoAdmin)
admin.site.register(AepsTxnCallbackByEko, AepsTxnCallbackByEkoAdmin)
admin.site.register(ServiceActivation, ServiceStatusAdmin)
# admin.site.register(DMTBankList, DMTBankListAdmin)
admin.site.register(PanVerificationTxn, PanVerificationTxnAdmin)
admin.site.register(AdhaarVerificationTxn, AdhaarVerificationTxnAdmin)
admin.site.register(BankVerificationTxn, BankVerificationTxnAdmin)
admin.site.register(DmtTxn, DmtTxnAdmin)
admin.site.register(CreditCardTxn, CreditCardTxnAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Payout, PayoutAdmin)
admin.site.register(PaySprintPayout, PaySprintPayoutAdmin)
admin.site.register(BbpsTxn, BbpsTxnAdmin)
admin.site.register(CommissionTxn, CommissionTxnAdmin)
admin.site.register(CMSTxnCallbackByEko, CMSTxnCallbackByEkoAdmin)
