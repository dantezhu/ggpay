# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

from ggpay import GGPay

CLIENT_ID = ''
CLIENT_SECRET = ''

refresh_token = ''
ggpay = GGPay(CLIENT_ID, CLIENT_SECRET, refresh_token)

print('should_alloc_new_access_token:', ggpay.should_alloc_new_access_token())
print('alloc_new_access_token:', ggpay.alloc_new_access_token())

print('access_token:', ggpay.access_token)
print('access_token_create_time:', ggpay.access_token_create_time)
print('access_token_expire_time:', ggpay.access_token_expire_time)

print(ggpay.verify_bill('com.xx.yy', 'item_1', '', '1'))
