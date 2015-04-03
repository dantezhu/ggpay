# -*- coding: utf-8 -*-
from ggpay import GGPay

CLIENT_ID = ''
CLIENT_SECRET = ''

access_token = ''
ggpay = GGPay(CLIENT_ID, CLIENT_SECRET, access_token)


print ggpay.verify_bill(1, 'com.xx.yy', 'item_1', '')
