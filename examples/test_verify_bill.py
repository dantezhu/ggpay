# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

from ggpay import GGPay

CLIENT_ID = ''
CLIENT_SECRET = ''

refresh_token = ''
ggpay = GGPay(CLIENT_ID, CLIENT_SECRET, refresh_token)


print ggpay.verify_bill(1, 'com.xx.yy', 'item_1', '')
