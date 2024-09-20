from enum import Enum

# PAYSPRINT_BASE_URL = "https://sit.paysprint.in/service-api/"  # Test URL
PAYSPRINT_BASE_URL = "https://api.paysprint.in/"    # Live URL


class PaySprintRoutes(Enum):
    CALLBACK_URL = "https://abdigitalindia.in/user/"
    WEB_ONBOARDING = f"{PAYSPRINT_BASE_URL}api/v1/service/onboard/onboard/getonboardurl"    # Live URL
    # WEB_ONBOARDING = f"{PAYSPRINT_BASE_URL}api/v1/service/onboard/onboardnew/getonboardurl"   # Test URL
    BALANCE_ENQUIRY = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/balanceenquiry/index"
    CASH_WITHDRAWAL = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/authcashwithdraw/index"
    CASH_WITHDRAWAL_TXN_STATUS = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/aepsquery/query"
    MINI_STATEMENT = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/ministatement/index"
    AADHAR_PAY = f"{PAYSPRINT_BASE_URL}api/v1/service/aadharpay/aadharpay/index"
    AADHAR_PAY_TXN_STATUS = f"{PAYSPRINT_BASE_URL}api/v1/service/aadharpay/aadharpayquery/query"
    BANK_2_REGISTRATION = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/kyc/Twofactorkyc/registration"
    BANK_2_AUTHENTICATION = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/kyc/Twofactorkyc/authentication"
    BANK_2_MERCHANT_AUTHENTICITY = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/kyc/Twofactorkyc/merchant_authencity"
    BANK_3_REGISTRATION = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/kyc/Twofactorkyc/register_agent"
    BANK_3_AUTHENTICATION = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/kyc/Twofactorkyc/auth_login"
    BANK_3_AGENT_AUTHENTICITY = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/kyc/Twofactorkyc/agent_authencity"
    AEPS_BANK_LIST = f"{PAYSPRINT_BASE_URL}api/v1/service/aeps/banklist/index"

    # PAYOUT Urls
    GET_LIST = f"{PAYSPRINT_BASE_URL}api/v1/service/payout/payout/list"
    ADD_ACCOUNT = f"{PAYSPRINT_BASE_URL}api/v1/service/payout/payout/add"
    UPLOAD_DOCUMENT = f"{PAYSPRINT_BASE_URL}api/v1/service/payout/payout/uploaddocument"
    ACCOUNT_STATUS = f"{PAYSPRINT_BASE_URL}api/v1/service/payout/Payout/accountstatus"
    DO_TRANSACTION = f"{PAYSPRINT_BASE_URL}api/v1/service/payout/payout/dotransaction"
    TRANSACTION_STATUS = f"{PAYSPRINT_BASE_URL}api/v1/service/payout/payout/status"

DMT_BANK_LIST = [
    {
        "bank_id": 649,
        "bank_name": "A B BANK LIMITED"
    },
    {
        "bank_id": 1908,
        "bank_name": "ABHINANDAN URBAN CO-OP BANK LTD"
    },
    {
        "bank_id": 425,
        "bank_name": "ABHINANDAN URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 2,
        "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 3,
        "bank_name": "ABHYUDAYA MAHILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1874,
        "bank_name": "ABN AMRO CREDIT CARD"
    },
    {
        "bank_id": 4,
        "bank_name": "ABU DHABI COMMERCIAL BANK"
    },
    {
        "bank_id": 157,
        "bank_name": "ACBL ASHOKNAGAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 5,
        "bank_name": "ACE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 441,
        "bank_name": "ADAR P.D.PATIL SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 6,
        "bank_name": "ADARSH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 640,
        "bank_name": "ADARSH MAHILA MERCNT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1025,
        "bank_name": "ADARSH MAHILA NAGARI SAHAKARI BANK "
    },
    {
        "bank_id": 1888,
        "bank_name": "ADITYA BIRLA IDEA PAYMENTS BANK"
    },
    {
        "bank_id": 155,
        "bank_name": "AGARTALA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1835,
        "bank_name": "AGRASEN COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 7,
        "bank_name": "AHILYADEVI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 8,
        "bank_name": "AHMEDABAD MERCANTILE COOPERATIVE BANK"
    },
    {
        "bank_id": 154,
        "bank_name": "AHMEDNAGAR DIST CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 145,
        "bank_name": "AHMEDNAGAR ZILLA PRATHAMIK SHIKSHAK SAHAKARI BANK "
    },
    {
        "bank_id": 1827,
        "bank_name": "AHMEDNAGAR ZPSS BANK"
    },
    {
        "bank_id": 9,
        "bank_name": "AIRTEL PAYMENTS BANK LIMITED"
    },
    {
        "bank_id": 1823,
        "bank_name": "AJANTHA URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 816,
        "bank_name": "AJINKYATARA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1517,
        "bank_name": "AJMER CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 650,
        "bank_name": "AKHAND ANAND COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 152,
        "bank_name": "AKKAMAHADEVI MAHILA SAHAKARI BANK"
    },
    {
        "bank_id": 10,
        "bank_name": "AKOLA JANATA COMMERCIAL COOPERATIVE BANK"
    },
    {
        "bank_id": 642,
        "bank_name": "AKOLA MERCHANT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 641,
        "bank_name": "AKOLA MERCHANT COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1824,
        "bank_name": "AKOLA URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 11,
        "bank_name": "ALAPUZHA DISTRICT COOPERATIVE BANK"
    },
    {
        "bank_id": 12,
        "bank_name": "ALAVI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 828,
        "bank_name": "ALIBAG COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 13,
        "bank_name": "ALLAHABAD BANK"
    },
    {
        "bank_id": 14,
        "bank_name": "ALLAHABAD DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 15,
        "bank_name": "ALLAHABAD UP GRAMIN BANK"
    },
    {
        "bank_id": 16,
        "bank_name": "ALMORA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1821,
        "bank_name": "ALMORA ZILA SAHAKARI BANK "
    },
    {
        "bank_id": 1833,
        "bank_name": "AMALNER URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 757,
        "bank_name": "AMAN SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 643,
        "bank_name": "AMARNATH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 635,
        "bank_name": "AMBAJOGAI PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 758,
        "bank_name": "AMBARNATH JAI HIND COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1830,
        "bank_name": "AMBEDKAR NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1875,
        "bank_name": "AMERICAN EXPRESS CREDIT CARD"
    },
    {
        "bank_id": 1834,
        "bank_name": "AMRAVATI DCC BANK "
    },
    {
        "bank_id": 630,
        "bank_name": "AMRAVATI ZILLA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1354,
        "bank_name": "AMRELI JILLA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 773,
        "bank_name": "AMRELI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 17,
        "bank_name": "ANANDA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 637,
        "bank_name": "ANDAMAN & NICOBAR STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 147,
        "bank_name": "ANDARSUL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 18,
        "bank_name": "ANDHRA BANK"
    },
    {
        "bank_id": 1847,
        "bank_name": "ANDHRA PRADESH GRAMIN VIKAS BANK"
    },
    {
        "bank_id": 20,
        "bank_name": "ANDHRA PRAGATHI GRAMIN BANK"
    },
    {
        "bank_id": 1829,
        "bank_name": "ANENDESHWARI NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1836,
        "bank_name": "ANGUL CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 502,
        "bank_name": "ANNASAHEB CHOUGULE COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 831,
        "bank_name": "ANNASAHEB MAGAR SAHAKARI BANK"
    },
    {
        "bank_id": 631,
        "bank_name": "ANURADHA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 151,
        "bank_name": "AP MAHAJANS COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1,
        "bank_name": "AP MAHESH COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1828,
        "bank_name": "AP RAJA MAHESHWARI BANK"
    },
    {
        "bank_id": 150,
        "bank_name": "AP RAJARAJESWARI MAHILA COOPERATIVE URBAN BANK LIM"
    },
    {
        "bank_id": 636,
        "bank_name": "APANI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 21,
        "bank_name": "APNA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1544,
        "bank_name": "APPASAHEB BIRNALE SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 755,
        "bank_name": "ARIHANT URBAN CO-OPERATIVA BANK LIMITED"
    },
    {
        "bank_id": 23,
        "bank_name": "ARIHANT URBAN COOPERATIVE BANK LIMITED, HDFC BANK"
    },
    {
        "bank_id": 22,
        "bank_name": "ARIHANT URBAN COOPERATIVE BANK LIMITED, YES BANK"
    },
    {
        "bank_id": 760,
        "bank_name": "ARMY BASE WORKSHOP CREDIT CO PRIMARY BANK LIMITED"
    },
    {
        "bank_id": 153,
        "bank_name": "AROODH JYOTI PATTAN SAHAKARA BANK"
    },
    {
        "bank_id": 149,
        "bank_name": "ARUNA SAHAKARA BANK"
    },
    {
        "bank_id": 24,
        "bank_name": "ARUNACHAL PRADESH COOPERATIVE APEX BANK"
    },
    {
        "bank_id": 1846,
        "bank_name": "ARUNACHAL PRADESH RURAL BANK"
    },
    {
        "bank_id": 632,
        "bank_name": "ARVIND SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1852,
        "bank_name": "ARYA VART GRAMIN BANK"
    },
    {
        "bank_id": 754,
        "bank_name": "ASHOK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 25,
        "bank_name": "ASSAM GRAMIN VIKASH BANK"
    },
    {
        "bank_id": 1825,
        "bank_name": "ASSOCIATE COOPERATIVE BANK"
    },
    {
        "bank_id": 639,
        "bank_name": "ASTHA MAHILA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1832,
        "bank_name": "ASTHA MAHILA NAGRIK SAHAKARI BANK MARYADIT"
    },
    {
        "bank_id": 26,
        "bank_name": "AU SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 1822,
        "bank_name": "AURANGABAD DCC BANK"
    },
    {
        "bank_id": 1916,
        "bank_name": "AURANGABAD DCC BANK HO"
    },
    {
        "bank_id": 851,
        "bank_name": "AURANGABAD DIST CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 27,
        "bank_name": "AUSTRALIA AND NEW ZEALAND BANKING GROUP LIMITED"
    },
    {
        "bank_id": 32,
        "bank_name": "AXIS BANK"
    },
    {
        "bank_id": 1861,
        "bank_name": "AXIS BANK CREDIT CARD"
    },
    {
        "bank_id": 904,
        "bank_name": "AZAD URBAN BANK"
    },
    {
        "bank_id": 875,
        "bank_name": "BAGALKOT DIST CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1394,
        "bank_name": "BAGALKOT DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 624,
        "bank_name": "BAIDYABATI SHEORAPHULI COOPERATIVE BANK"
    },
    {
        "bank_id": 168,
        "bank_name": "BALAGERIA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 609,
        "bank_name": "BALASINOR NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1818,
        "bank_name": "BALASORE COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1853,
        "bank_name": "BALIA ETAWA GRAMIN BANK"
    },
    {
        "bank_id": 169,
        "bank_name": "BALLY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 170,
        "bank_name": "BALOTRA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 171,
        "bank_name": "BALTIKURI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 867,
        "bank_name": "BALUSSERY COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 172,
        "bank_name": "BANARAS MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1353,
        "bank_name": "BANASKANTHA DISTRICT CENTRAL COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 338,
        "bank_name": "BANASKANTHA MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1810,
        "bank_name": "BANDA URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 174,
        "bank_name": "BANDHAN BANK LIMITED"
    },
    {
        "bank_id": 941,
        "bank_name": "BANGALORE CITY COOPERATIVE BANK"
    },
    {
        "bank_id": 1411,
        "bank_name": "BANGALORE RURAL RAMANAGAR COOPERATIVE BANK"
    },
    {
        "bank_id": 175,
        "bank_name": "BANGIYA GRAMIN VIKASH BANK"
    },
    {
        "bank_id": 177,
        "bank_name": "BANK OF AMERICA"
    },
    {
        "bank_id": 178,
        "bank_name": "BANK OF BAHARAIN AND KUWAIT"
    },
    {
        "bank_id": 179,
        "bank_name": "BANK OF BARODA"
    },
    {
        "bank_id": 1862,
        "bank_name": "BANK OF BARODA CREDIT CARD"
    },
    {
        "bank_id": 180,
        "bank_name": "BANK OF CEYLON"
    },
    {
        "bank_id": 181,
        "bank_name": "BANK OF INDIA"
    },
    {
        "bank_id": 184,
        "bank_name": "BANK OF MAHARASHTRA"
    },
    {
        "bank_id": 185,
        "bank_name": "BANK OF TOKYO MITSUBISHI LIMITED"
    },
    {
        "bank_id": 186,
        "bank_name": "BANKURA TOWN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 187,
        "bank_name": "BAPUJI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 188,
        "bank_name": "BARAMULLA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1489,
        "bank_name": "BARAN KENDRIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 613,
        "bank_name": "BARAN NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 189,
        "bank_name": "BARCLAYS BANK"
    },
    {
        "bank_id": 1878,
        "bank_name": "BARCLAYS BANK CREDIT CARD"
    },
    {
        "bank_id": 1351,
        "bank_name": "BARODA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 190,
        "bank_name": "BARODA GUJARAT GRAMIN BANK"
    },
    {
        "bank_id": 191,
        "bank_name": "BARODA RAJASTHAN GRAMIN BANK"
    },
    {
        "bank_id": 192,
        "bank_name": "BARODA UTTAR PRADESH GRAMIN BANK"
    },
    {
        "bank_id": 462,
        "bank_name": "BASODA NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 193,
        "bank_name": "BASSEIN CATHOLIC COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 752,
        "bank_name": "BASTI ZILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 194,
        "bank_name": "BEAWAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 158,
        "bank_name": "BELAGAVI SHREE BASAVESHWAR COOPERATIVE BANK"
    },
    {
        "bank_id": 619,
        "bank_name": "BELGAUM INDUSTRIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 883,
        "bank_name": "BELGAUM ZILLA RANI CHANNAMMA MAHILA SAHAKARI BANK "
    },
    {
        "bank_id": 886,
        "bank_name": "BELLAD BAGEWADI URBAN SOUHARD SAHAKARI BANK "
    },
    {
        "bank_id": 1817,
        "bank_name": "BERHAMPUR CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 138,
        "bank_name": "BETUL NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1816,
        "bank_name": "BHADOHI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1132,
        "bank_name": "BHADRADRI COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 612,
        "bank_name": "BHAGINI NIVEDITA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 623,
        "bank_name": "BHAGYODAYA FRIENDS UR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 195,
        "bank_name": "BHARAT COOPERATIVE BANK MUMBAI LIMITED"
    },
    {
        "bank_id": 606,
        "bank_name": "BHARATHIYA SAHAKARA BANK "
    },
    {
        "bank_id": 1567,
        "bank_name": "BHARATI SAHAKARI BANK"
    },
    {
        "bank_id": 1352,
        "bank_name": "BHARUCH DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1629,
        "bank_name": "BHATPARA NAIHATI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 144,
        "bank_name": "BHAUSAHEB BIRAJDAR NAGARI SAHAKARI BANK"
    },
    {
        "bank_id": 753,
        "bank_name": "BHAUSAHEB BIRAJDAR NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1812,
        "bank_name": "BHAVANA RISHI COOPERATIVE BANK "
    },
    {
        "bank_id": 780,
        "bank_name": "BHAVANI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 749,
        "bank_name": "BHAVANI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1350,
        "bank_name": "BHAVNAGAR DISTRICT CENTRAL COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 196,
        "bank_name": "BHEL EMPLOYEES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 611,
        "bank_name": "BHILAI NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 614,
        "bank_name": "BHILWARA MAHILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 622,
        "bank_name": "BHILWARA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 608,
        "bank_name": "BHIND NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 1542,
        "bank_name": "BHINGAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 204,
        "bank_name": "BHOPAL  COOPERATIVE CENTRAL BANK LIMITED"
    },
    {
        "bank_id": 258,
        "bank_name": "BHUJ MERCHANTILE BANK"
    },
    {
        "bank_id": 1927,
        "bank_name": "BIHAR GRAMIN BANK"
    },
    {
        "bank_id": 197,
        "bank_name": "BIHAR KSHETRIYA GRAMIN BANK"
    },
    {
        "bank_id": 1811,
        "bank_name": "BIHAR STATE COOPERATIVE BANK "
    },
    {
        "bank_id": 1401,
        "bank_name": "BIJAPUR COOPERATIVE CENTRAL BANK LIMITED"
    },
    {
        "bank_id": 143,
        "bank_name": "BIJAPUR DISTRICT MAHILA COOPERATIVE BANK"
    },
    {
        "bank_id": 159,
        "bank_name": "BIJAPUR SAHAKARI BANK"
    },
    {
        "bank_id": 874,
        "bank_name": "BILAGI PATTANA SAHAKARI BANK"
    },
    {
        "bank_id": 615,
        "bank_name": "BILASA MAHILA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 610,
        "bank_name": "BILASPUR NAGRIK SAHA BANK LIMITED"
    },
    {
        "bank_id": 751,
        "bank_name": "BIRDEV SAHAKARI BANK "
    },
    {
        "bank_id": 1815,
        "bank_name": "BIRDEV SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 167,
        "bank_name": "BNP PARIBAS BANK"
    },
    {
        "bank_id": 173,
        "bank_name": "BOLANGIR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 140,
        "bank_name": "BOMBAY MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1819,
        "bank_name": "BOUDH COOPERATIVE CENTRAL BANK "
    },
    {
        "bank_id": 1814,
        "bank_name": "BRAHMADEODADA BANK "
    },
    {
        "bank_id": 198,
        "bank_name": "BRAHMAWART COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 604,
        "bank_name": "BRAMHAPURI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 141,
        "bank_name": "BULDANA DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 199,
        "bank_name": "CANARA BANK"
    },
    {
        "bank_id": 1863,
        "bank_name": "CANARA BANK CREDIT CARD"
    },
    {
        "bank_id": 200,
        "bank_name": "CAPITAL SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 201,
        "bank_name": "CATHOLIC SYRIAN BANK LIMITED"
    },
    {
        "bank_id": 207,
        "bank_name": "CENTRAL BANK OF INDIA"
    },
    {
        "bank_id": 208,
        "bank_name": "CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 209,
        "bank_name": "CENTRAL MADHYA PRADESH GRAMIN BANK"
    },
    {
        "bank_id": 206,
        "bank_name": "CG RAJYA SAHAKRI BANK "
    },
    {
        "bank_id": 1022,
        "bank_name": "CHAITANYA COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 19,
        "bank_name": "CHAITANYA GODAVARI GRAMIN BANK"
    },
    {
        "bank_id": 132,
        "bank_name": "CHAITANYA MAHILA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 768,
        "bank_name": "CHAITANYA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 744,
        "bank_name": "CHAMOLI ZILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1805,
        "bank_name": "CHARTERED SAHAKARI BANK NIYAMITHA"
    },
    {
        "bank_id": 1131,
        "bank_name": "CHEMBUR NAGARIK SAHAKARI BANK"
    },
    {
        "bank_id": 210,
        "bank_name": "CHHATTISGARH GRAMIN BANK"
    },
    {
        "bank_id": 1808,
        "bank_name": "CHIKHLI URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 1402,
        "bank_name": "CHIKMAGALUR DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 211,
        "bank_name": "CHINATRUST COMMERCIAL BANK LIMITED"
    },
    {
        "bank_id": 1568,
        "bank_name": "CHIPLUN URBAN BANK"
    },
    {
        "bank_id": 1409,
        "bank_name": "CHITRADURGA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1510,
        "bank_name": "CHITTORGARH CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 595,
        "bank_name": "CHITTORGARH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 597,
        "bank_name": "CHOPDA PEOPLES COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 419,
        "bank_name": "CHURU ZILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 594,
        "bank_name": "CHURUZILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 212,
        "bank_name": "CITI BANK"
    },
    {
        "bank_id": 1879,
        "bank_name": "CITIBANK CREDIT CARD"
    },
    {
        "bank_id": 213,
        "bank_name": "CITIZEN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 214,
        "bank_name": "CITIZEN CREDIT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1806,
        "bank_name": "CITIZENS COOPERATIVE BANK "
    },
    {
        "bank_id": 215,
        "bank_name": "CITIZENS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1809,
        "bank_name": "CITIZENS URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 216,
        "bank_name": "CITY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 217,
        "bank_name": "CITY UNION BANK LIMITED"
    },
    {
        "bank_id": 413,
        "bank_name": "COL R D NIKAM SAINIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 599,
        "bank_name": "COLOUR MERCHANT'S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 218,
        "bank_name": "COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 219,
        "bank_name": "COMMONWEALTH BANK OF AUSTRALIA"
    },
    {
        "bank_id": 220,
        "bank_name": "CONTAI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 221,
        "bank_name": "CORPORATION BANK"
    },
    {
        "bank_id": 1864,
        "bank_name": "CORPORATION BANK CREDIT CARD"
    },
    {
        "bank_id": 222,
        "bank_name": "CREDIT AGRICOLE CORPORATE AND INVESTMENT BANK CALYON BANK"
    },
    {
        "bank_id": 223,
        "bank_name": "CREDIT SUISEE AG BANK"
    },
    {
        "bank_id": 224,
        "bank_name": "CUTTACK CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 810,
        "bank_name": "D.Y.PATIL SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 124,
        "bank_name": "DADASAHEB RAMRAO PATIL COOPERATIVE BANK"
    },
    {
        "bank_id": 123,
        "bank_name": "DAIVADNYA SAHAKARA BANK"
    },
    {
        "bank_id": 582,
        "bank_name": "DAIVADNYA SAHAKARA BANK "
    },
    {
        "bank_id": 1936,
        "bank_name": "DAKSHIN BIHAR GRAMIN BANK"
    },
    {
        "bank_id": 862,
        "bank_name": "DAPOLI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 225,
        "bank_name": "DARJEELING DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 579,
        "bank_name": "DARUSSALAM COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 743,
        "bank_name": "DATTATRAYA MAHARAJ KALAMBE JAOLI SAHAKARI BANK LIM"
    },
    {
        "bank_id": 593,
        "bank_name": "DAUND URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1491,
        "bank_name": "DAUSA KENDRIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 226,
        "bank_name": "DAUSA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1395,
        "bank_name": "DAVANAGERE CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 128,
        "bank_name": "DAVANGERE HARIHAR URBAN SAHAKARI BANK"
    },
    {
        "bank_id": 897,
        "bank_name": "DAYALBAGH MAHILA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1895,
        "bank_name": "DBS"
    },
    {
        "bank_id": 227,
        "bank_name": "DCB BANK LIMITED"
    },
    {
        "bank_id": 584,
        "bank_name": "DEENDAYAL N S BANK LIMITED"
    },
    {
        "bank_id": 125,
        "bank_name": "DEENDAYAL NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1797,
        "bank_name": "DEHRADUN DISTT COOPERATIVE BANK "
    },
    {
        "bank_id": 1800,
        "bank_name": "DELHI NAGRIK SEH BANK"
    },
    {
        "bank_id": 228,
        "bank_name": "DENA BANK"
    },
    {
        "bank_id": 1891,
        "bank_name": "DENA GUJARAT GRAMIN BANK"
    },
    {
        "bank_id": 1913,
        "bank_name": "DENA GUJARAT GRAMIN BANK"
    },
    {
        "bank_id": 127,
        "bank_name": "DEOGHAR JAMATRA CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1799,
        "bank_name": "DEOGIRI NAGARI SAHAKARI BANK "
    },
    {
        "bank_id": 229,
        "bank_name": "DEOGIRI NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 230,
        "bank_name": "DEORIA KASIA DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 231,
        "bank_name": "DEPOSIT INSURANCE AND CREDIT GUARANTEE CORPORATION"
    },
    {
        "bank_id": 585,
        "bank_name": "DESAIGANJ NAGARI COOPERATIVE BANK"
    },
    {
        "bank_id": 232,
        "bank_name": "DEUSTCHE BANK"
    },
    {
        "bank_id": 233,
        "bank_name": "DEVELOPMENT BANK OF SINGAPORE"
    },
    {
        "bank_id": 1801,
        "bank_name": "DEVELOPMENT COOPERATIVE BANK "
    },
    {
        "bank_id": 590,
        "bank_name": "DEVI GAYATRI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 234,
        "bank_name": "DEVIKA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 363,
        "bank_name": "DEVYANI SAHAKARI BANK "
    },
    {
        "bank_id": 182,
        "bank_name": "DHAKURIA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 235,
        "bank_name": "DHANALAKSHMI BANK"
    },
    {
        "bank_id": 122,
        "bank_name": "DHANASHREE URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 795,
        "bank_name": "DHULE AND NANDURBAR DISTRICT CENTRAL COOPERATIVE B"
    },
    {
        "bank_id": 126,
        "bank_name": "DHULE AND NANDURBAR JILHA SARKARI BANK"
    },
    {
        "bank_id": 121,
        "bank_name": "DHULE VIKAS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 589,
        "bank_name": "DILIP URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 236,
        "bank_name": "DISTRICT COOPERATIVE BANK"
    },
    {
        "bank_id": 1804,
        "bank_name": "DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 725,
        "bank_name": "DISTRICT COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 237,
        "bank_name": "DOHA BANK"
    },
    {
        "bank_id": 940,
        "bank_name": "DOHA BANK "
    },
    {
        "bank_id": 238,
        "bank_name": "DOMBIVLI NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 633,
        "bank_name": "DR BABASAHEB AMBEDKAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 628,
        "bank_name": "DR BABASAHEB AMBEDKAR UR COOPERATIVE BANK"
    },
    {
        "bank_id": 129,
        "bank_name": "DR BABASAHEB AMBEDKAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 108,
        "bank_name": "DR JAIPRAKASH MUNDADA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 239,
        "bank_name": "DUMKA CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 586,
        "bank_name": "DURGAPUR MAHILA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 240,
        "bank_name": "DURGAPUR STEEL PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 742,
        "bank_name": "DWARKADAS MANTRI NAGARI SAHAKARI BANK"
    },
    {
        "bank_id": 1910,
        "bank_name": "District Co Operative Bank Ltd Faizabad"
    },
    {
        "bank_id": 1892,
        "bank_name": "District Cooperative Bank limited"
    },
    {
        "bank_id": 1843,
        "bank_name": "ELLAQUAI DEHATI BANK"
    },
    {
        "bank_id": 241,
        "bank_name": "EQUITAS SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 242,
        "bank_name": "ESAF SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 243,
        "bank_name": "ETAH DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 244,
        "bank_name": "ETAH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 245,
        "bank_name": "ETAWAH DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 575,
        "bank_name": "ETAWAH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 578,
        "bank_name": "EXCELLENT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 246,
        "bank_name": "EXPORT IMPORT BANK OF INDIA"
    },
    {
        "bank_id": 247,
        "bank_name": "FATEHPUR DISTRICT COOPERATIVE BANK"
    },
    {
        "bank_id": 259,
        "bank_name": "FEDERAL BANK"
    },
    {
        "bank_id": 1794,
        "bank_name": "FINANCIAL COOPERATIVE BANK "
    },
    {
        "bank_id": 260,
        "bank_name": "FINCARE SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 261,
        "bank_name": "FINO PAYMENTS BANK LIMITED"
    },
    {
        "bank_id": 262,
        "bank_name": "FIROZABAD DISTRICT CENTRAL COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 120,
        "bank_name": "FIROZABAD ZILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 263,
        "bank_name": "FIRSTRAND BANK LIMITED"
    },
    {
        "bank_id": 1941,
        "bank_name": "Fingrowth Cooperative Bank Ltd"
    },
    {
        "bank_id": 739,
        "bank_name": "GAJANAN NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1792,
        "bank_name": "GANDHI COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 1789,
        "bank_name": "GANDHIBAGH SAHAKARI BANK "
    },
    {
        "bank_id": 265,
        "bank_name": "GANDHIDHAM COOPERATIVE BANK"
    },
    {
        "bank_id": 1790,
        "bank_name": "GANDHIDHAM MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 571,
        "bank_name": "GANDHINAGAR NAG. COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 574,
        "bank_name": "GANRAJ NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1793,
        "bank_name": "GARHA COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1550,
        "bank_name": "GAUTAM SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 565,
        "bank_name": "GHOGHAMBA VIBHAG NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1791,
        "bank_name": "GODAVARI LAXMI COOPERATIVE BANK "
    },
    {
        "bank_id": 1017,
        "bank_name": "GODAVARI LAXMI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1787,
        "bank_name": "GODAVARI URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 573,
        "bank_name": "GODAVARI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 114,
        "bank_name": "GODHRA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 738,
        "bank_name": "GOMTI NAGARIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 569,
        "bank_name": "GONDAL NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 264,
        "bank_name": "GOPINATH PATIL PARSIK BANK"
    },
    {
        "bank_id": 1571,
        "bank_name": "GUARDIAN BANK"
    },
    {
        "bank_id": 1018,
        "bank_name": "GUJARAT AMBUJA COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 572,
        "bank_name": "GUJARAT MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1398,
        "bank_name": "GULBARGA YADAGIR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 266,
        "bank_name": "GULSHAN MERCANTILE URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 116,
        "bank_name": "GUNA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 267,
        "bank_name": "GURGAON GRAMIN BANK"
    },
    {
        "bank_id": 268,
        "bank_name": "HADAGALI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 269,
        "bank_name": "HAMIRPUR DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 111,
        "bank_name": "HANAMASAGAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1490,
        "bank_name": "HANUMANGARH KENDRIYA SAHAKARI BANK"
    },
    {
        "bank_id": 270,
        "bank_name": "HARDOI DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 271,
        "bank_name": "HARDOI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 737,
        "bank_name": "HARIHARESHWAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 112,
        "bank_name": "HASSAN DISTRICT COOPERATIVE CENTRAL BANK"
    },
    {
        "bank_id": 1784,
        "bank_name": "HAVELI SAHAKARI BANK "
    },
    {
        "bank_id": 309,
        "bank_name": "HDFC BANK"
    },
    {
        "bank_id": 576,
        "bank_name": "HDFC BANK LIMITED, EASTERN & NORTH EAST FRONTIER R"
    },
    {
        "bank_id": 532,
        "bank_name": "HDFC BANK LIMITED, KRISHNA BHIMA SAMRUDDHI LAB"
    },
    {
        "bank_id": 303,
        "bank_name": "HDFC BANK LIMITED, VAIJANATH APPA SARAF MARAT NSBL"
    },
    {
        "bank_id": 293,
        "bank_name": "HDFC BANK LIMITED, VASUNDHARA MAHILA N G B L AMBAJ"
    },
    {
        "bank_id": 1865,
        "bank_name": "HDFC BANK LTD CREDIT CARD"
    },
    {
        "bank_id": 1859,
        "bank_name": "HIMACHAL GRAMIN BANK"
    },
    {
        "bank_id": 653,
        "bank_name": "HIMACHAL PRADESH STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 832,
        "bank_name": "HIMATNAGAR NAGARIK SAHAKARI BANK"
    },
    {
        "bank_id": 1783,
        "bank_name": "HINDUSTAN SHIPYARD STAFF COOPERATIVE BANK"
    },
    {
        "bank_id": 654,
        "bank_name": "HSBC BANK"
    },
    {
        "bank_id": 1881,
        "bank_name": "HSBC CREDIT CARD"
    },
    {
        "bank_id": 736,
        "bank_name": "HUTATMA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 861,
        "bank_name": "HUTATMA SHAHKARI BANK LIMITED "
    },
    {
        "bank_id": 656,
        "bank_name": "ICICI BANK LIMITED"
    },
    {
        "bank_id": 663,
        "bank_name": "ICICI BANK LIMITED, VAISHYA NAGARI"
    },
    {
        "bank_id": 1866,
        "bank_name": "ICICI BANK LTD CREDIT CARD"
    },
    {
        "bank_id": 761,
        "bank_name": "IDBI BANK"
    },
    {
        "bank_id": 785,
        "bank_name": "IDBI BANK LIMITED,MHAISAL"
    },
    {
        "bank_id": 916,
        "bank_name": "IDFC BANK LIMITED"
    },
    {
        "bank_id": 918,
        "bank_name": "IDUKKI DISTRICT COOPERATIVE BANK"
    },
    {
        "bank_id": 917,
        "bank_name": "IDUKKI DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 919,
        "bank_name": "ILKAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1779,
        "bank_name": "IMPERIAL URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 920,
        "bank_name": "IMPHAL URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 732,
        "bank_name": "INDAPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 559,
        "bank_name": "INDEPEDENCE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1858,
        "bank_name": "INDIA POST PAYMENT BANK"
    },
    {
        "bank_id": 921,
        "bank_name": "INDIAN BANK"
    },
    {
        "bank_id": 924,
        "bank_name": "INDIAN OVERSEAS BANK"
    },
    {
        "bank_id": 1867,
        "bank_name": "INDIAN OVERSEAS BANK CREDIT CARD"
    },
    {
        "bank_id": 556,
        "bank_name": "INDIRA  MAHILA  SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1014,
        "bank_name": "INDIRA MAHILA NAGARI SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 734,
        "bank_name": "INDIRA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1013,
        "bank_name": "INDIRA MAHILA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1782,
        "bank_name": "INDORE CLOTH MKT COOPERATIVE BANK "
    },
    {
        "bank_id": 733,
        "bank_name": "INDORE PARASPAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 203,
        "bank_name": "INDORE PREMIER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 555,
        "bank_name": "INDORE SWAYAMSIDH MAHILA COOPERATIVE BANK"
    },
    {
        "bank_id": 110,
        "bank_name": "INDRAPRASTHA SEHKARI BANK LIMITED"
    },
    {
        "bank_id": 558,
        "bank_name": "INDRAYANI COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 735,
        "bank_name": "INDRAYANI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 927,
        "bank_name": "INDUSIND BANK"
    },
    {
        "bank_id": 942,
        "bank_name": "INDUSTRIAL AND COMMERCIAL BANK OF CHINA LIMITED"
    },
    {
        "bank_id": 943,
        "bank_name": "INDUSTRIAL BANK OF KOREA"
    },
    {
        "bank_id": 1860,
        "bank_name": "ING VYSYA BANK LTD"
    },
    {
        "bank_id": 1781,
        "bank_name": "INNOVATIVE COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 553,
        "bank_name": "INTEGRAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 923,
        "bank_name": "IOB PANDYAN GRAMA BANK"
    },
    {
        "bank_id": 554,
        "bank_name": "IRINJALAKUDA TOWN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1900,
        "bank_name": "IndusInd Bank CREDIT CARD"
    },
    {
        "bank_id": 1626,
        "bank_name": "J C COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 907,
        "bank_name": "JABALPUR MAHILA NAGRIK SHAKARI BANK"
    },
    {
        "bank_id": 944,
        "bank_name": "JAGRUTI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1012,
        "bank_name": "JAI BHAVANI SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 537,
        "bank_name": "JAI TULJA BHAVANI UR BANK COOPERATIVE LIMITED "
    },
    {
        "bank_id": 730,
        "bank_name": "JAIPRAKASH NARAYAN NAGRI SAHAKARI BANK"
    },
    {
        "bank_id": 945,
        "bank_name": "JALAUN DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 946,
        "bank_name": "JALGAON JANATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 786,
        "bank_name": "JALNA DIST CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 547,
        "bank_name": "JALNA MERCHANTS COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 552,
        "bank_name": "JALORE NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 947,
        "bank_name": "JAMIA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 948,
        "bank_name": "JAMMU AND KASHMIR BANK LIMITED"
    },
    {
        "bank_id": 109,
        "bank_name": "JAMMU AND KASHMIR GRAMEEN BANK"
    },
    {
        "bank_id": 1348,
        "bank_name": "JAMNAGAR DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 949,
        "bank_name": "JAMPETA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1914,
        "bank_name": "JANA SMALL FINANCE BANK LTD"
    },
    {
        "bank_id": 549,
        "bank_name": "JANAKALYAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 950,
        "bank_name": "JANAKALYAN SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1775,
        "bank_name": "JANALAXMI COOPERATIVE BANK "
    },
    {
        "bank_id": 1778,
        "bank_name": "JANASEVA COOPERATIVE BANK "
    },
    {
        "bank_id": 951,
        "bank_name": "JANASEVA SAHAKARI BANK BORIVLI LIMITED"
    },
    {
        "bank_id": 952,
        "bank_name": "JANASEVA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 550,
        "bank_name": "JANATA COOPERATIVE BANK LIMITED, MALEGAON"
    },
    {
        "bank_id": 107,
        "bank_name": "JANATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1553,
        "bank_name": "JANATA SAHAKARI BANK LIMITED AMRAVATI"
    },
    {
        "bank_id": 953,
        "bank_name": "JANATHA SEVA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 535,
        "bank_name": "JANKALYAN URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 543,
        "bank_name": "JANSEVA NAGARI SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 536,
        "bank_name": "JANSEWA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 104,
        "bank_name": "JANSEWA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 729,
        "bank_name": "JANTA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 728,
        "bank_name": "JANTA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 551,
        "bank_name": "JATH URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 860,
        "bank_name": "JAWAHAR SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 727,
        "bank_name": "JAYSINGPUR UDGAON SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1506,
        "bank_name": "JHALAWAR KENDRIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1854,
        "bank_name": "JHARKHAND GRAMIN BANK"
    },
    {
        "bank_id": 774,
        "bank_name": "JHARKHAND STATE COOPERATIVE BANK "
    },
    {
        "bank_id": 541,
        "bank_name": "JHARNESHWAR NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1505,
        "bank_name": "JHUNJHUNU KENDRIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 546,
        "bank_name": "JIJAMATA MAHILA NAG SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 882,
        "bank_name": "JIJAMATA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 545,
        "bank_name": "JIJAMATA MAHILA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1129,
        "bank_name": "JIJAU COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 106,
        "bank_name": "JILA SAHAKARI KENDRIYA BANK"
    },
    {
        "bank_id": 202,
        "bank_name": "JILA SAHAKARI KENDRIYA BANK "
    },
    {
        "bank_id": 803,
        "bank_name": "JIVAJI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1776,
        "bank_name": "JIVAN COMM COOPERATIVE BANK "
    },
    {
        "bank_id": 955,
        "bank_name": "JIVAN COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 544,
        "bank_name": "JODHPUR NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1777,
        "bank_name": "JOGINDRA CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 956,
        "bank_name": "JP MORGAN BANK"
    },
    {
        "bank_id": 105,
        "bank_name": "JUBILEE HILLS MERCANTILE COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1347,
        "bank_name": "JUNAGADH JILLA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 94,
        "bank_name": "KADUTHURUTHY URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1772,
        "bank_name": "KAIRA DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 957,
        "bank_name": "KALLAPPANNA AWADE ICHALKARANJI JANATA SAHAKARI BAN"
    },
    {
        "bank_id": 958,
        "bank_name": "KALPARUKSHA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 959,
        "bank_name": "KALUPUR COMMERCIAL COOPERATIVE BANK"
    },
    {
        "bank_id": 961,
        "bank_name": "KALYAN JANATA SAHAKARI BANK"
    },
    {
        "bank_id": 512,
        "bank_name": "KALYANSAGAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 962,
        "bank_name": "KAMALA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1399,
        "bank_name": "KANARA DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1051,
        "bank_name": "KANKARIA MANINAGAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 963,
        "bank_name": "KANNUR DISTRICT  COOPERATIVE BANK"
    },
    {
        "bank_id": 827,
        "bank_name": "KANNUR DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 720,
        "bank_name": "KANPUR ZILLA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 964,
        "bank_name": "KAPOL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 965,
        "bank_name": "KARAMANA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 514,
        "bank_name": "KARAN URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1764,
        "bank_name": "KARMALA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 99,
        "bank_name": "KARNALA NAGARI SAHAKARI BANK"
    },
    {
        "bank_id": 966,
        "bank_name": "KARNATAKA BANK LIMITED"
    },
    {
        "bank_id": 1400,
        "bank_name": "KARNATAKA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 131,
        "bank_name": "KARNATAKA MAHILA SAHAKARI BANK"
    },
    {
        "bank_id": 967,
        "bank_name": "KARNATAKA VIKAS GRAMIN BANK"
    },
    {
        "bank_id": 968,
        "bank_name": "KARUR VYSYA BANK"
    },
    {
        "bank_id": 1849,
        "bank_name": "KASHI GOMTI SAMYUT GRAMIN BANK"
    },
    {
        "bank_id": 509,
        "bank_name": "KASHIPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 533,
        "bank_name": "KASHMIR MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1345,
        "bank_name": "KATCH DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1774,
        "bank_name": "KATIHAR DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1845,
        "bank_name": "KAVERI KALPATARU GRAMIN BANK"
    },
    {
        "bank_id": 511,
        "bank_name": "KAVITA URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 969,
        "bank_name": "KEB Hana Bank"
    },
    {
        "bank_id": 723,
        "bank_name": "KEDARNATH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 823,
        "bank_name": "KEMPEGOWDA PATTANA SOUHARDA SAHAKARI BANK "
    },
    {
        "bank_id": 970,
        "bank_name": "KEONJHAR CENTRAL COOOPERATIVE BANK"
    },
    {
        "bank_id": 971,
        "bank_name": "KERALA GRAMIN BANK"
    },
    {
        "bank_id": 724,
        "bank_name": "KHALILABAD NAGAR SAHAKARI BANK LIMITED ICICI BANK"
    },
    {
        "bank_id": 1771,
        "bank_name": "KHALILABAD NAGAR SAHAKARI BANK YES BANK"
    },
    {
        "bank_id": 518,
        "bank_name": "KHAMGAON URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 972,
        "bank_name": "KHARDAH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 523,
        "bank_name": "KHATRA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1773,
        "bank_name": "KHATTRI COOPERATIVE URBAN BANK "
    },
    {
        "bank_id": 1770,
        "bank_name": "KHORDA CCB MAHILA BANK "
    },
    {
        "bank_id": 1769,
        "bank_name": "KHORDA CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 908,
        "bank_name": "KHORDHA CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 98,
        "bank_name": "KISAN NAGRI SAHAKARI BANK"
    },
    {
        "bank_id": 1403,
        "bank_name": "KODAGU CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1346,
        "bank_name": "KODINAR TALUKA COOPERATIVE BANKING UNION LIMITED "
    },
    {
        "bank_id": 974,
        "bank_name": "KODOLI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 521,
        "bank_name": "KOHINOOR SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1010,
        "bank_name": "KOKAN MERCANTILE COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1410,
        "bank_name": "KOLAR CHIKKABALLAPUR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 809,
        "bank_name": "KOLHAPUR DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 529,
        "bank_name": "KOLHAPUR MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 975,
        "bank_name": "KOLKATA POLICE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 976,
        "bank_name": "KONOKLOTA MAHILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1767,
        "bank_name": "KOTA MAHILA NAGRIK BANK "
    },
    {
        "bank_id": 527,
        "bank_name": "KOTA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1868,
        "bank_name": "KOTAK MAHINDRA BANK CREDIT CARD"
    },
    {
        "bank_id": 989,
        "bank_name": "KOTAK MAHINDRA BANK LIMITED"
    },
    {
        "bank_id": 520,
        "bank_name": "KOTESHWARA SAHAKARI BANK "
    },
    {
        "bank_id": 102,
        "bank_name": "KOTTAKKAL COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1026,
        "bank_name": "KOTTAYAM COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1027,
        "bank_name": "KOTTAYAM DISTRICT COOPERATIVE BANK"
    },
    {
        "bank_id": 800,
        "bank_name": "KOYANA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1028,
        "bank_name": "KOZHIKODE DISTRICT COOPERATIAVE BANK LIMITED"
    },
    {
        "bank_id": 1901,
        "bank_name": "KRISHNA GRAMEENA BANK"
    },
    {
        "bank_id": 101,
        "bank_name": "KRISHNA MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1541,
        "bank_name": "KRISHNA PATTANA SAHAKAR BANK NIYAMITHA"
    },
    {
        "bank_id": 801,
        "bank_name": "KRISHNA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 516,
        "bank_name": "KRISHNA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 515,
        "bank_name": "KRUSHISEVA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 808,
        "bank_name": "KUMBHI KASARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1128,
        "bank_name": "KURLA N S BANK "
    },
    {
        "bank_id": 1029,
        "bank_name": "KUTCH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1030,
        "bank_name": "KUTTIADY COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1919,
        "bank_name": "Kaveri Grameena Bank"
    },
    {
        "bank_id": 719,
        "bank_name": "LAKHIMPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 508,
        "bank_name": "LALA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 507,
        "bank_name": "LALBAUG COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1842,
        "bank_name": "LANGPI DEHANGI RURAL BANK"
    },
    {
        "bank_id": 1031,
        "bank_name": "LATUR DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1763,
        "bank_name": "LAXMI MAHILA NAG SAHAKARI BANK "
    },
    {
        "bank_id": 506,
        "bank_name": "LAXMI MAHILA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 91,
        "bank_name": "LAXMI SAHAKARI BANK"
    },
    {
        "bank_id": 717,
        "bank_name": "LAXMI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1032,
        "bank_name": "LAXMI VILAS BANK"
    },
    {
        "bank_id": 503,
        "bank_name": "LAXMI VISHNU SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 718,
        "bank_name": "LAXMIBAI MAHILA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1033,
        "bank_name": "LIC COOPERATIVE BANK"
    },
    {
        "bank_id": 1034,
        "bank_name": "LIC EMPLOYEES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1035,
        "bank_name": "LIC OF INDIA STAFF COOPERATIVE BANK"
    },
    {
        "bank_id": 1036,
        "bank_name": "LILUAH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1037,
        "bank_name": "LOKMANGAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 93,
        "bank_name": "LOKNETE DATTAJI PATIL SAHAKARI BANK"
    },
    {
        "bank_id": 833,
        "bank_name": "LOKNETE DATTAJI PATIL SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1762,
        "bank_name": "LOKVIKAS NAGARI SAHAKARI BANK "
    },
    {
        "bank_id": 504,
        "bank_name": "LONAVALA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1127,
        "bank_name": "LUCKNOW URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 92,
        "bank_name": "LUNAWADA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1897,
        "bank_name": "Lakshmi Vilas bank"
    },
    {
        "bank_id": 1038,
        "bank_name": "M S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1039,
        "bank_name": "M.D. PAWAR PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 205,
        "bank_name": "M.P. RAJYA SAHAKARI BANK "
    },
    {
        "bank_id": 711,
        "bank_name": "MAA SHARDA MAHILA NAGRIK BANK"
    },
    {
        "bank_id": 475,
        "bank_name": "MADHESHWARI URBAN  DEV COOPERATIVE BANK"
    },
    {
        "bank_id": 1040,
        "bank_name": "MADHYA BHARAT GRAMIN BANK"
    },
    {
        "bank_id": 1850,
        "bank_name": "MADHYA BIHAR GRAMIN BANK"
    },
    {
        "bank_id": 820,
        "bank_name": "MAGADH CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1041,
        "bank_name": "MAHABHAIRAB COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1042,
        "bank_name": "MAHALAKSHMI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1931,
        "bank_name": "MAHANAGAR CO-OP BANK LTD"
    },
    {
        "bank_id": 1043,
        "bank_name": "MAHANAGAR COOPERATIVE BANK"
    },
    {
        "bank_id": 1756,
        "bank_name": "MAHANAGAR NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 712,
        "bank_name": "MAHARANA PRATAP COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1044,
        "bank_name": "MAHARASHTRA GRAMIN BANK"
    },
    {
        "bank_id": 1045,
        "bank_name": "MAHARASHTRA STATE COOPERATIVE BANK"
    },
    {
        "bank_id": 491,
        "bank_name": "MAHATAMA FULE DIST URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1046,
        "bank_name": "MAHATAMA FULE DISTRICT URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 490,
        "bank_name": "MAHATMA FULE DIST UR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 492,
        "bank_name": "MAHAVEER COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 164,
        "bank_name": "MAHEMDAVAD URBAN PEOPLES COOPERATIVE BANK"
    },
    {
        "bank_id": 1126,
        "bank_name": "MAHESH SAHAKARI BANK "
    },
    {
        "bank_id": 496,
        "bank_name": "MAHESH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 81,
        "bank_name": "MAHESH URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 481,
        "bank_name": "MAHESH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 710,
        "bank_name": "MAHESH URBAN COP BANK LIMITED"
    },
    {
        "bank_id": 1624,
        "bank_name": "MAHILA COOPERATIVE BANK"
    },
    {
        "bank_id": 322,
        "bank_name": "MAHILA COOPERATIVE NAGARIK BANK LIMITED"
    },
    {
        "bank_id": 488,
        "bank_name": "MAHILA NAGRIK SAHA BANK "
    },
    {
        "bank_id": 483,
        "bank_name": "MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1754,
        "bank_name": "MAHILA SAMRIDHI BANK "
    },
    {
        "bank_id": 714,
        "bank_name": "MAHISHMATI NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1047,
        "bank_name": "MAHOBA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1757,
        "bank_name": "MAKARPURA IND EST COOPERATIVE BANK "
    },
    {
        "bank_id": 501,
        "bank_name": "MALAD SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1048,
        "bank_name": "MALAPPURAM DISTRICT COOPERATIVE BANK"
    },
    {
        "bank_id": 476,
        "bank_name": "MALVIYA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 478,
        "bank_name": "MALVIYA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1049,
        "bank_name": "MALWA GRAMIN BANK"
    },
    {
        "bank_id": 1755,
        "bank_name": "MAMASAHEB PAWAR SATYAVIJAY COOPERATIVE BANK "
    },
    {
        "bank_id": 1404,
        "bank_name": "MANDYA DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1050,
        "bank_name": "MANGAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 85,
        "bank_name": "MANGALDAI NAGAR SAMABAI BANK LIMITED"
    },
    {
        "bank_id": 1903,
        "bank_name": "MANIPUR RURAL BANK"
    },
    {
        "bank_id": 1904,
        "bank_name": "MANIPUR RURAL BANK"
    },
    {
        "bank_id": 1052,
        "bank_name": "MANJERI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 500,
        "bank_name": "MANMAD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 794,
        "bank_name": "MANN DESHI MAHILA SAHAKARI BANK LIMITED, MHASWAD"
    },
    {
        "bank_id": 1761,
        "bank_name": "MANNDESHI MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 499,
        "bank_name": "MANORAMA COOPERATIVE.BANK LIMITED"
    },
    {
        "bank_id": 1698,
        "bank_name": "MANSA NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 1133,
        "bank_name": "MANSAROVAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1053,
        "bank_name": "MANSING COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1007,
        "bank_name": "MANTHA URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 484,
        "bank_name": "MANVI PATTANA SOUH SAHAKARI BANK"
    },
    {
        "bank_id": 497,
        "bank_name": "MANWATH UR COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 716,
        "bank_name": "MANWATH URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 881,
        "bank_name": "MARATHA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 713,
        "bank_name": "MARKANDEY NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1315,
        "bank_name": "MARKETYARD COMM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1054,
        "bank_name": "MASHREQ BANK"
    },
    {
        "bank_id": 709,
        "bank_name": "MATHURA ZILLA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1759,
        "bank_name": "MAYURBHANJ CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1760,
        "bank_name": "MEGHALAYA COOPERATIVE APEX BANK "
    },
    {
        "bank_id": 1841,
        "bank_name": "MEGHALAYA RURAL BANK"
    },
    {
        "bank_id": 1344,
        "bank_name": "MEHSANA DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1055,
        "bank_name": "MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 87,
        "bank_name": "MERCHANTS LIBERAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1906,
        "bank_name": "MEWAR AANCHALIK GRAMIN BANK"
    },
    {
        "bank_id": 819,
        "bank_name": "MIDNAPORE PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1056,
        "bank_name": "MILLATH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1057,
        "bank_name": "MIZORAM COOPERATIVE APEX BANK LIMITED"
    },
    {
        "bank_id": 1840,
        "bank_name": "MIZORAM RURAL BANK"
    },
    {
        "bank_id": 1058,
        "bank_name": "MIZUHO BANK LIMITED"
    },
    {
        "bank_id": 487,
        "bank_name": "MODEL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 814,
        "bank_name": "MOGAVEERA COOPERATIVE BANK"
    },
    {
        "bank_id": 1059,
        "bank_name": "MOHAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 472,
        "bank_name": "MOHOL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 486,
        "bank_name": "MOHOL URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1758,
        "bank_name": "MONGHYR DCC BANK LIMITED"
    },
    {
        "bank_id": 1060,
        "bank_name": "MONGHYR JAMUI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1061,
        "bank_name": "MUDGAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1062,
        "bank_name": "MUGBERIA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1063,
        "bank_name": "MUKTAI COOPERATIVE BANK LIMITED NIPHAD"
    },
    {
        "bank_id": 474,
        "bank_name": "MUKTAI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1625,
        "bank_name": "MURSHIDABAD DIST CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 829,
        "bank_name": "MUZAFFARPUR CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1405,
        "bank_name": "MYSORE CHAMARAJANAGAR COOPERATIVE BANK"
    },
    {
        "bank_id": 1564,
        "bank_name": "MYSORE MERCH COOPERATIVE BANK"
    },
    {
        "bank_id": 1008,
        "bank_name": "MYSORE SILK CLOTH MERCHANT COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 868,
        "bank_name": "MYSORE ZILLA MAHILA SAHAKARA BANK "
    },
    {
        "bank_id": 1753,
        "bank_name": "Mizoram Urban COOPERATIVE Development Bank"
    },
    {
        "bank_id": 866,
        "bank_name": "NADAPURAM COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1064,
        "bank_name": "NADIA DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1839,
        "bank_name": "NAGALAND RURAL BANK"
    },
    {
        "bank_id": 1751,
        "bank_name": "NAGAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 877,
        "bank_name": "NAGAR SAHAKARI BANK, BANK OF INDIA"
    },
    {
        "bank_id": 1742,
        "bank_name": "NAGAR SAHAKARI BANK, YES BANK"
    },
    {
        "bank_id": 1929,
        "bank_name": "NAGAR URBAN CO OPERATIVE BANK"
    },
    {
        "bank_id": 1065,
        "bank_name": "NAGAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1741,
        "bank_name": "NAGAR VIKAS SAHAKARI BANK "
    },
    {
        "bank_id": 458,
        "bank_name": "NAGARIK SAHAKARI BANK "
    },
    {
        "bank_id": 888,
        "bank_name": "NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 461,
        "bank_name": "NAGARIK SAMABAY BANK LIMITED"
    },
    {
        "bank_id": 1066,
        "bank_name": "NAGAUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 466,
        "bank_name": "NAGINA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 456,
        "bank_name": "NAGNATH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1067,
        "bank_name": "NAGPUR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 40,
        "bank_name": "NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 457,
        "bank_name": "NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 1857,
        "bank_name": "NAINITAL ALMORA KSHETRIYA GRAMIN BANK"
    },
    {
        "bank_id": 1748,
        "bank_name": "NAKODAR HINDU URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1068,
        "bank_name": "NALANDA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 74,
        "bank_name": "NALBARI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 460,
        "bank_name": "NANDANI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 78,
        "bank_name": "NANDED DISCTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1909,
        "bank_name": "NARMADA JHABUA GRAMIN BANK"
    },
    {
        "bank_id": 1926,
        "bank_name": "NARMADA MALWA GB-INDORE BR"
    },
    {
        "bank_id": 704,
        "bank_name": "NARODA NAGRIK COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 468,
        "bank_name": "NASHIK DIST GIRNA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1780,
        "bank_name": "NASHIK DISTT IMC BANK "
    },
    {
        "bank_id": 1747,
        "bank_name": "NASHIK JILHA MAHILA BANK "
    },
    {
        "bank_id": 463,
        "bank_name": "NASHIK JILHA MAHILA VIKAS SAHAKARI BANK"
    },
    {
        "bank_id": 1744,
        "bank_name": "NASHIK RD DEOLALI BANK "
    },
    {
        "bank_id": 1745,
        "bank_name": "NASHIK RD DEOLALI VYAPARI SAHAKARI BANK"
    },
    {
        "bank_id": 1740,
        "bank_name": "NASHIK ZILHA S AND P KARMACHARI BANK"
    },
    {
        "bank_id": 1069,
        "bank_name": "NATIONAL AUSTRALIA BANK LIMITED"
    },
    {
        "bank_id": 1070,
        "bank_name": "NATIONAL BANK OF ABU DHABI PJSC"
    },
    {
        "bank_id": 1125,
        "bank_name": "NATIONAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1071,
        "bank_name": "NATIONAL URBAN COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1899,
        "bank_name": "NATIONAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1005,
        "bank_name": "NAVABHARAT COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 454,
        "bank_name": "NAVANAGARA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 848,
        "bank_name": "NAVI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1746,
        "bank_name": "NAVNIRMAN COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 464,
        "bank_name": "NAVSARJAN INDUSTRIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1749,
        "bank_name": "NE EC RLY EMP PRIMARY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 467,
        "bank_name": "NEELA KRISHNA COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1072,
        "bank_name": "NELLORE COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1497,
        "bank_name": "NEW DHAN MANDI RAI SINGH NAGAR SAHAKARI BANK "
    },
    {
        "bank_id": 1073,
        "bank_name": "NEW INDIA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 705,
        "bank_name": "NIDHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 826,
        "bank_name": "NILESHWAR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1074,
        "bank_name": "NILKANTH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 471,
        "bank_name": "NIRMAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 706,
        "bank_name": "NISHIGANDHA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 459,
        "bank_name": "NISHIGANDHA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1189,
        "bank_name": "NIZAMABAD DISTRICT COOPERATIVE CENTRAL BANK LIMITE"
    },
    {
        "bank_id": 1075,
        "bank_name": "NKGSB COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1076,
        "bank_name": "NOBLE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 938,
        "bank_name": "NOIDA COMMERCIAL COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 707,
        "bank_name": "NORTH EAST SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 1077,
        "bank_name": "NORTH MALABAR GRAMIN BANK"
    },
    {
        "bank_id": 77,
        "bank_name": "NORTHERN RAILWAY PRIMARY COOPERATIVE BANK"
    },
    {
        "bank_id": 1743,
        "bank_name": "NORTHERN RLY PR COOPERATIVE BANK"
    },
    {
        "bank_id": 1942,
        "bank_name": "NSDL Payments Bank Limited"
    },
    {
        "bank_id": 1078,
        "bank_name": "NUTAN NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 802,
        "bank_name": "NUTAN SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 76,
        "bank_name": "NYAYAMITRA SAHAKARA BANK"
    },
    {
        "bank_id": 1923,
        "bank_name": "Nainital District Cooperative Bank"
    },
    {
        "bank_id": 451,
        "bank_name": "ODE URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 922,
        "bank_name": "ODISHA GRAMEEN BANK"
    },
    {
        "bank_id": 1739,
        "bank_name": "OJHAR MERCHANTS BANK "
    },
    {
        "bank_id": 1079,
        "bank_name": "OMAN INTERNATIONAL BANK SAOG"
    },
    {
        "bank_id": 702,
        "bank_name": "OMERGA JANTA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 449,
        "bank_name": "OMKAR NAGARIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1738,
        "bank_name": "OMKAR NAGREEYA SAHAKARI BANK KAUSHALPURI"
    },
    {
        "bank_id": 1080,
        "bank_name": "ORIENTAL BANK OF COMMERCE"
    },
    {
        "bank_id": 1802,
        "bank_name": "OSMANABAD DIST CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1556,
        "bank_name": "PADMASHREE DR. VITTHALRAO VIKHE PATIL COOPERATIVE "
    },
    {
        "bank_id": 448,
        "bank_name": "PADMAVATHI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 71,
        "bank_name": "PALAKKAD DISTRICT  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 72,
        "bank_name": "PALAMOOR COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1081,
        "bank_name": "PALI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 70,
        "bank_name": "PALUS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1733,
        "bank_name": "PANCHKULA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1343,
        "bank_name": "PANCHMAHAL DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1732,
        "bank_name": "PANCHSHEEL COOPERATIVE BANK "
    },
    {
        "bank_id": 1731,
        "bank_name": "PANCHSHEEL MERC COOPERATIVE BANK "
    },
    {
        "bank_id": 1725,
        "bank_name": "PANIPAT URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1727,
        "bank_name": "PARASPAR SAHAYAK COOPERATIVE BANK "
    },
    {
        "bank_id": 1735,
        "bank_name": "PARBHANI DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 999,
        "bank_name": "PARNER TALUKA SAINIK SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 447,
        "bank_name": "PARSHWANATH COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1696,
        "bank_name": "PARWANOO URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 1082,
        "bank_name": "PASCHIM BANGA GRAMIN BANK"
    },
    {
        "bank_id": 1083,
        "bank_name": "PATAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1310,
        "bank_name": "PATAN NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 435,
        "bank_name": "PATAN NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1084,
        "bank_name": "PATLIPUTRA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 894,
        "bank_name": "PAVANA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 825,
        "bank_name": "PAYANGADI URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1085,
        "bank_name": "PAYTM PAYMENTS BANK LIMITED"
    },
    {
        "bank_id": 1086,
        "bank_name": "PAYYANUR COOPERATIVE TOWN BANK LIMITED"
    },
    {
        "bank_id": 1087,
        "bank_name": "PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 446,
        "bank_name": "PEOPLES COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 427,
        "bank_name": "PEOPLES URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1088,
        "bank_name": "PILIBHIT DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 440,
        "bank_name": "PIMPALGOAN MER COOPERATIVE BANK"
    },
    {
        "bank_id": 893,
        "bank_name": "PIMPRI CHINCHWAD SAHAKARI BANK "
    },
    {
        "bank_id": 766,
        "bank_name": "PITHORAGARH JILA SAHAKARI BANK"
    },
    {
        "bank_id": 767,
        "bank_name": "PITHORAGARH ZILA SAHAKARI BANK"
    },
    {
        "bank_id": 1737,
        "bank_name": "POCHAMPALLY COOPERATIVE BANK "
    },
    {
        "bank_id": 1089,
        "bank_name": "PONDICHERRY STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1090,
        "bank_name": "PONNAMPET TOWN COOPERATIVE BANK"
    },
    {
        "bank_id": 436,
        "bank_name": "POORNAWADI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 445,
        "bank_name": "PORBANDAR COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 426,
        "bank_name": "PORBANDAR VIBHAGIYA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1729,
        "bank_name": "POSTAL AND RMS EMP COOPERATIVE BANK "
    },
    {
        "bank_id": 1091,
        "bank_name": "PRAGATHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1092,
        "bank_name": "PRAGATHI KRISHNA GRAMIN BANK"
    },
    {
        "bank_id": 1730,
        "bank_name": "PRAGATI MAHILA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1728,
        "bank_name": "PRAGATI SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 433,
        "bank_name": "PRAGATI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1451,
        "bank_name": "PRATAP COOPERATIVE BANK "
    },
    {
        "bank_id": 1093,
        "bank_name": "PRATHAMA BANK"
    },
    {
        "bank_id": 793,
        "bank_name": "PRATHAMIC SHIKSHAK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 431,
        "bank_name": "PRAVARA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1094,
        "bank_name": "PRERANA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1000,
        "bank_name": "PRERNA NAGARI SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1095,
        "bank_name": "PRIME COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 437,
        "bank_name": "PRIYADARSHANI MAH NAG SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1001,
        "bank_name": "PRIYADARSHANI NAGARI SAHAKARI BANK "
    },
    {
        "bank_id": 1918,
        "bank_name": "PRIYADARSHANI NAGARI SAHAKARI BANK LTD"
    },
    {
        "bank_id": 429,
        "bank_name": "PRIYADARSHANI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 68,
        "bank_name": "PRIYADARSHINI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1002,
        "bank_name": "PROGRESSIVE COOPERATIVE BANK"
    },
    {
        "bank_id": 439,
        "bank_name": "PROGRESSIVE MERCANTILE COOPERATIVE BANK"
    },
    {
        "bank_id": 428,
        "bank_name": "PROGRESSIVE URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1096,
        "bank_name": "PT BANK MAYBANK INDONESIA TBK"
    },
    {
        "bank_id": 444,
        "bank_name": "PUNE CANTONMENT SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 442,
        "bank_name": "PUNE DISTRICT CENTRAL COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1907,
        "bank_name": "PUNE MERCHANTS CO-OPERATIVE BANK LTD"
    },
    {
        "bank_id": 1097,
        "bank_name": "PUNE MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 438,
        "bank_name": "PUNE MUNICIPALCORPSER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 783,
        "bank_name": "PUNE PEOPLES COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1569,
        "bank_name": "PUNE URBAN BANK"
    },
    {
        "bank_id": 1098,
        "bank_name": "PUNJAB AND MAHARSHTRA COOPERATIVE BANK"
    },
    {
        "bank_id": 1099,
        "bank_name": "PUNJAB AND SIND BANK"
    },
    {
        "bank_id": 1851,
        "bank_name": "PUNJAB GRAMIN BANK"
    },
    {
        "bank_id": 1100,
        "bank_name": "PUNJAB NATIONAL BANK"
    },
    {
        "bank_id": 1869,
        "bank_name": "PUNJAB NATIONAL BANK CREDIT CARD"
    },
    {
        "bank_id": 1734,
        "bank_name": "PURNEA DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1101,
        "bank_name": "PURVANCHAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1102,
        "bank_name": "PURVANCHAL GRAMIN BANK"
    },
    {
        "bank_id": 424,
        "bank_name": "QATAR NATIONAL BANK"
    },
    {
        "bank_id": 1453,
        "bank_name": "R S COOPERATIVE BANK "
    },
    {
        "bank_id": 1103,
        "bank_name": "RABOBANK INTERNATIONAL"
    },
    {
        "bank_id": 1104,
        "bank_name": "RAE BARELI DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1105,
        "bank_name": "RAICHUR DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 651,
        "bank_name": "RAIGAD SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 414,
        "bank_name": "RAIGARH NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1106,
        "bank_name": "RAILWAY EMPLOYEE COOPERATIVE BANK"
    },
    {
        "bank_id": 317,
        "bank_name": "RAIPUR URBAN MERCANTILE CO BANK LIMITED"
    },
    {
        "bank_id": 1107,
        "bank_name": "RAJADHANI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 698,
        "bank_name": "RAJAPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1889,
        "bank_name": "RAJARAM BAPU SAHAKARI BANK LTD"
    },
    {
        "bank_id": 857,
        "bank_name": "RAJARAMBAPU SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1108,
        "bank_name": "RAJARSHI SHAHU GOVERMENT SERVANTS COOPERATIVE BANK"
    },
    {
        "bank_id": 411,
        "bank_name": "RAJARSHI SHAHU SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1109,
        "bank_name": "RAJASTHAN MARUDHARA GRAMIN BANK"
    },
    {
        "bank_id": 1722,
        "bank_name": "RAJDHANI NAGAR SAHAKARI BANK"
    },
    {
        "bank_id": 1110,
        "bank_name": "RAJGURUNAGAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1342,
        "bank_name": "RAJKOT DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1111,
        "bank_name": "RAJKOT NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 836,
        "bank_name": "RAJKOT PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 67,
        "bank_name": "RAJMATA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 415,
        "bank_name": "RAJPUTANA MAHILA URB COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1720,
        "bank_name": "RAJSAMAND URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 1454,
        "bank_name": "RAMESHWAR COOPERATIVE BANK "
    },
    {
        "bank_id": 821,
        "bank_name": "RAMGARHIA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 699,
        "bank_name": "RAMPUR ZILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1721,
        "bank_name": "RAMRAJYA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1112,
        "bank_name": "RANAGHAT PEOPLES COOPERATIVE BANK"
    },
    {
        "bank_id": 416,
        "bank_name": "RANI LAXMIBAI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1113,
        "bank_name": "RANIGANJ COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 65,
        "bank_name": "RATANCHAND SHAH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 422,
        "bank_name": "RATNAGIRI DIST CENT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 781,
        "bank_name": "RATNAGIRI DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1114,
        "bank_name": "RATNAGIRI DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 420,
        "bank_name": "RAVI COMMERCIAL UR COP BANK LIMITED"
    },
    {
        "bank_id": 1723,
        "bank_name": "RAVI COMMERCIAL URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1115,
        "bank_name": "RBL BANK LIMITED"
    },
    {
        "bank_id": 856,
        "bank_name": "RENDAL SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 418,
        "bank_name": "RENUKA NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 1116,
        "bank_name": "RESERVE BANK OF INDIA"
    },
    {
        "bank_id": 66,
        "bank_name": "RUKMINI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1856,
        "bank_name": "RUSHIKULYA GRAMIN BANK"
    },
    {
        "bank_id": 1341,
        "bank_name": "SABARKANTHA DISTRICT CENTRAL COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 393,
        "bank_name": "SADGURU GAHININATH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 373,
        "bank_name": "SADGURU NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 403,
        "bank_name": "SADHANA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1117,
        "bank_name": "SAHEBRAO DESHMUKH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1566,
        "bank_name": "SAHYADRI  SAHAKARI BANK"
    },
    {
        "bank_id": 784,
        "bank_name": "SAHYOG URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 996,
        "bank_name": "SAHYOG URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 59,
        "bank_name": "SAIBABA NAGARI SAHAKARI  BANK LIMITED"
    },
    {
        "bank_id": 997,
        "bank_name": "SAIBABA NAGARI SAHAKARI BANK"
    },
    {
        "bank_id": 688,
        "bank_name": "SAMARTH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 366,
        "bank_name": "SAMARTH SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1702,
        "bank_name": "SAMARTH URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 682,
        "bank_name": "SAMARTH URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1118,
        "bank_name": "SAMATA COOPERATIVE DEVELOPMENT BANK"
    },
    {
        "bank_id": 1124,
        "bank_name": "SAMATA SAHAKARI BANK"
    },
    {
        "bank_id": 696,
        "bank_name": "SAMATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 992,
        "bank_name": "SAMATHA MAHILA COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 811,
        "bank_name": "SAMPADA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 910,
        "bank_name": "SAMRUDDHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1119,
        "bank_name": "SAMRUDDHI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 365,
        "bank_name": "SAMRUDDHI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1719,
        "bank_name": "SAMTA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 367,
        "bank_name": "SANAWAD NAGARIK SAHAKARI BANK "
    },
    {
        "bank_id": 765,
        "bank_name": "SANDUR PATTANA SOUHARDA SAHAKARI BANK"
    },
    {
        "bank_id": 1715,
        "bank_name": "SANGHAMITRA COOPERATIVE BANK "
    },
    {
        "bank_id": 1716,
        "bank_name": "SANGHAMITRA COOPERATIVE URBN BANK "
    },
    {
        "bank_id": 791,
        "bank_name": "SANGLI DISTRICT PRIMARY TEACHERS COOPERATIVE BANK "
    },
    {
        "bank_id": 55,
        "bank_name": "SANGLI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 350,
        "bank_name": "SANGLI URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1120,
        "bank_name": "SANGOLA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 54,
        "bank_name": "SANMATI SAHAKARI BANK"
    },
    {
        "bank_id": 685,
        "bank_name": "SANMATI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 383,
        "bank_name": "SANMITRA MAHILA NAG SAHAKARI BANK "
    },
    {
        "bank_id": 689,
        "bank_name": "SANMITRA MAHILA NAGRI SAHAKARI BANK"
    },
    {
        "bank_id": 370,
        "bank_name": "SANMITRA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 995,
        "bank_name": "SANMITRA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 408,
        "bank_name": "SANMITRA URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 357,
        "bank_name": "SANT SOPANKAKA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 58,
        "bank_name": "SARAKARI NAUKARARA SAHAKARI BANK"
    },
    {
        "bank_id": 378,
        "bank_name": "SARASPUR NAGARIK COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1295,
        "bank_name": "SARASPUR NAGARIK COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1121,
        "bank_name": "SARASWAT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 987,
        "bank_name": "SARASWATI SHAKARI BANK LIMITED "
    },
    {
        "bank_id": 136,
        "bank_name": "SARDAR BHILADWALA PARDI PEOPLE COOPERATIVE BANK"
    },
    {
        "bank_id": 395,
        "bank_name": "SARDAR GUNJ MERCAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 359,
        "bank_name": "SARDAR SINGH NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 343,
        "bank_name": "SARDAR VALLABHBHAI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1300,
        "bank_name": "SARDARGUNJ MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1855,
        "bank_name": "SARVA HARYANA GRAMIN BANK"
    },
    {
        "bank_id": 1848,
        "bank_name": "SARVA UP GRAMIN BANK"
    },
    {
        "bank_id": 817,
        "bank_name": "SARVODAYA COOPERATIVE BANK"
    },
    {
        "bank_id": 1912,
        "bank_name": "SARVODAYA SAH BANK"
    },
    {
        "bank_id": 1135,
        "bank_name": "SASARAM BHABHUA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1136,
        "bank_name": "SATLUJ GRAMIN BANK BATHINDA"
    },
    {
        "bank_id": 1893,
        "bank_name": "SATPURA NARMADA KSHETRIYA GRAMIN BANK"
    },
    {
        "bank_id": 1717,
        "bank_name": "SATYASHODHAK SAHAKARI BANK"
    },
    {
        "bank_id": 1137,
        "bank_name": "SAURASHTRA GRAMIN BANK"
    },
    {
        "bank_id": 1500,
        "bank_name": "SAWAI MADHOPUR KENDRIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 342,
        "bank_name": "SAWAI MADHOPUR URBAN COOPERATIVE LIMITED "
    },
    {
        "bank_id": 1138,
        "bank_name": "SAWANTWADI URBAN COPERATIVE BANK"
    },
    {
        "bank_id": 1139,
        "bank_name": "SBER BANK"
    },
    {
        "bank_id": 1134,
        "bank_name": "SBU- MERGED BANKS"
    },
    {
        "bank_id": 61,
        "bank_name": "SEC MERCANTILE COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 57,
        "bank_name": "SEHORE NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1141,
        "bank_name": "SEVEN HILLS COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1705,
        "bank_name": "SHAHADA PEOPLES COOPERATIVE BANK "
    },
    {
        "bank_id": 1142,
        "bank_name": "SHAHJAHANPUR DISTRICT CENTRAL COOPERATIVE BANK LIM"
    },
    {
        "bank_id": 991,
        "bank_name": "SHAJAPUR NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 382,
        "bank_name": "SHANKARRAO MOHITE PATIL SAHAKARI BANK"
    },
    {
        "bank_id": 797,
        "bank_name": "SHARAD NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 391,
        "bank_name": "SHARAD SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1143,
        "bank_name": "SHIGGAON URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1299,
        "bank_name": "SHIHORI NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 392,
        "bank_name": "SHIHORI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 368,
        "bank_name": "SHIKSHAK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 839,
        "bank_name": "SHILLONG COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1701,
        "bank_name": "SHIMLA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1408,
        "bank_name": "SHIMOGA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1144,
        "bank_name": "SHINHAN BANK"
    },
    {
        "bank_id": 47,
        "bank_name": "SHIVA SAHAKARI BANK"
    },
    {
        "bank_id": 369,
        "bank_name": "SHIVA SAHAKARI BANK "
    },
    {
        "bank_id": 1925,
        "bank_name": "SHIVAJI NAGARI PAITHAN"
    },
    {
        "bank_id": 406,
        "bank_name": "SHIVAJIRAO BHOSALE SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1145,
        "bank_name": "SHIVALIK MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 362,
        "bank_name": "SHIVAM COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1711,
        "bank_name": "SHIVAM SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 397,
        "bank_name": "SHIVDAULAT SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 38,
        "bank_name": "SHIVSHAKTI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 915,
        "bank_name": "SHRAMIK NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 880,
        "bank_name": "SHREE BASAVESHWAR COOPERATIVE BANK "
    },
    {
        "bank_id": 134,
        "bank_name": "SHREE BASAVESHWAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 903,
        "bank_name": "SHREE BASAVESHWAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1301,
        "bank_name": "SHREE BHAVNAGAR NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 837,
        "bank_name": "SHREE BOTAD MERCANTILE COOPERATIVE BANK"
    },
    {
        "bank_id": 1337,
        "bank_name": "SHREE BOTAD MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 398,
        "bank_name": "SHREE CHHANI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1146,
        "bank_name": "SHREE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1714,
        "bank_name": "SHREE DHARATI COOPERATIVE BANK "
    },
    {
        "bank_id": 1147,
        "bank_name": "SHREE DHARTI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 830,
        "bank_name": "SHREE GAJANAN LOKSEVA SAHAKARI BANK "
    },
    {
        "bank_id": 901,
        "bank_name": "SHREE GAJANAN URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 850,
        "bank_name": "SHREE GAVISIDDHESHWAR URBAN COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 567,
        "bank_name": "SHREE GVERDHNSNGH RAGUVNSHI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1766,
        "bank_name": "SHREE KADI NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 385,
        "bank_name": "SHREE LAXMI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1320,
        "bank_name": "SHREE LODRA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 993,
        "bank_name": "SHREE MAHAVIR SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 489,
        "bank_name": "SHREE MAHUVA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1296,
        "bank_name": "SHREE MORBI NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 62,
        "bank_name": "SHREE MURUGHARAJENDRA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1148,
        "bank_name": "SHREE PARSWANATH COOPERATIVE BANK"
    },
    {
        "bank_id": 364,
        "bank_name": "SHREE SAMARTH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1303,
        "bank_name": "SHREE SAVARKUNDLA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1302,
        "bank_name": "SHREE SAVLI  NAGRIK SAHAKARI  BANK LIMITED"
    },
    {
        "bank_id": 360,
        "bank_name": "SHREE SAVLI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1712,
        "bank_name": "SHREE SHARADA SAHAKARI BANK "
    },
    {
        "bank_id": 983,
        "bank_name": "SHREE TALAJA NAGARIK SAHA BANK LIMITED"
    },
    {
        "bank_id": 1149,
        "bank_name": "SHREE TUKARAM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1700,
        "bank_name": "SHREE VARDHAMAN BANK "
    },
    {
        "bank_id": 1277,
        "bank_name": "SHREE VIRPUR URBAN SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 680,
        "bank_name": "SHREE VYANKATESH COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 345,
        "bank_name": "SHREE VYAS DHANVARSHA SAHAKARI BANK"
    },
    {
        "bank_id": 341,
        "bank_name": "SHREE WARANA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1884,
        "bank_name": "SHREYAS GRAMIN BANK"
    },
    {
        "bank_id": 409,
        "bank_name": "SHRI ADINATH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 156,
        "bank_name": "SHRI ANAND COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 407,
        "bank_name": "SHRI ANAND NAGARI SAHAKARI BANK LIMITED, HDFC BANK"
    },
    {
        "bank_id": 1718,
        "bank_name": "SHRI ANAND NAGARI SAHAKARI BANK, YES BANK"
    },
    {
        "bank_id": 756,
        "bank_name": "SHRI ARIHANT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1150,
        "bank_name": "SHRI BALAJI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 139,
        "bank_name": "SHRI BARIA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 695,
        "bank_name": "SHRI BASAVESHWAR SAHAKARI BANK "
    },
    {
        "bank_id": 404,
        "bank_name": "SHRI BHAILALBHAI CONTRACTOR SMARAK COOPERATIVE BAN"
    },
    {
        "bank_id": 621,
        "bank_name": "SHRI BHARAT UR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 401,
        "bank_name": "SHRI BHAUSAHEB THORAT AMRUTVAHINI SAHAKARI BANK LI"
    },
    {
        "bank_id": 1151,
        "bank_name": "SHRI CHHATRAPATI RAJASHRI SHAHU URBAN COOPERATIVE"
    },
    {
        "bank_id": 1152,
        "bank_name": "SHRI D T PATIL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1015,
        "bank_name": "SHRI GAJANAN MAHARAJ URBAN COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1565,
        "bank_name": "SHRI GANESH SAHAKARI BANK"
    },
    {
        "bank_id": 394,
        "bank_name": "SHRI GANESH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 396,
        "bank_name": "SHRI GURUSIDDHESHWAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1298,
        "bank_name": "SHRI JANATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 835,
        "bank_name": "SHRI KADASIDDESHWAR PATTAN SAHAKARI BANK "
    },
    {
        "bank_id": 100,
        "bank_name": "SHRI KANYAKA NAGARI SAHAKARI BANK"
    },
    {
        "bank_id": 1558,
        "bank_name": "SHRI KRISHNA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1321,
        "bank_name": "SHRI LAXMI MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 384,
        "bank_name": "SHRI LAXMIKRUPA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1153,
        "bank_name": "SHRI MAHALAXMI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 83,
        "bank_name": "SHRI MAHALAXMI PATTAN SAHAKARA BANK"
    },
    {
        "bank_id": 60,
        "bank_name": "SHRI MAHANT SHIVAYOGI COOPERATIVE BANK"
    },
    {
        "bank_id": 379,
        "bank_name": "SHRI MAHAVIR URB COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 380,
        "bank_name": "SHRI MAHILA SEWA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 806,
        "bank_name": "SHRI PANCHGANGA NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 371,
        "bank_name": "SHRI PATNESHWAR URB COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 56,
        "bank_name": "SHRI PRAGATI PATTAN SAHAKARI BANK"
    },
    {
        "bank_id": 160,
        "bank_name": "SHRI REVANSIDDESHWAR SAHAKARI BANK"
    },
    {
        "bank_id": 988,
        "bank_name": "SHRI RUKHMINI SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 358,
        "bank_name": "SHRI SATYAVIJAY SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 355,
        "bank_name": "SHRI SAWAMI SAMARATH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 879,
        "bank_name": "SHRI SHANTAPPANNA MIRAJI URBAN COOPERATIVE BANK LI"
    },
    {
        "bank_id": 50,
        "bank_name": "SHRI SHARAN VEERESHWAR SAHAKARI BANK"
    },
    {
        "bank_id": 53,
        "bank_name": "SHRI SHIDDESHWAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1154,
        "bank_name": "SHRI SHIDDHESHWAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 344,
        "bank_name": "SHRI VAIBHAV LAKSHMI MAHILA NS BANK"
    },
    {
        "bank_id": 1155,
        "bank_name": "SHRI VEER PULIKESHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 300,
        "bank_name": "SHRI VEERSHAIV COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 46,
        "bank_name": "SHRI VIJAY MAHANTESH COOPERATIVE BANK"
    },
    {
        "bank_id": 807,
        "bank_name": "SHRI YASHWANT SAHAKARI BANK "
    },
    {
        "bank_id": 687,
        "bank_name": "SHRIMANT MALOJIRAJE SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 855,
        "bank_name": "SHRIPAL ALASE KURUNWAD URB COOPERATIVE BANK"
    },
    {
        "bank_id": 854,
        "bank_name": "SHRIPATRAODADA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 352,
        "bank_name": "SHRIRAM URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1708,
        "bank_name": "SHUBHLAKSHMI MAH COOPERATIVE BANK "
    },
    {
        "bank_id": 356,
        "bank_name": "SHUSHRUTI SOUAHRDA SAHAKRA BANK"
    },
    {
        "bank_id": 1156,
        "bank_name": "SIDDAGANGA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 390,
        "bank_name": "SIDDHESHWAR SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 692,
        "bank_name": "SIDDHESHWAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1157,
        "bank_name": "SIDDHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 561,
        "bank_name": "SIHOR MERCANTILE COOPERATIVE BANK"
    },
    {
        "bank_id": 1710,
        "bank_name": "SIHOR MERCANTILE COOPERATIVE BANK "
    },
    {
        "bank_id": 375,
        "bank_name": "SIHOR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1499,
        "bank_name": "SIKAR KENDRIYA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 351,
        "bank_name": "SIKAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1924,
        "bank_name": "SIKKIM STATE CO-OPERATIVE BANK LTD"
    },
    {
        "bank_id": 1703,
        "bank_name": "SIKKIM STATE COOPERATIVE BANK "
    },
    {
        "bank_id": 1158,
        "bank_name": "SIKKIMSTATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1709,
        "bank_name": "SIND COOPERATIVE URBAN BANK "
    },
    {
        "bank_id": 1159,
        "bank_name": "SINDHUDURG COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 388,
        "bank_name": "SINDHUDURG DIST CENT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 762,
        "bank_name": "SIR M VISHWESHARAIAH SAHAKAR BANK "
    },
    {
        "bank_id": 1160,
        "bank_name": "SIR M VISVESVARAYA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1578,
        "bank_name": "SIWAN CNETRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 381,
        "bank_name": "SMRITI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1161,
        "bank_name": "SOCIETE GENERALE BANK LIMITED"
    },
    {
        "bank_id": 1162,
        "bank_name": "SOLAPUR JANATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 389,
        "bank_name": "SOLAPUR SIDDHESHWAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 354,
        "bank_name": "SOLAPUR SOCIAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 402,
        "bank_name": "SONALI BANK LIMITED"
    },
    {
        "bank_id": 374,
        "bank_name": "SONBHADRA NAGAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 990,
        "bank_name": "SONPETH NAGARI SAHAKARI BANK"
    },
    {
        "bank_id": 898,
        "bank_name": "SOUBHAGYA MAHILA SOUHARDHA SAHAKARI BANK "
    },
    {
        "bank_id": 1163,
        "bank_name": "SOUTH INDIAN BANK"
    },
    {
        "bank_id": 934,
        "bank_name": "SREE CHARAN BANK "
    },
    {
        "bank_id": 1164,
        "bank_name": "SREE CHARAN SOUHARDHA COOPERATIVE BANK  LIMITED"
    },
    {
        "bank_id": 1549,
        "bank_name": "SREE MAHAYOGI LAKSHAMMA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 146,
        "bank_name": "SREE MAHAYOGI LAKSHMAMMA COOPERATIVE BANK"
    },
    {
        "bank_id": 1165,
        "bank_name": "SREE SUBRAMANYESWARA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1166,
        "bank_name": "SREE THYAGARAJA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 929,
        "bank_name": "SREENIDHI SOUH BANK"
    },
    {
        "bank_id": 930,
        "bank_name": "SREENIDHI SOUH SAHAK BANK "
    },
    {
        "bank_id": 1167,
        "bank_name": "SREENIVASA PADMAVATHI COOPERATIVE BANK"
    },
    {
        "bank_id": 64,
        "bank_name": "SRI AMBABHAVANI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 935,
        "bank_name": "SRI BANASHANKAR MAHILA COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 135,
        "bank_name": "SRI BASAVESHWAR PATTANA SAHAKARI BANK"
    },
    {
        "bank_id": 405,
        "bank_name": "SRI BHAGAVATHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 601,
        "bank_name": "SRI CHANNABASAVASWAMY BANK"
    },
    {
        "bank_id": 763,
        "bank_name": "SRI CHATRAPATI SHIVAJI SAHAKARI BANK"
    },
    {
        "bank_id": 1552,
        "bank_name": "SRI GANAPATHI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1168,
        "bank_name": "SRI GANESH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1169,
        "bank_name": "SRI GAYATRI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1170,
        "bank_name": "SRI GOKARNATH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 764,
        "bank_name": "SRI GURU RAGHAVENDRA SAHAKARA BANK "
    },
    {
        "bank_id": 691,
        "bank_name": "SRI KALIDASA SAHAKARA BANK "
    },
    {
        "bank_id": 387,
        "bank_name": "SRI KANNIKAPARAMESWARI COOPBANK LIMITED"
    },
    {
        "bank_id": 933,
        "bank_name": "SRI LAKSHMI MAHILA SAHAKARI BANK "
    },
    {
        "bank_id": 932,
        "bank_name": "SRI LAKSHMINARAYANA COOPERATIVE BANK "
    },
    {
        "bank_id": 1171,
        "bank_name": "SRI POTTI SRI RAMULU NELLORE DISTRICT COOPERATIVE "
    },
    {
        "bank_id": 1172,
        "bank_name": "SRI RAMA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1548,
        "bank_name": "SRI SATYA SAI NAGARIK SAHAKARI BANK"
    },
    {
        "bank_id": 51,
        "bank_name": "SRI SEETHARAGHAVA SOUHARDA SAHAKARI BANK"
    },
    {
        "bank_id": 1173,
        "bank_name": "SRI SHARADA MAHILA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 928,
        "bank_name": "SRI SHARADA MAHILA COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 52,
        "bank_name": "SRI SHIVESHWAR NAGRI SAHAKARI BANK"
    },
    {
        "bank_id": 1174,
        "bank_name": "SRI SUDHA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1175,
        "bank_name": "SRI VASAVAMBA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 931,
        "bank_name": "SRIMATHA MAHILA SAHAKARI BANK "
    },
    {
        "bank_id": 840,
        "bank_name": "SRIRAMANAGAR PATTANA SAHAKARA BANK "
    },
    {
        "bank_id": 361,
        "bank_name": "SSMS URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 49,
        "bank_name": "STAMBADRI COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1176,
        "bank_name": "STANDARD CHARTERED BANK"
    },
    {
        "bank_id": 1882,
        "bank_name": "STANDARD CHARTERED CREDIT CARD"
    },
    {
        "bank_id": 914,
        "bank_name": "STANDARD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1885,
        "bank_name": "STATE BANK OF HYDERABAD, DECCAN GRAMEENA BANK"
    },
    {
        "bank_id": 1177,
        "bank_name": "STATE BANK OF INDIA"
    },
    {
        "bank_id": 1870,
        "bank_name": "STATE BANK OF INDIA CREDIT CARD"
    },
    {
        "bank_id": 1905,
        "bank_name": "STATE BANK OF INDIA HYDERABAD"
    },
    {
        "bank_id": 1178,
        "bank_name": "STATE BANK OF MAURITIUS LIMITED"
    },
    {
        "bank_id": 776,
        "bank_name": "STATE TRANSPORT  BANK "
    },
    {
        "bank_id": 1456,
        "bank_name": "STATE TRANSPORT BANK MUMBAI CENTRAL"
    },
    {
        "bank_id": 775,
        "bank_name": "STATE TRANSPORT COOPERATIVE BANK "
    },
    {
        "bank_id": 353,
        "bank_name": "STERLING URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 386,
        "bank_name": "SUBHADRA LOCAL AREA BANK LIMITED"
    },
    {
        "bank_id": 348,
        "bank_name": "SUCO SOUHARDA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 347,
        "bank_name": "SUDHA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 681,
        "bank_name": "SULAIMANI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 410,
        "bank_name": "SUMERPUR MERC. URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1179,
        "bank_name": "SUMITOMO MITSUI BANKING CORPORATION"
    },
    {
        "bank_id": 1122,
        "bank_name": "SUNDARLAL SAVJI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1123,
        "bank_name": "SUNDARLAL SAWJI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1707,
        "bank_name": "SURAT MERC COOPERATIVE BANK "
    },
    {
        "bank_id": 377,
        "bank_name": "SURAT NATIONAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1340,
        "bank_name": "SURENDRANAGAR DISTRICT CENTRAL COOPERATIVE BANK LI"
    },
    {
        "bank_id": 1180,
        "bank_name": "SURYODAY SMALL FINANCE BANK LIMITED"
    },
    {
        "bank_id": 1181,
        "bank_name": "SUTEX COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1182,
        "bank_name": "SUVARNA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 346,
        "bank_name": "SUVARNAYUG SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 871,
        "bank_name": "SWARNA BHARATHI SAHAKARA BANK "
    },
    {
        "bank_id": 1183,
        "bank_name": "SYNDICATE BANK"
    },
    {
        "bank_id": 1871,
        "bank_name": "SYNDICATE BANK CREDIT CARD"
    },
    {
        "bank_id": 1623,
        "bank_name": "T G C COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 824,
        "bank_name": "TALIPARAMBA COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1184,
        "bank_name": "TAMILNAD MERCANTILE BANK LIMITED"
    },
    {
        "bank_id": 1896,
        "bank_name": "TAMILNADU GRAMA BANK"
    },
    {
        "bank_id": 1185,
        "bank_name": "TAMLUK GHATAL CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1186,
        "bank_name": "TARAPUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1187,
        "bank_name": "TEACHERS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 674,
        "bank_name": "TEHRI GARHWAL ZILA SAHAKARI BANK LIMITED, ICICI BA"
    },
    {
        "bank_id": 772,
        "bank_name": "TEHRI GARHWAL ZILA SAHAKARI BANK, IDBI BANK"
    },
    {
        "bank_id": 1190,
        "bank_name": "TELANGANA GRAMEEN BANK"
    },
    {
        "bank_id": 1188,
        "bank_name": "TELANGANA STATE COOPERATIVE BANK APEX BANK"
    },
    {
        "bank_id": 670,
        "bank_name": "TERNA NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 315,
        "bank_name": "TEXTILE TRADERS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1191,
        "bank_name": "THA UTTARPARA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 669,
        "bank_name": "THASRA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1192,
        "bank_name": "THE  KHEDA  PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1193,
        "bank_name": "THE A.P. MAHESH COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1194,
        "bank_name": "THE ADARSH COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1195,
        "bank_name": "THE ADILABAD DISTRICT COOPERATIVE CENTRAL BANK LIM"
    },
    {
        "bank_id": 645,
        "bank_name": "THE ADINATH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1837,
        "bank_name": "THE ADINATH COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 340,
        "bank_name": "THE AGRASEN NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1196,
        "bank_name": "THE AGROHA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 644,
        "bank_name": "THE AGS EMPLOYEES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 759,
        "bank_name": "THE AHMEDNAGAR DIST CEN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 495,
        "bank_name": "THE AHMEDNAGAR MER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 863,
        "bank_name": "THE AJARA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1197,
        "bank_name": "THE AKKI ALUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1198,
        "bank_name": "THE AKOLA DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1199,
        "bank_name": "THE ALLEPPEY URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1200,
        "bank_name": "THE ALMEL URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1201,
        "bank_name": "THE ALNAVAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1516,
        "bank_name": "THE ALWAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1202,
        "bank_name": "THE AMBALA CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1545,
        "bank_name": "THE AMBIKA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1339,
        "bank_name": "THE AMOD NAGRIC COOPEARATIVE BANK LIMITED, GUJRAT"
    },
    {
        "bank_id": 638,
        "bank_name": "THE AMOD NAGRIK COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1203,
        "bank_name": "THE AMRITSAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1204,
        "bank_name": "THE ANAND MERCANTILE  COOPERATIVE BANK LIMITED, AX"
    },
    {
        "bank_id": 679,
        "bank_name": "THE ANAND MERCANTILE COOPERATIVE BANK"
    },
    {
        "bank_id": 1561,
        "bank_name": "THE ANANTHPUR COOPERATIVE TOWN BANK  "
    },
    {
        "bank_id": 1205,
        "bank_name": "THE ANDHRA PRADESH STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 905,
        "bank_name": "THE ANKOLA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 634,
        "bank_name": "THE AP JANATA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1209,
        "bank_name": "THE ARSIKERE URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1547,
        "bank_name": "THE ARYA VAISHYA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 646,
        "bank_name": "THE ARYAPURAM COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 148,
        "bank_name": "THE ASKA COOPERATIVE CENTRAL BANK LIMITED"
    },
    {
        "bank_id": 648,
        "bank_name": "THE ASSAM COOPERATIVE APEX BANK LIMITED"
    },
    {
        "bank_id": 864,
        "bank_name": "THE ASTHA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 846,
        "bank_name": "THE AZAD COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 750,
        "bank_name": "THE BABASAHEB DESHMUKH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 804,
        "bank_name": "THE BABASAHEB DESHMUKH SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 842,
        "bank_name": "THE BADAGARA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1210,
        "bank_name": "THE BAGALKOT COOPERATIVE BANK"
    },
    {
        "bank_id": 1211,
        "bank_name": "THE BAILHONGAL MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 884,
        "bank_name": "THE BAILHONGAL URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1396,
        "bank_name": "THE BALLARI DISTRICT COOPERATIVE CENTRAL BANK LIMI"
    },
    {
        "bank_id": 1212,
        "bank_name": "THE BANK OF NOVA SCOTIA"
    },
    {
        "bank_id": 1813,
        "bank_name": "THE BANKI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1515,
        "bank_name": "THE BANSWARA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 627,
        "bank_name": "THE BANTRA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 616,
        "bank_name": "THE BAPUNAGAR MAHILA COOPERATIVE BANK"
    },
    {
        "bank_id": 1213,
        "bank_name": "THE BAPUNAGAR MAHILA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 607,
        "bank_name": "THE BARAMATI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1293,
        "bank_name": "THE BARDOLI  NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 771,
        "bank_name": "THE BARDOLI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1514,
        "bank_name": "THE BARMER CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1214,
        "bank_name": "THE BARODA CITY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1215,
        "bank_name": "THE BARODA TRADERS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1216,
        "bank_name": "THE BATHINDA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 337,
        "bank_name": "THE BAVLA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1024,
        "bank_name": "THE BAVLA NAGRIK SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1292,
        "bank_name": "THE BECHRAJI NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1217,
        "bank_name": "THE BEGUSARAI DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 885,
        "bank_name": "THE BELGAUM DIST CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1218,
        "bank_name": "THE BELLARY DISTRICT CENTRAL COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 878,
        "bank_name": "THE BELLARY DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1219,
        "bank_name": "THE BERHAMPORE COOPERATIVE CENTRAL BANK LIMITED"
    },
    {
        "bank_id": 625,
        "bank_name": "THE BERHAMPUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 602,
        "bank_name": "THE BHABHAR VIBHAG NAG SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1338,
        "bank_name": "THE BHABHAR VIBHAG NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 748,
        "bank_name": "THE BHADGAON PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 137,
        "bank_name": "THE BHADRAN PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1220,
        "bank_name": "THE BHAGALPUR CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1221,
        "bank_name": "THE BHAGAT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 618,
        "bank_name": "THE BHAGYALAKSHMI MAHILA SAHAKARI BANK"
    },
    {
        "bank_id": 339,
        "bank_name": "THE BHAGYODAYA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 778,
        "bank_name": "THE BHANDARA DISTRICT CENTRAL COOPERATIVE BANK LIM"
    },
    {
        "bank_id": 620,
        "bank_name": "THE BHANDARA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1222,
        "bank_name": "THE BHARAT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1513,
        "bank_name": "THE BHARATPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1223,
        "bank_name": "THE BHATKAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 142,
        "bank_name": "THE BHAVASAR KSHATRIYA COOPERATIVE BANK"
    },
    {
        "bank_id": 1224,
        "bank_name": "THE BHAWANIPATNA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1225,
        "bank_name": "THE BHIWANI CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1921,
        "bank_name": "THE BHIWANI CENTRAL COOPERATIVE BANK LTD"
    },
    {
        "bank_id": 165,
        "bank_name": "THE BHUJ COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 617,
        "bank_name": "THE BHUJ MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 603,
        "bank_name": "THE BICHOLIUM URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 629,
        "bank_name": "THE BIHAR AWAMI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1226,
        "bank_name": "THE BIJNOR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1227,
        "bank_name": "THE BISHNUPUR TOWN COOPERATIVE BANK"
    },
    {
        "bank_id": 1228,
        "bank_name": "THE BODELI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 336,
        "bank_name": "THE BORAL UNION COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1229,
        "bank_name": "THE BOTAD PEOPLE S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1511,
        "bank_name": "THE BUNDI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 605,
        "bank_name": "THE BUNDI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 626,
        "bank_name": "THE BURDWAN CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1820,
        "bank_name": "THE BUSINESS COOPERATIVE BANK "
    },
    {
        "bank_id": 1230,
        "bank_name": "THE CALICUT COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 841,
        "bank_name": "THE CARDAMOM MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 133,
        "bank_name": "THE CATHOLIC COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1495,
        "bank_name": "THE CENTARAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1512,
        "bank_name": "THE CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 652,
        "bank_name": "THE CHAMBA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1336,
        "bank_name": "THE CHANASMA COMM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1335,
        "bank_name": "THE CHANASMA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 598,
        "bank_name": "THE CHANASMA NAGRIK SAHA. BANK LIMITED"
    },
    {
        "bank_id": 745,
        "bank_name": "THE CHANDGAD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1231,
        "bank_name": "THE CHANDIGARH STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1807,
        "bank_name": "THE CHANDRAPUR DCC BANK "
    },
    {
        "bank_id": 747,
        "bank_name": "THE CHANDWAD MERCHANT S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1232,
        "bank_name": "THE CHANGANACHERRY COOPERATIVE URBAN BANK  LIMITED"
    },
    {
        "bank_id": 600,
        "bank_name": "THE CHARADA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 746,
        "bank_name": "THE CHEMBUR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1233,
        "bank_name": "THE CHENNAI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1234,
        "bank_name": "THE CHERPALCHERI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 334,
        "bank_name": "THE CHHAPI NAGARIK SAHAKARI BANK"
    },
    {
        "bank_id": 1334,
        "bank_name": "THE CHHAPI NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 596,
        "bank_name": "THE CHIKHLI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 678,
        "bank_name": "THE CHITNAVISPURA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 130,
        "bank_name": "THE CHOPDA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1509,
        "bank_name": "THE CHURU CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 45,
        "bank_name": "THE CITIZEN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 813,
        "bank_name": "THE CITY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1235,
        "bank_name": "THE CKP COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1236,
        "bank_name": "THE COASTAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1237,
        "bank_name": "THE COIMBATORE DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 335,
        "bank_name": "THE COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1238,
        "bank_name": "THE COOPERATIVE BANK OF MEHSANA LIMITED "
    },
    {
        "bank_id": 1023,
        "bank_name": "THE COOPERATIVE BANK OF MEHSANA LIMITED  "
    },
    {
        "bank_id": 1724,
        "bank_name": "THE COOPERATIVE BANK OF RAJKOT "
    },
    {
        "bank_id": 1239,
        "bank_name": "THE COOPERATIVE CITY BANK LIMITED"
    },
    {
        "bank_id": 1240,
        "bank_name": "THE COSMOS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1241,
        "bank_name": "THE CUDDALORE DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1020,
        "bank_name": "THE DAHANU ROAD JANATA COOPERATIVE BANK"
    },
    {
        "bank_id": 588,
        "bank_name": "THE DAHOD MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1019,
        "bank_name": "THE DAHOD MERCANTILE COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 580,
        "bank_name": "THE DAHOD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 581,
        "bank_name": "THE DARUSSALAM COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 902,
        "bank_name": "THE DAVANGERE URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1021,
        "bank_name": "THE DECCAN COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 1242,
        "bank_name": "THE DECCAN MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1798,
        "bank_name": "THE DELHI ST COOPERATIVE BANK "
    },
    {
        "bank_id": 1243,
        "bank_name": "THE DELHI STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1244,
        "bank_name": "THE DEOLA MERCHANT S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 677,
        "bank_name": "THE DEOLA MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 591,
        "bank_name": "THE DEVGAD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1245,
        "bank_name": "THE DHANBAD CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 587,
        "bank_name": "THE DHANERA MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1246,
        "bank_name": "THE DHARMAJ PEOPLES  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 583,
        "bank_name": "THE DHARMAJ PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1247,
        "bank_name": "THE DHARMAPURI DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1333,
        "bank_name": "THE DHINOJ  NAGARIK SAHAKARI  BANK LIMITED"
    },
    {
        "bank_id": 1248,
        "bank_name": "THE DHOLPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 838,
        "bank_name": "THE DHRANGADHRA PEO COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1249,
        "bank_name": "THE DHRANGADHRA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1250,
        "bank_name": "THE DINDIGUL CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1939,
        "bank_name": "THE DISTRICT CO-OPERATIVE BANK LTD AGRA"
    },
    {
        "bank_id": 1917,
        "bank_name": "THE DISTRICT COOP CENTRAL BANK LTD BIDAR"
    },
    {
        "bank_id": 1252,
        "bank_name": "THE DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1208,
        "bank_name": "THE DISTRICT COOPERATIVE CENTRAL BANK "
    },
    {
        "bank_id": 1397,
        "bank_name": "THE DISTRICT COOPERATIVE CENTRAL BANK LIMITED "
    },
    {
        "bank_id": 1508,
        "bank_name": "THE DUNGARPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1253,
        "bank_name": "THE DURGA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 577,
        "bank_name": "THE EENADU COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1796,
        "bank_name": "THE ELURI COOPERATIVE URBAN BANK "
    },
    {
        "bank_id": 741,
        "bank_name": "THE ELURI COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 676,
        "bank_name": "THE ELURU URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1254,
        "bank_name": "THE ERNAKULAM DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1255,
        "bank_name": "THE ERODE DISTRICT CENTRAL COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1795,
        "bank_name": "THE FAIZ MERCANTILE COOPERATIVE BANK"
    },
    {
        "bank_id": 1256,
        "bank_name": "THE FARIDABAD CENTRAL  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1257,
        "bank_name": "THE FARIDKOT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1258,
        "bank_name": "THE FATEHABAD CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1259,
        "bank_name": "THE FATEHGARH SAHIB CENTRAL COOPERATIVE  BANK LIMI"
    },
    {
        "bank_id": 1260,
        "bank_name": "THE FAZILKA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 249,
        "bank_name": "THE FEDERAL BANK LIMITED"
    },
    {
        "bank_id": 256,
        "bank_name": "THE FEDERAL BANK LIMITED, ALWAYE URBAN COOPERATIVE"
    },
    {
        "bank_id": 251,
        "bank_name": "THE FEDERAL BANK LIMITED, AUCB BR ALENGAD"
    },
    {
        "bank_id": 252,
        "bank_name": "THE FEDERAL BANK LIMITED, AUCB BR CHUNANGAMVELI"
    },
    {
        "bank_id": 1261,
        "bank_name": "THE FEROKE COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1262,
        "bank_name": "THE FEROZEPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1263,
        "bank_name": "THE GADCHIROLI DISTRICT CENTRAL COOPERATIVE BANK L"
    },
    {
        "bank_id": 570,
        "bank_name": "THE GADCHIROLI NAG SAHAKARI BANK"
    },
    {
        "bank_id": 1264,
        "bank_name": "THE GADHINGLAJ URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 906,
        "bank_name": "THE GANDEVI PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1265,
        "bank_name": "THE GANDHI GUNJ COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1266,
        "bank_name": "THE GANDHIDHAM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 939,
        "bank_name": "THE GANDHIDHAM MER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1331,
        "bank_name": "THE GANDHIDHAM MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 331,
        "bank_name": "THE GANDHINAGAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 675,
        "bank_name": "THE GANESH SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1267,
        "bank_name": "THE GANGA MERCANTILE URBAN COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1496,
        "bank_name": "THE GANGANAGAR KENDRIYA SAHAKARI BANK"
    },
    {
        "bank_id": 1268,
        "bank_name": "THE GAUHATI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 333,
        "bank_name": "THE GAYATRI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 568,
        "bank_name": "THE GHATAL PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1330,
        "bank_name": "THE GHOGHAMBA  VIBHAG NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 117,
        "bank_name": "THE GHOTI MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 118,
        "bank_name": "THE GIRIDIH CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1788,
        "bank_name": "THE GOA STATE COOPERATIVE BANK"
    },
    {
        "bank_id": 566,
        "bank_name": "THE GOA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1269,
        "bank_name": "THE GODHRA CITY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1270,
        "bank_name": "THE GODHRA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1271,
        "bank_name": "THE GOKAK URBAN COOPERATIVE CREDIT BANK LIMITED"
    },
    {
        "bank_id": 119,
        "bank_name": "THE GONDIA DISTRICT BANK"
    },
    {
        "bank_id": 1546,
        "bank_name": "THE GOOTY COOPERATIVE TOWN BANK LIMITED"
    },
    {
        "bank_id": 1272,
        "bank_name": "THE GOPALGANJ CENTRAL GOPALGANJ COOPERATIVE BANK L"
    },
    {
        "bank_id": 332,
        "bank_name": "THE GOZARIA NAGARIK SAHAKARI BANK"
    },
    {
        "bank_id": 782,
        "bank_name": "THE GRAIN MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1273,
        "bank_name": "THE GREATER BOMBAY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 892,
        "bank_name": "THE GUDIVADA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1349,
        "bank_name": "THE GUJARAT RAJYA KARMACHARI COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 1308,
        "bank_name": "THE GUJARAT STATE CO-OPERATIVE BANK LTD"
    },
    {
        "bank_id": 1355,
        "bank_name": "THE GUJARAT STATE CO-OPERATIVE BANK LTD"
    },
    {
        "bank_id": 844,
        "bank_name": "THE GUMLA SIMDEGA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 115,
        "bank_name": "THE GUNTUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1206,
        "bank_name": "THE GUNTUR DIST COOPERATIVE CENTRAL BANK LIMITED "
    },
    {
        "bank_id": 1357,
        "bank_name": "THE GURDASPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1358,
        "bank_name": "THE GURGAON CENTRAL  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 562,
        "bank_name": "THE HALOL MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1329,
        "bank_name": "THE HALOL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1291,
        "bank_name": "THE HANSOT NAGARIC SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 563,
        "bank_name": "THE HANUMANTHANAGAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1328,
        "bank_name": "THE HARIJ NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1359,
        "bank_name": "THE HARYANA STATE COOPERATIVE  APEX BANK LIMITED"
    },
    {
        "bank_id": 1786,
        "bank_name": "THE HASSAN DCC BANK LIMITED"
    },
    {
        "bank_id": 1937,
        "bank_name": "THE HASSAN DISTRICT CENTRAL CO-OPERATIVE BANK LTD"
    },
    {
        "bank_id": 564,
        "bank_name": "THE HASTI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1360,
        "bank_name": "THE HAVERI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1361,
        "bank_name": "THE HAVERI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 113,
        "bank_name": "THE HAZARIBAG CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1362,
        "bank_name": "THE HAZARIBAG CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1363,
        "bank_name": "THE HINDU COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1898,
        "bank_name": "THE HINDUSTHAN CO OP BANK LIMITED"
    },
    {
        "bank_id": 560,
        "bank_name": "THE HIRASUGAR EMPLOYEES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1364,
        "bank_name": "THE HIRIYUR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1365,
        "bank_name": "THE HISAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1366,
        "bank_name": "THE HISAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1367,
        "bank_name": "THE HONAVAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1368,
        "bank_name": "THE HOOGHLY COOPERATIVE CREDIT BANK LIMITED"
    },
    {
        "bank_id": 1369,
        "bank_name": "THE HOSHIARPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1555,
        "bank_name": "THE HOTEL INDUSTRIALISTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1628,
        "bank_name": "THE HOWRAH DISTRICT CENTRAL CO-OPERTAIVE BANK LIMI"
    },
    {
        "bank_id": 1785,
        "bank_name": "THE HP STATE COOPERATIVE BANK "
    },
    {
        "bank_id": 1562,
        "bank_name": "THE HUBLI URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 330,
        "bank_name": "THE HUKKERI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1890,
        "bank_name": "THE HYDERABAD DISTRICT CO OPERATIVE CENTRAL BANK"
    },
    {
        "bank_id": 1370,
        "bank_name": "THE HYDERABAD DISTRICT COOPERATIVE CENTRAL BANK LI"
    },
    {
        "bank_id": 557,
        "bank_name": "THE ICHALKARANJI MER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1327,
        "bank_name": "THE IDAR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 870,
        "bank_name": "THE IDAR NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 890,
        "bank_name": "THE INCOME TAX DEPT COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 865,
        "bank_name": "THE INDUSTRIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1371,
        "bank_name": "THE INNESPETA  COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 329,
        "bank_name": "THE ISLAMPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1372,
        "bank_name": "THE JAGRUTI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1373,
        "bank_name": "THE JAIN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 815,
        "bank_name": "THE JAIN SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1374,
        "bank_name": "THE JAIPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1493,
        "bank_name": "THE JAISALMER CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1375,
        "bank_name": "THE JALANDHAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1376,
        "bank_name": "THE JALGAON DISTRICT CENTRAL COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 1377,
        "bank_name": "THE JALGAON PEOPELS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 539,
        "bank_name": "THE JALNA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 540,
        "bank_name": "THE JALNA PEOPLES COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1507,
        "bank_name": "THE JALORE CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1627,
        "bank_name": "THE JALPAIGURI CTRL BANK "
    },
    {
        "bank_id": 1325,
        "bank_name": "THE JAMBUSAR PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1378,
        "bank_name": "THE JAMKHANDI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1326,
        "bank_name": "THE JAMNAGAR MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 328,
        "bank_name": "THE JAMNAGAR PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 534,
        "bank_name": "THE JAMSHEDPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 731,
        "bank_name": "THE JANATA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1379,
        "bank_name": "THE JANATHA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 889,
        "bank_name": "THE JAWHAR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 895,
        "bank_name": "THE JAYNAGAR MOZILPUR PEOPLES COOPERATIVE BANK LIM"
    },
    {
        "bank_id": 1380,
        "bank_name": "THE JHAJJAR CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 542,
        "bank_name": "THE JHALAWAR NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1381,
        "bank_name": "THE JHALOD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1011,
        "bank_name": "THE JHALOD URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1382,
        "bank_name": "THE JIND CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1504,
        "bank_name": "THE JODHPUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1383,
        "bank_name": "THE JOWAI COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1384,
        "bank_name": "THE JOWAI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 548,
        "bank_name": "THE JUNAGADH COMM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 859,
        "bank_name": "THE KAGAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 726,
        "bank_name": "THE KAIRA DISTRICT CENTRAL COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1385,
        "bank_name": "THE KAITHAL CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1386,
        "bank_name": "THE KAKATIYA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 103,
        "bank_name": "THE KAKINADA COOPERATIVE TOWN BANK"
    },
    {
        "bank_id": 891,
        "bank_name": "THE KAKINADA TOWN COOPERATIVE TOWN BANK"
    },
    {
        "bank_id": 519,
        "bank_name": "THE KALNA TOWN CREDIT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 843,
        "bank_name": "THE KALOL NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 325,
        "bank_name": "THE KALOL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1557,
        "bank_name": "THE KALWAN MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 528,
        "bank_name": "THE KALWAN MERCHANTS COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 43,
        "bank_name": "THE KANAKAMAHALAKSHMI COOPERATIVE BANK"
    },
    {
        "bank_id": 1387,
        "bank_name": "THE KANAKAMAHALAKSHMI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1388,
        "bank_name": "THE KANCHIPURAM CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1389,
        "bank_name": "THE KANGRA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1390,
        "bank_name": "THE KANGRA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1391,
        "bank_name": "THE KANNUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1392,
        "bank_name": "THE KANYAKUMARI DISTRICT CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 524,
        "bank_name": "THE KAPADWANJ PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 96,
        "bank_name": "THE KAPURTHALA CENTRAL  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 530,
        "bank_name": "THE KARAD JANATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1393,
        "bank_name": "THE KARAD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1412,
        "bank_name": "THE KARANATAKA STATE COOPERATIVE APEX BANK LIMITED"
    },
    {
        "bank_id": 1413,
        "bank_name": "THE KARIMNAGAR DISTRICT COOPERATIVE CENTRAL BANK L"
    },
    {
        "bank_id": 673,
        "bank_name": "THE KARJAN NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1289,
        "bank_name": "THE KARJAN NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 522,
        "bank_name": "THE KARMALA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1414,
        "bank_name": "THE KARNAL CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1415,
        "bank_name": "THE KARNATAKA COOPERATIVE BANK LIMITED,"
    },
    {
        "bank_id": 985,
        "bank_name": "THE KARNAVATI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1416,
        "bank_name": "THE KARWAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1417,
        "bank_name": "THE KASARAGOD COOPERATIVE TOWN BANK LIMITED"
    },
    {
        "bank_id": 1902,
        "bank_name": "THE KASARAGOD DISTRICT CO-OPERATIVE BANK LTD"
    },
    {
        "bank_id": 1418,
        "bank_name": "THE KASARAGOD DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 517,
        "bank_name": "THE KATTAPPANA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 510,
        "bank_name": "THE KENDRAPARA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1419,
        "bank_name": "THE KERALA MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1420,
        "bank_name": "THE KERALA STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 822,
        "bank_name": "THE KESHAV SEHKARI BANK LIMITED"
    },
    {
        "bank_id": 872,
        "bank_name": "THE KHAGARIA DISTRICTCENTRAL COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 1323,
        "bank_name": "THE KHAMBHAT NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1421,
        "bank_name": "THE KHAMMAM DISTRICT COOPERATIVE CENTRAL BANK LIMI"
    },
    {
        "bank_id": 722,
        "bank_name": "THE KHEDA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1290,
        "bank_name": "THE KHERALU NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 526,
        "bank_name": "THE KODINAR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 858,
        "bank_name": "THE KODOLI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1422,
        "bank_name": "THE KODUNGALLUR TOWN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 513,
        "bank_name": "THE KOLHAPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1768,
        "bank_name": "THE KOLLAM DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 960,
        "bank_name": "THE KONARK URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1560,
        "bank_name": "THE KOPARGAON PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 97,
        "bank_name": "THE KORAPUT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1324,
        "bank_name": "THE KOSAMBA  MERC COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1503,
        "bank_name": "THE KOTA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1543,
        "bank_name": "THE KOVVUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 525,
        "bank_name": "THE KOYLANCHAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1423,
        "bank_name": "THE KOZHIKODE DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 95,
        "bank_name": "THE KRANTHI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1207,
        "bank_name": "THE KRISHNA DISTRICT COOPERATIVE CENTRAL BANK LIMI"
    },
    {
        "bank_id": 531,
        "bank_name": "THE KRISHNANAGAR CITY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 326,
        "bank_name": "THE KUKARWADA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1424,
        "bank_name": "THE KUMBAKONAM CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1425,
        "bank_name": "THE KUMTA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1765,
        "bank_name": "THE KUNBI SAHAKARI BANK "
    },
    {
        "bank_id": 721,
        "bank_name": "THE KURLA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1426,
        "bank_name": "THE KURMANCHAL NAGAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1427,
        "bank_name": "THE KURUKSHETRA CENTRAL  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 327,
        "bank_name": "THE KUTCH MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1322,
        "bank_name": "THE LAKHWAD NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1559,
        "bank_name": "THE LASALGAON MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 790,
        "bank_name": "THE LATUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1428,
        "bank_name": "THE LAXMI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 324,
        "bank_name": "THE LAXMI COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1429,
        "bank_name": "THE LAXMI URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1319,
        "bank_name": "THE LIMBASI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1430,
        "bank_name": "THE LIMDI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1431,
        "bank_name": "THE LUDHIANA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 505,
        "bank_name": "THE LUNAWADA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 485,
        "bank_name": "THE MADANAPALLE COOPERATIVE TOWN BANK LIMITED"
    },
    {
        "bank_id": 482,
        "bank_name": "THE MADGAUM URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1432,
        "bank_name": "THE MADURAI DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 798,
        "bank_name": "THE MAHABALESHWAR URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1433,
        "bank_name": "THE MAHABOOBNAGAR DISTRICT COOPERATIVE CENTRAL BAN"
    },
    {
        "bank_id": 1434,
        "bank_name": "THE MAHANAGAR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 913,
        "bank_name": "THE MAHARAJA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 323,
        "bank_name": "THE MAHAVEER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 89,
        "bank_name": "THE MAHENDERGARH CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 480,
        "bank_name": "THE MAHILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1318,
        "bank_name": "THE MAHILA VIKAS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1006,
        "bank_name": "THE MAHILA VIKAS COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 42,
        "bank_name": "THE MAHUDHA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 82,
        "bank_name": "THE MALAD SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1435,
        "bank_name": "THE MALEGAON MERCHANT S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 321,
        "bank_name": "THE MALKAPUR URB COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 493,
        "bank_name": "THE MALLESWARAM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1317,
        "bank_name": "THE MALPUR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 498,
        "bank_name": "THE MANDAL NAGRIC SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1312,
        "bank_name": "THE MANDAL NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 88,
        "bank_name": "THE MANDAPETA COOPERATIVE TOWN BANK"
    },
    {
        "bank_id": 86,
        "bank_name": "THE MANDVI MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1288,
        "bank_name": "THE MANDVI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1436,
        "bank_name": "THE MANDYA CITY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1437,
        "bank_name": "THE MANGALORE CATHOLIC COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1438,
        "bank_name": "THE MANGALORE COOPERATIVE TOWN BANK LIMITED"
    },
    {
        "bank_id": 1752,
        "bank_name": "THE MANIPUR WOMEN S COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 79,
        "bank_name": "THE MANIPUR WOMENS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 715,
        "bank_name": "THE MANJERI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1439,
        "bank_name": "THE MANMANDIR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1440,
        "bank_name": "THE MANSA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1316,
        "bank_name": "THE MANSA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 479,
        "bank_name": "THE MAPUSA URB COOPERATIVE BANK OF GOA LIMITED "
    },
    {
        "bank_id": 1441,
        "bank_name": "THE MATTANCHERRY MAHAJANIK COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1442,
        "bank_name": "THE MATTANCHERRY SARVAJANIK COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 671,
        "bank_name": "THE MAYANI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1443,
        "bank_name": "THE MEDAK DISTRICT COOPERATIVE CENTRAL BANK LIMITE"
    },
    {
        "bank_id": 257,
        "bank_name": "THE MEENACHIL EAST URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1313,
        "bank_name": "THE MEGHRAJ NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 477,
        "bank_name": "THE MEHKAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1444,
        "bank_name": "THE MEHMADABAD URBAN PEOPLES COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 1314,
        "bank_name": "THE MEHSANA JILLA PANCHAYAT KARMACHARI COOPERATIVE"
    },
    {
        "bank_id": 818,
        "bank_name": "THE MEHSANA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1445,
        "bank_name": "THE MEHSANA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 80,
        "bank_name": "THE MERCHANT URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 847,
        "bank_name": "THE MERCHANTS SOUHARDA SAHAKARA BANK "
    },
    {
        "bank_id": 672,
        "bank_name": "THE MERCHANTS URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1446,
        "bank_name": "THE MODA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1009,
        "bank_name": "THE MODASA NAGARIK SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1447,
        "bank_name": "THE MODEL COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 494,
        "bank_name": "THE MODERN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 84,
        "bank_name": "THE MOIRANG PRIMARY COOPERATIVE BANK"
    },
    {
        "bank_id": 41,
        "bank_name": "THE MOTI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1448,
        "bank_name": "THE MOTIHARI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1449,
        "bank_name": "THE MUDALAGI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1450,
        "bank_name": "THE MUKTSAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1455,
        "bank_name": "THE MUMBAI DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 1457,
        "bank_name": "THE MUNICIPAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 90,
        "bank_name": "THE MUSLIM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 473,
        "bank_name": "THE MUSLIM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1458,
        "bank_name": "THE MUVATTUPUZHA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 470,
        "bank_name": "THE NABADWIP COOPERATIVE CREDIT BANK LIMITED"
    },
    {
        "bank_id": 1459,
        "bank_name": "THE NABAPALLI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 162,
        "bank_name": "THE NADIAD PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 75,
        "bank_name": "THE NAGALAND STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 163,
        "bank_name": "THE NAGAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1502,
        "bank_name": "THE NAGAUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 787,
        "bank_name": "THE NAGPUR DIST CENTRAL COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1460,
        "bank_name": "THE NAINITAL BANK LIMITED"
    },
    {
        "bank_id": 465,
        "bank_name": "THE NAKODAR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1461,
        "bank_name": "THE NALGONDA DISTRICT COOPERATIVE CENTRAL BANK LIM"
    },
    {
        "bank_id": 789,
        "bank_name": "THE NANDED MERCHANT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 452,
        "bank_name": "THE NANDURA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1004,
        "bank_name": "THE NANDURBAR MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 320,
        "bank_name": "THE NARODA NAGRIK COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 812,
        "bank_name": "THE NASHIK JILHA MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 708,
        "bank_name": "THE NASIK DIST CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1462,
        "bank_name": "THE NASIK MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 845,
        "bank_name": "THE NATIONAL CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1464,
        "bank_name": "THE NATIONAL COOPERATIVE BANK"
    },
    {
        "bank_id": 984,
        "bank_name": "THE NATIONAL COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1465,
        "bank_name": "THE NAVAL DOCKYARD COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 703,
        "bank_name": "THE NAVJEEVAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1466,
        "bank_name": "THE NAVNIRMAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1750,
        "bank_name": "THE NAWADA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1467,
        "bank_name": "THE NAWANAGAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1468,
        "bank_name": "THE NAWANSHAHR CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 937,
        "bank_name": "THE NEHRUNAGAR COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 469,
        "bank_name": "THE NEMMARA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1469,
        "bank_name": "THE NEW AGRA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 453,
        "bank_name": "THE NEW URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1470,
        "bank_name": "THE NILAMBUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1471,
        "bank_name": "THE NILGIRIS DISTRICT CENTRAL COOPERATIVE BANK LIM"
    },
    {
        "bank_id": 455,
        "bank_name": "THE NIPHAD URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1003,
        "bank_name": "THE NIPHAD URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1472,
        "bank_name": "THE NIZAMABAD DISTRICT COOPERATIVE APEX CENTRAL BA"
    },
    {
        "bank_id": 1311,
        "bank_name": "THE ODE URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 450,
        "bank_name": "THE OJHAR MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1473,
        "bank_name": "THE OTTAPALAM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 73,
        "bank_name": "THE PACHHAPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 434,
        "bank_name": "THE PACHORA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1307,
        "bank_name": "THE PADRA NAGAR NAG SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1474,
        "bank_name": "THE PALAMOOR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1501,
        "bank_name": "THE PALI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1475,
        "bank_name": "THE PANCHKULA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1476,
        "bank_name": "THE PANCHKULA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 701,
        "bank_name": "THE PANDHARPUR  MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1477,
        "bank_name": "THE PANDHARPUR URBAN COOPERATIVE  BANK LIMITED PAN"
    },
    {
        "bank_id": 1478,
        "bank_name": "THE PANIHATI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1479,
        "bank_name": "THE PANIPAT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 834,
        "bank_name": "THE PANVELURBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 430,
        "bank_name": "THE PATAN URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1285,
        "bank_name": "THE PATDI NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1480,
        "bank_name": "THE PATHANAMTHITTA DISTRICT COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 1481,
        "bank_name": "THE PATIALA CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1482,
        "bank_name": "THE PAYYOLI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1483,
        "bank_name": "THE PEOPLE S URBAN COOPERATIVE BANK,"
    },
    {
        "bank_id": 319,
        "bank_name": "THE PEOPLES COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1309,
        "bank_name": "THE PIJ  PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 700,
        "bank_name": "THE PIJ PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1484,
        "bank_name": "THE PIONEER URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 443,
        "bank_name": "THE POCHAMPALLY COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 250,
        "bank_name": "THE PONANI COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 432,
        "bank_name": "THE POSTAL & RMS EMPLOY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1286,
        "bank_name": "THE PRAGATI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 805,
        "bank_name": "THE PRATHAMIK SHIKSHAK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 799,
        "bank_name": "THE PRITISANGAM SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 69,
        "bank_name": "THE PRODDATUR COOPERATIVE TOWN BANK"
    },
    {
        "bank_id": 1485,
        "bank_name": "THE PUDUKKOTTAI DISTRICT CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 161,
        "bank_name": "THE PUNJAB STATE COOPERATIVE BANK"
    },
    {
        "bank_id": 1486,
        "bank_name": "THE PURNIA DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 769,
        "bank_name": "THE QUILON COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 900,
        "bank_name": "THE RADDI SAHAKARA BANK "
    },
    {
        "bank_id": 896,
        "bank_name": "THE RADHASOMAY URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1487,
        "bank_name": "THE RAIGAD DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 1488,
        "bank_name": "THE RAILWAY COOPERATIVE BANK LIMITED, MYSORE"
    },
    {
        "bank_id": 697,
        "bank_name": "THE RAIPUR URBAN MERCHANT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 421,
        "bank_name": "THE RAJAJINAGAR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 779,
        "bank_name": "THE RAJAPUR SAHAKARI BANK"
    },
    {
        "bank_id": 1492,
        "bank_name": "THE RAJASTHAN STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1894,
        "bank_name": "THE RAJASTHAN STATE COOPERATIVE BANK LTD"
    },
    {
        "bank_id": 1518,
        "bank_name": "THE RAJASTHAN URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1519,
        "bank_name": "THE RAJKOT COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 417,
        "bank_name": "THE RAJLAXMI MAHILA UC BANK LIMITED"
    },
    {
        "bank_id": 1304,
        "bank_name": "THE RAJPIPLA  NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1306,
        "bank_name": "THE RAJULA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1932,
        "bank_name": "THE RAMANATHAPURAM DISTRICT CENTRAL CO-OPERATIVE B"
    },
    {
        "bank_id": 1520,
        "bank_name": "THE RAMANATHAPURAM DISTRICT CENTRAL COOPERATIVE BA"
    },
    {
        "bank_id": 1521,
        "bank_name": "THE RANCHI KHUNTI CENTRAL  COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 412,
        "bank_name": "THE RANDER PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1305,
        "bank_name": "THE RANDHEJA COMMERCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 998,
        "bank_name": "THE RANGA REDDY COOPERATIVE URBAN BANK LIMITED "
    },
    {
        "bank_id": 873,
        "bank_name": "THE RANUJ NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 423,
        "bank_name": "THE RANUJ NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1883,
        "bank_name": "THE RATNAKAR BANK LIMITED CREDIT CARD"
    },
    {
        "bank_id": 1522,
        "bank_name": "THE RAVER PEOPLES CO -OPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1523,
        "bank_name": "THE RAYAT SEVAK COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1554,
        "bank_name": "THE REVDANDA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1524,
        "bank_name": "THE REWARI CENTRAL  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 876,
        "bank_name": "THE ROHIKA CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1525,
        "bank_name": "THE ROHTAK CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1526,
        "bank_name": "THE ROPAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1527,
        "bank_name": "THE ROYAL BANK OF SCOTLAND N V"
    },
    {
        "bank_id": 1294,
        "bank_name": "THE SALAL SARVODAY NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1528,
        "bank_name": "THE SALEM DISTRICT CENTRAL COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1529,
        "bank_name": "THE SALUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1530,
        "bank_name": "THE SAMASTIPUR DISTRICT CENTRAL COOPERATIVE BANK L"
    },
    {
        "bank_id": 936,
        "bank_name": "THE SAMMCO BANK LIMITED "
    },
    {
        "bank_id": 316,
        "bank_name": "THE SANGAMNER MERCH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 792,
        "bank_name": "THE SANGLI DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 1531,
        "bank_name": "THE SANGRUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 982,
        "bank_name": "THE SANKHEDA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 376,
        "bank_name": "THE SANKHEDA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1532,
        "bank_name": "THE SANTRAGACHI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1533,
        "bank_name": "THE SANTRAMPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1534,
        "bank_name": "THE SARANGPUR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1297,
        "bank_name": "THE SARDAR GUNJ MERC COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 63,
        "bank_name": "THE SARDARGANJ MERCANTILE  COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1535,
        "bank_name": "THE SARSA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 400,
        "bank_name": "THE SARVODAYA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1284,
        "bank_name": "THE SARVODAYA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 981,
        "bank_name": "THE SARVODAYA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 1536,
        "bank_name": "THE SAS NAGAR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 667,
        "bank_name": "THE SATANA MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1537,
        "bank_name": "THE SATARA DISTRICT CENTRAL COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 1694,
        "bank_name": "THE SATARA SAHAKARI BANK "
    },
    {
        "bank_id": 372,
        "bank_name": "THE SATHAMBA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1538,
        "bank_name": "THE SAURASHTRA COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 1539,
        "bank_name": "THE SAURASHTRA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 349,
        "bank_name": "THE SAVANUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 690,
        "bank_name": "THE SECUNDERABAD MERCANTILE COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1540,
        "bank_name": "THE SEVA VIKAS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 694,
        "bank_name": "THE SEVALIA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1551,
        "bank_name": "THE SHALINI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1563,
        "bank_name": "THE SHAMRAO VITHAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1572,
        "bank_name": "THE SHIBPUR COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 994,
        "bank_name": "THE SHIRPUR PEOPLES COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1573,
        "bank_name": "THE SHORANUR COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 683,
        "bank_name": "THE SINDAGI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1574,
        "bank_name": "THE SINDHUDURG DISTRICT CENTRAL COOPERATIVE BANK L"
    },
    {
        "bank_id": 1575,
        "bank_name": "THE SINGHBHUM DISTRICT CENTRAL COOPERATIVE BANK LI"
    },
    {
        "bank_id": 686,
        "bank_name": "THE SINOR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1498,
        "bank_name": "THE SIROHI CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1576,
        "bank_name": "THE SIRSA CENTRAL COOPERATIVE  BANK LIMITED"
    },
    {
        "bank_id": 899,
        "bank_name": "THE SIRSI URBAN SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 770,
        "bank_name": "THE SITAMARHI CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1577,
        "bank_name": "THE SIVAGANGAI DISTRICT CENTRAL COOPERATIVE BANK L"
    },
    {
        "bank_id": 399,
        "bank_name": "THE SOCIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1713,
        "bank_name": "THE SOLAPUR DIST CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1579,
        "bank_name": "THE SOLAPUR DISTRICT CENTRAL COOPERATIVE BANK LIMI"
    },
    {
        "bank_id": 869,
        "bank_name": "THE SONEPAT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1580,
        "bank_name": "THE SONEPAT URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1581,
        "bank_name": "THE SOUTH CANARA DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 887,
        "bank_name": "THE SRI KANNIKAPARAMESHWARI COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 684,
        "bank_name": "THE SSK COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 48,
        "bank_name": "THE SUDHA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1582,
        "bank_name": "THE SULTAN S BATTERY COOPERATIVE URBAN BANK"
    },
    {
        "bank_id": 1583,
        "bank_name": "THE SULTAN?S BATTERY COOPERATIVE URBAN BANK LIMITE"
    },
    {
        "bank_id": 1584,
        "bank_name": "THE SURAT DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1585,
        "bank_name": "THE SURATH PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1586,
        "bank_name": "THE SUVIKAS PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1587,
        "bank_name": "THE SWASAKTHI MERCANTILE COOPERATIVE URBAN BANK LI"
    },
    {
        "bank_id": 666,
        "bank_name": "THE TALOD NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1287,
        "bank_name": "THE TALOD NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1588,
        "bank_name": "THE TAMIL NADU STATE APEX COOPERATIVE BANK"
    },
    {
        "bank_id": 1589,
        "bank_name": "THE TAMILNADU INDUSTRIAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 313,
        "bank_name": "THE TAPINDU URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1590,
        "bank_name": "THE TARN TARAN CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 777,
        "bank_name": "THE TASGAON URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1699,
        "bank_name": "THE TEXCO BANK "
    },
    {
        "bank_id": 1591,
        "bank_name": "THE THANE BHARAT SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1592,
        "bank_name": "THE THANE DISTRICT CENTRAL COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 1593,
        "bank_name": "THE THANJAVUR CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1594,
        "bank_name": "THE THIRUVANANTHAPURAM DISTRICT COOPERATIVE BANK L"
    },
    {
        "bank_id": 668,
        "bank_name": "THE THODUPUZHA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1595,
        "bank_name": "THE THOOTHUKUDI DISTRICT CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 1596,
        "bank_name": "THE THRISSUR DISTRICT  COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1597,
        "bank_name": "THE TIRUCHIRAPALLI DISTRICT CENTRAL COOPERATIVE BANK LTD"
    },
    {
        "bank_id": 1598,
        "bank_name": "THE TIRUNELVELI DISTRICT CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 1599,
        "bank_name": "THE TIRUPATI COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1600,
        "bank_name": "THE TIRUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 166,
        "bank_name": "THE TIRUVALLA EAST COOPERATIVE BANK"
    },
    {
        "bank_id": 1601,
        "bank_name": "THE TIRUVALLA EAST COOPERATIVE BANK "
    },
    {
        "bank_id": 1602,
        "bank_name": "THE TIRUVANNAMALAI DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 1603,
        "bank_name": "THE TOWN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 318,
        "bank_name": "THE TRICHUR URBAN CO OPERA BANK LIMITED"
    },
    {
        "bank_id": 1604,
        "bank_name": "THE TRIVANDRUM COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1693,
        "bank_name": "THE TURA URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 1494,
        "bank_name": "THE UDAIPUR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 305,
        "bank_name": "THE UDGIR URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1605,
        "bank_name": "THE UDUPI COOPERATIVE TOWN BANK"
    },
    {
        "bank_id": 1606,
        "bank_name": "THE UMRETH URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1607,
        "bank_name": "THE UNA PEOPLES COOPERATIVE BANK"
    },
    {
        "bank_id": 1282,
        "bank_name": "THE UNA PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1280,
        "bank_name": "THE UNAVA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1608,
        "bank_name": "THE UNION COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1691,
        "bank_name": "THE UNITED COOPERATIVE BANK "
    },
    {
        "bank_id": 1609,
        "bank_name": "THE UNITED COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1690,
        "bank_name": "THE URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 665,
        "bank_name": "THE URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1610,
        "bank_name": "THE UTTARPARA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 925,
        "bank_name": "THE UTTARSANDA PEOPLES COOPERATIVE BANK"
    },
    {
        "bank_id": 1275,
        "bank_name": "THE VADALI NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 33,
        "bank_name": "THE VAIDYANATH URBAN COOPERATIVE BANK, AXIS BANK"
    },
    {
        "bank_id": 34,
        "bank_name": "THE VAIDYANATH URBAN COOPERATIVE BANK, HDFC BANK"
    },
    {
        "bank_id": 301,
        "bank_name": "THE VAISH COOPERATIVE ADARSH BANK LIMITED"
    },
    {
        "bank_id": 311,
        "bank_name": "THE VAISH COOPERATIVE COMM BANK LIMITED"
    },
    {
        "bank_id": 1678,
        "bank_name": "THE VAISH COOPERATIVE NEW BANK "
    },
    {
        "bank_id": 1611,
        "bank_name": "THE VAISHALI DISTRICT CENTRAL COOPERATIVE BANK LIM"
    },
    {
        "bank_id": 283,
        "bank_name": "THE VALLABH VIDYANAGAR COMM COOPERATIVE BANK LIMIT"
    },
    {
        "bank_id": 661,
        "bank_name": "THE VALSAD MAHILA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1612,
        "bank_name": "THE VARACHHA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1613,
        "bank_name": "THE VARDHMAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 28,
        "bank_name": "THE VEJALPUR NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 1614,
        "bank_name": "THE VELLORE DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1279,
        "bank_name": "THE VEPAR UDHYOG VIKAS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 294,
        "bank_name": "THE VERAVAL MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 292,
        "bank_name": "THE VERAVAL PEOPLES COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1283,
        "bank_name": "THE VIJAPUR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1615,
        "bank_name": "THE VIJAY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1616,
        "bank_name": "THE VILLUPURAM DISTRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1278,
        "bank_name": "THE VIRAMGAM MERCANTILE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1617,
        "bank_name": "THE VIRUDHUNAGAR DISTRICT CENTRAL COOPERATIVE BANK"
    },
    {
        "bank_id": 912,
        "bank_name": "THE VISAKHAPATNAM COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1618,
        "bank_name": "THE VISHWESHWAR SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 852,
        "bank_name": "THE VITA MERCHANT COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 662,
        "bank_name": "THE VITA MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 285,
        "bank_name": "THE VITA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1619,
        "bank_name": "THE VSV COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 310,
        "bank_name": "THE VYANKATESHWARA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1620,
        "bank_name": "THE WAGHODIYA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1621,
        "bank_name": "THE WARANGAL DISTRICT COOPERATIVE CENTRAL BANK LIM"
    },
    {
        "bank_id": 278,
        "bank_name": "THE WASHIM URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 248,
        "bank_name": "THE WAYANAD DIST COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1622,
        "bank_name": "THE WEST BENGAL STATE COOPERATIVE BANK"
    },
    {
        "bank_id": 280,
        "bank_name": "THE WOMENS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1630,
        "bank_name": "THE YAMUNA NAGAR CENTRAL CO  OPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 276,
        "bank_name": "THE YASHWANT COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1671,
        "bank_name": "THE YAVATMAL DCC BANK "
    },
    {
        "bank_id": 273,
        "bank_name": "THE YAVATMAL MAHILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 909,
        "bank_name": "THE YAVATMAL URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 29,
        "bank_name": "THE YEMMIGANUR COOPERATIVE TOWN BANK LIMITED"
    },
    {
        "bank_id": 1631,
        "bank_name": "THE ZOROASTRIAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 314,
        "bank_name": "TIRUPATI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1632,
        "bank_name": "TJSB SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1697,
        "bank_name": "TRANSPORT COOPERATIVE BANK "
    },
    {
        "bank_id": 1633,
        "bank_name": "TRIPURA GRAMIN BANK"
    },
    {
        "bank_id": 1634,
        "bank_name": "TRIPURA STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1406,
        "bank_name": "TUMKUR DCC BANK LIMITED"
    },
    {
        "bank_id": 1407,
        "bank_name": "TUMKUR DISTRICT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 44,
        "bank_name": "TUMKUR DISTRICT COOPERATIVE CENTRAL BANK"
    },
    {
        "bank_id": 1635,
        "bank_name": "TUMKUR GRAIN MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1636,
        "bank_name": "TUMKUR VEERASHAIVA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1920,
        "bank_name": "The Navnirman Co - Op. Bank Ltd."
    },
    {
        "bank_id": 1637,
        "bank_name": "UCO BANK"
    },
    {
        "bank_id": 664,
        "bank_name": "UDAIPUR MAHILA URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1638,
        "bank_name": "UDGIR URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1639,
        "bank_name": "UDHAM SINGH NAGAR DISTRICT COOPERATIVE BANK LIMITE"
    },
    {
        "bank_id": 306,
        "bank_name": "UDYAM VIKAS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1692,
        "bank_name": "UJJAIN AUDHYOGIK VIKAS NAGRIK BANK"
    },
    {
        "bank_id": 1686,
        "bank_name": "UJJAIN NAGRIK SAHAKARI BANK "
    },
    {
        "bank_id": 1685,
        "bank_name": "UJJAIN PARASPAR SAHAKARI BANK "
    },
    {
        "bank_id": 1940,
        "bank_name": "UJJIVAN SMALL FINANCE BANK LIMITED DHARMANAGAR"
    },
    {
        "bank_id": 1641,
        "bank_name": "UMA COOPERATIVE BANK"
    },
    {
        "bank_id": 1688,
        "bank_name": "UMIYA URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1687,
        "bank_name": "UMIYA URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 980,
        "bank_name": "UMIYA URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1642,
        "bank_name": "UNION BANK OF INDIA"
    },
    {
        "bank_id": 1872,
        "bank_name": "UNION BANK OF INDIA CREDIT CARD"
    },
    {
        "bank_id": 1643,
        "bank_name": "UNITED BANK OF INDIA"
    },
    {
        "bank_id": 1922,
        "bank_name": "UNITED BANK OF INDIA, LANGPI DEHANGI RURAL BANK, D"
    },
    {
        "bank_id": 1644,
        "bank_name": "UNITED INDIA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1689,
        "bank_name": "UNITED MERC COOPERATIVE BANK "
    },
    {
        "bank_id": 1645,
        "bank_name": "UNITED OVERSEAS BANK LIMITED"
    },
    {
        "bank_id": 1695,
        "bank_name": "UNITED PURI NIMAPRA CENTRAL COOPERATIVE BANK "
    },
    {
        "bank_id": 307,
        "bank_name": "UNIVERSAL COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 1281,
        "bank_name": "UNJHA NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 308,
        "bank_name": "URBAN COOPERATIVE BANK "
    },
    {
        "bank_id": 693,
        "bank_name": "URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1838,
        "bank_name": "UTKAL GRAMYA BANK"
    },
    {
        "bank_id": 1646,
        "bank_name": "UTKARSH SMALL FINANCE BANK"
    },
    {
        "bank_id": 1647,
        "bank_name": "UTTAR BANGA KSHETRIYA GRAMIN BANK"
    },
    {
        "bank_id": 1648,
        "bank_name": "UTTAR BIHAR GRAMIN BANK"
    },
    {
        "bank_id": 1649,
        "bank_name": "UTTAR PRADESH COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1650,
        "bank_name": "UTTAR PRADESH STATE COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1933,
        "bank_name": "UTTARAKHAND GRAMIN BANK"
    },
    {
        "bank_id": 1651,
        "bank_name": "UTTARANCHAL GRAMIN BANK"
    },
    {
        "bank_id": 849,
        "bank_name": "UTTARKASHI ZILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1652,
        "bank_name": "UTTRAKHAND COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1653,
        "bank_name": "UTTRAKHAND STATE CO-COPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1640,
        "bank_name": "Ujjivan Small Finance Bank Limited"
    },
    {
        "bank_id": 282,
        "bank_name": "V.V.C.C BANK LIMITED"
    },
    {
        "bank_id": 1276,
        "bank_name": "VADNAGAR NAGARIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1679,
        "bank_name": "VAIJAPUR MERCHANTS BANK "
    },
    {
        "bank_id": 1683,
        "bank_name": "VAISH COOPERATIVE ADARSH BANK "
    },
    {
        "bank_id": 36,
        "bank_name": "VAISHYA NAGARI SAH BANK LIMITED"
    },
    {
        "bank_id": 35,
        "bank_name": "VAISHYA NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 788,
        "bank_name": "VAISHYA SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 37,
        "bank_name": "VALMIKI URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1274,
        "bank_name": "VALSAD DISRICT CENTRAL COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1654,
        "bank_name": "VANANCHAL GRAMIN BANK"
    },
    {
        "bank_id": 304,
        "bank_name": "VANI MERCHANTS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 302,
        "bank_name": "VARDHAMAN MAHILA COOPERATIVE URBAN BANK LIMITED"
    },
    {
        "bank_id": 296,
        "bank_name": "VASAI JANATA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1655,
        "bank_name": "VASAI VIKAS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1682,
        "bank_name": "VASANTDADA NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 290,
        "bank_name": "VEERASHAIVA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 284,
        "bank_name": "VEPAR UDYOG VIKAS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 911,
        "bank_name": "VIDARBHA MERCHANTS U.C.B. LIMITED"
    },
    {
        "bank_id": 1656,
        "bank_name": "VIDHARBHA KONKAN GRAMIN BANK LIMITED"
    },
    {
        "bank_id": 1570,
        "bank_name": "VIDYA BANK"
    },
    {
        "bank_id": 299,
        "bank_name": "VIDYANAND COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 979,
        "bank_name": "VIJAY COMMERCIAL COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 312,
        "bank_name": "VIJAY COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1658,
        "bank_name": "VIJAYA BANK"
    },
    {
        "bank_id": 1873,
        "bank_name": "VIJAYA BANK CREDIT CARD"
    },
    {
        "bank_id": 1659,
        "bank_name": "VIKAS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 796,
        "bank_name": "VIKAS SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 289,
        "bank_name": "VIKAS SAHAKARI BANK LIMITED "
    },
    {
        "bank_id": 297,
        "bank_name": "VIKAS SOUHARDA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1660,
        "bank_name": "VIKAS URBAN COOPERATIVE BANK"
    },
    {
        "bank_id": 1677,
        "bank_name": "VIKRAMADITYA NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 659,
        "bank_name": "VIKRAMADITYA NAGRIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1680,
        "bank_name": "VIMA KAMGAR COOPERATIVE BANK "
    },
    {
        "bank_id": 291,
        "bank_name": "VIRAJPET PATTANA SAHAKARA BANK "
    },
    {
        "bank_id": 183,
        "bank_name": "VISAKHAPATNAM MID CORPORATE BANK"
    },
    {
        "bank_id": 287,
        "bank_name": "VISHWAKALYAN SAHAKAR BANK "
    },
    {
        "bank_id": 286,
        "bank_name": "VISHWAKARAMA SAHAKARA BANK LIMITED"
    },
    {
        "bank_id": 1681,
        "bank_name": "VISHWAKARMA SAHAKARI BANK "
    },
    {
        "bank_id": 853,
        "bank_name": "VISHWANATHRAO PATIL MURGUD SAHAKARI BANK "
    },
    {
        "bank_id": 298,
        "bank_name": "VISHWAS COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1661,
        "bank_name": "VISL EMPLOYEES COOPERATIVE BANK"
    },
    {
        "bank_id": 660,
        "bank_name": "VIVEKANAND NAGRIK SAHAKARI BANK"
    },
    {
        "bank_id": 288,
        "bank_name": "VYAPARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1684,
        "bank_name": "VYAPARIK AUDYOGIK SAHAKARI BANK "
    },
    {
        "bank_id": 295,
        "bank_name": "VYAVASAYIK EVAM AUDHYOGIK SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1676,
        "bank_name": "VYAVSAYIK SAHAKARI BANK "
    },
    {
        "bank_id": 1662,
        "bank_name": "VYSYA COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1675,
        "bank_name": "WANA NAGARIK SAHAKARI BANK "
    },
    {
        "bank_id": 1674,
        "bank_name": "WANA NAGRI SAHAKARI BANK "
    },
    {
        "bank_id": 281,
        "bank_name": "WANI NAGRI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 30,
        "bank_name": "WARANGAL URBAN COOPERATIVE BANK LIMITED, AXIS BANK"
    },
    {
        "bank_id": 31,
        "bank_name": "WARANGAL URBAN COOPERATIVE BANK LIMITED, ICICI BAN"
    },
    {
        "bank_id": 1673,
        "bank_name": "WARDHA NAGRI BANK "
    },
    {
        "bank_id": 658,
        "bank_name": "WARDHA ZILLA PARISHAD EMPLOYEES URBAN COOPERATIVE "
    },
    {
        "bank_id": 1663,
        "bank_name": "WARDHAMAN URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 279,
        "bank_name": "WARDHMAN URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 277,
        "bank_name": "WARUD URBAN COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1664,
        "bank_name": "WESTPAC BANKING CORPORATION"
    },
    {
        "bank_id": 1665,
        "bank_name": "WOORI BANK"
    },
    {
        "bank_id": 1670,
        "bank_name": "YADAGIRI LNS COOPERATIVE BANK "
    },
    {
        "bank_id": 1666,
        "bank_name": "YADRAV COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 39,
        "bank_name": "YARAGATTI URBAN COOPERATIVE CREDIT BANK"
    },
    {
        "bank_id": 272,
        "bank_name": "YASHWANT NAGARI SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 274,
        "bank_name": "YEOLA MER COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 1668,
        "bank_name": "YES BANK"
    },
    {
        "bank_id": 1826,
        "bank_name": "YES BANK LIMITED, ARUNACHAL PRADESH SCB NAHARLAGUN"
    },
    {
        "bank_id": 977,
        "bank_name": "YESHWANT URBAN COOPERATIVE BANK LIMITED "
    },
    {
        "bank_id": 1669,
        "bank_name": "YLNS COOPERATIVE URBAN BANK "
    },
    {
        "bank_id": 275,
        "bank_name": "YOUTH DEVELOPMENT COOPERATIVE BANK LIMITED"
    },
    {
        "bank_id": 657,
        "bank_name": "ZILA SAHAKARI BANK LIMITED"
    },
    {
        "bank_id": 1667,
        "bank_name": "ZILA SAHAKARI BANK, YES BANK"
    },
    {
        "bank_id": 1886,
        "bank_name": "ZILA SAHKARI BANK LTD GHAZIABAD"
    },
    {
        "bank_id": 1915,
        "bank_name": "ZILA SAHKARI BANK LTD MUZAFFARNAGAR"
    },
    {
        "bank_id": 1938,
        "bank_name": "Zila Sahkari Bank Ltd  Bulandshahr"
    },
    {
        "bank_id": 1887,
        "bank_name": "banda district co-operative bank ltd"
    }
]


PAYOUT_TRANSACTION_STATUS = {
    0:	"Failed and Refunded",
    1:	"Success",
    2:	"Pending",
    3:	"Transaction In Process",
    4:	"On Hold"
}
