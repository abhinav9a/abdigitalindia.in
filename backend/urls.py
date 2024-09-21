from django.urls import path
from . import views, view_users, view_services, view_admins, api_views, view_paysprint_services

urlpatterns = [
    path('user-signup', view_users.user_signup, name='user_signup'),
    path('user-login', view_users.user_login, name='user_login'),
    path('user-logout', view_users.user_logout, name='user_logout'),
    path('user-profile', view_users.user_profile, name='user_profile'),
    path('change-password', view_users.change_password, name='change_password'),

    path('generate-id-card', view_users.generate_id_card, name='generate_id_card'),

    # QR Payment Service Urls
    path('activate-qr-payment', view_services.activate_qr_payment, name='activate_qr_payment'),
    path('recharge-wallet', view_services.recharge_wallet, name='recharge_wallet'),  # Eko
    path('wallet-report', view_services.wallet_report, name='wallet_report'),
    path('wallet-2-report', view_services.wallet2_report, name='wallet2_report'),
    path('get_config_info', view_services.get_config_info, name='get_config_info'),

    # AEPS Service Urls
    path('activate-aeps', view_services.activate_aeps, name='activate_aeps'),
    path('aeps', view_services.aeps, name='aeps'),
    path('aeps-report', view_services.aeps_report, name='aeps_report'),

    # AEPS 2 (PaySprint)
    path('add-commission-charges', view_admins.add_commission_charges,  name='add_commission_charges_paysprint'),
    path('aeps-wallet-2', view_paysprint_services.user_onboarding,  name='onboarding_user_paysprint'),
    path('aeps-wallet-2-status', view_paysprint_services.user_onboarding_status,  name='onboarding_user_status_paysprint'),
    path('balance-enquiry', view_paysprint_services.balance_enquiry,  name='balance_enquiry_paysprint'),
    path('cash-withdrawl', view_paysprint_services.cash_withdrawal,  name='cash_withdrawl_paysprint'),
    path('mini-statement', view_paysprint_services.mini_statement,  name='mini_statement_paysprint'),
    path('aadhar-pay', view_paysprint_services.aadhar_pay,  name='aadhar_pay_paysprint'),
    path('Twofactorkyc-registraton', view_paysprint_services.merchant_registration_with_bank,  name='merchant_registration_with_bank_paysprint'),
    path('aeps-report-2', view_paysprint_services.aeps_report, name='aeps_report_paysprint'),
    # API Callback Views
    path('callback', api_views.pay_sprint_onboarding_callback, name='onboarding_callback'),

    # DMT
    # if customer exists
    path('dmt', view_services.list_dmt_recipient, name='list_dmt_recipient'),
    path('dmt-initiate-payment', view_services.initiate_dmt_payment, name='initiate_dmt_payment'),
    path('dmt-initiate-refund', view_services.initiate_dmt_refund, name='initiate_dmt_refund'),
    path('dmt-initiate-refund-otp', view_services.resend_dmt_refund_otp, name='resend_dmt_refund_otp'),
    path('dmt-create-recipient', view_services.create_dmt_recipient, name='create_dmt_recipient'),
    path('dmt-report', view_services.dmt_report, name='dmt_report'),
    
    # if customer not exists
    path('dmt-create-customer', view_services.create_dmt_customer, name='create_dmt_customer'),
    path('dmt-verify-otp', view_services.verify_dmt_otp, name='verify_dmt_otp'),
    path('dmt-customer-info', view_services.get_dmt_customer_info, name='get_dmt_customer_info'),

    # Payout Urls
    path('bank-add', view_services.add_bank, name='add_bank'),
    path('transfer-fund', view_services.transfer_fund, name='transfer_fund'),
    path('Payout-report', view_services.payout_report, name='payout_report'),

    # PAYOUT 2 (PaySprint)
    path('add-account', view_paysprint_services.add_bank, name='add_account'),
    path('do-transaction', view_paysprint_services.do_transaction, name='do_transaction'),
    path('upload-documents', view_paysprint_services.upload_supporting_document, name='upload_documents'),
    path('payout-report-2', view_paysprint_services.payout_report, name='payout_report_paysprint'),

    # Verification service
    path('pan-verification', view_services.pan_verification, name='panVerification'),
    path('pan-verification-report', view_services.pan_verification_report, name='pan_verification_report'),
    path('bank-verification', view_services.bank_verification, name='bankVerification'),
    path('bank-verification-report', view_services.bank_verification_report, name='bank_verification_report'),
    
    path('adhaar-consent', view_services.adhaar_consent, name='adhaar_consent'),
    path('adhaar-verification', view_services.adhaar_verification, name='adhaar_verification'),
    path('adhaar-verification-report', view_services.adhaar_verification_report, name='adhaar_verification_report'),

    path('commission-report', view_services.commission_report, name='commission_report'),


    # Auth Pages
    path('', views.dashboard, name='dashboard'),
    path('kyc-action', views.kycAction, name='kycAction'),
    path('other-services/<str:service>', view_services.otherServices, name='otherServices'),
    path('support', views.support, name='support'),
    path('festival-season-dhamaka', view_services.festivalSeasonDhamaka, name='festivalSeasonDhamaka'),
    path('onboarding-user', view_services.onboarding_user, name='onboardingUser'),
    path('get-services', view_services.get_services, name='getServices'),
    path('get-user-services', view_services.get_user_services, name='userServiceInquiry'),
    path('reload-wallet', view_services.reload_wallet, name='reload_wallet'),
    path('reload-wallet2', view_services.reload_wallet2, name='reload_wallet2'),
    path('import_banks_from_excel', view_services.import_banks_from_excel, name='import_banks_from_excel'),

    # BBPS Urls
    path('bbps', view_services.bbps, name='bbps'),
    path('bbps-operator/<int:id>', view_services.bbps_operator, name='bbps_operator'),

    path('bbps-recharge/<int:id>', view_services.bbps_recharge, name='bbps_recharge'),
    path('get-bbps-recharge-param', view_services.get_bbps_recharge_param, name='get_bbps_recharge_param'),
    
    path('get-bbps-operator-param', view_services.get_bbps_operator_param, name='get_bbps_operator_param'),
    path('bbps-fetchbill', view_services.bbps_fetch_bill, name='bbps_fetch_bill'),
    path('bbps-paybill', view_services.bbps_paybill, name='bbps_paybill'),
    path('bbps-report', view_services.bbps_report, name='bbps_report'),
    
    # Admin Actions
    path('get-user', view_admins.AdminGetUser, name='AdminGetUser'), #admin only to get username
    path('wallet-action', view_admins.AdminWalletAction, name='AdminWalletAction'), #admin only to recharge user's wallet
    path('pending-kyc-action', view_admins.AdminPendingKycList, name='AdminPendingKycList'), #admin only to approve user's KYC
    path('rejected-kyc-action', view_admins.AdminRejectedKycList, name='AdminRejectedKycList'), #admin only to reject user's KYC
    path('explore-pending-kyc/<int:id>', view_admins.AdminExplorePendingKyc, name='AdminExplorePendingKyc'), #admin only to explore pending/rejected user's KYC
    path('all-retailers', view_admins.allRetailers, name='allRetailers'), #admin only to view all retailers
    path('all-distributors', view_admins.allDistributors, name='allDistributors'), #admin only to view all Distributors
    path('all-master-distributors', view_admins.allMasterDistributors, name='allMasterDistributors'), #admin only to view all Master Distributors
    path('txn-status', view_admins.AdminTxnStatus, name='AdminTxnStatus'), #admin only to view all Master Distributors
    path('unauthorized', views.unauthorized, name='unauthorized'), #unauthorized
    path('balance-sheet/<int:id>', view_admins.balance_sheet, name='balance_sheet'),
    path('change-user-password', view_admins.AdminChangeUserPassword, name='AdminChangeUserPassword'),
    
    path('explore-user/<int:id>', view_admins.AdminExploreUser, name='AdminExploreUser'), #admin only to view users profile
    path('explore-aeps-report/<int:id>', view_admins.AdminExploreAepsReport, name='AdminExploreAepsReport'), #admin, md, d only to view user's AEPS report
    path('explore-dmt-report/<int:id>', view_admins.AdminExploreDmtReport, name='AdminExploreDmtReport'), #admin, md, d only to view user's DMT report
    path('explore-wallet-report/<int:id>', view_admins.AdminExploreWalletReport, name='AdminExploreWalletReport'), #admin, md, d only to view user's Wallet report
    path('explore-wallet-2-report/<int:id>', view_admins.AdminExploreWallet2Report, name='AdminExploreWallet2Report'), #admin, md, d only to view user's Wallet 2 report
    path('explore-pan-verification-report/<int:id>', view_admins.AdminExplorePanVerificationReport, name='AdminExplorePanVerificationReport'), #admin, md, d only to view user's Pan Verification report
    path('explore-bank-verification-report/<int:id>', view_admins.AdminExploreBankVerificationReport, name='AdminExploreBankVerificationReport'), #admin, md, d only to view user's Bank Verification report
    path('explore-payout-report/<int:id>', view_admins.AdminExplorePayoutReport, name='AdminExplorePayoutReport'), #admin, md, d only to view user's Payout report
    path('explore-bbps-report/<int:id>', view_admins.AdminExploreBBPSReport, name='AdminExploreBBPSReport'), #admin, md, d only to view user's Payout report
    path('explore-creditcard-report/<int:id>', view_admins.AdminExploreCreditCardReport, name='AdminExploreCreditCardReport'), #admin, md, d only to view user's Payout report

    path('create-new-retailer', view_admins.create_retailer, name='create_retailer'), #admin, md, d only to create retailer
    path('create-new-distributor', view_admins.create_distributor, name='create_distributor'), #admin, md only to create distributor
    path('create-new-master-distributor', view_admins.create_master_distributor, name='create_master_distributor'), #admin only to create master distributor
    
    # path('vpa-verification', view_services.vpa_verification, name='vpa_verification'),
    path('credit-card-bill', view_services.credit_card_bill, name='credit_card_bill'),
    path('create-credit-card-recipient', view_services.create_credit_card_recipient, name='create_credit_card_recipient'),
    path('credit-card-report', view_services.credit_card_report, name='credit_card_report'),

    # API Views
    path('aeps_tx_callback/', api_views.aeps_txn_callback, name='aeps_tx_callback'),
    path('eko_txn_callback/', api_views.eko_txn_callback, name='eko_txn_callback'),
    path('debit-hook-receiver/', api_views.debit_receiver_hook, name='debit_receiver_hook'),

    # Generate PDF Slip
    path('generate_slip/<str:src>/<int:id>', view_services.generate_slip, name='generate_slip'),

    # Pancard UTI
    path('pancard_uti', view_services.pancard_uti, name='pancard_uti'),
    path('pancard_nsdl', view_services.pancard_nsdl, name='pancard_nsdl'),
]
