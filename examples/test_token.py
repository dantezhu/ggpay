# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

from ggpay import TokenHelper

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://www.example.com/oauth2callback'

helper = TokenHelper(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

# 可为 1、2
step_index = 1

if step_index == 1:
    # 先拿到这个url，去浏览器里登录
    print(helper.make_login_url())
elif step_index == 2:
    code = ''
    print(helper.get_token(code))