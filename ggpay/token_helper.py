# -*- coding: utf-8 -*-

import urllib
import requests


class TokenHelper(object):
    """用来生成token的工具"""

    client_id = None
    client_secret = None
    redirect_uri = None

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def make_login_url(self):
        """获取登录用的url
        """

        base_url = 'https://accounts.google.com/o/oauth2/auth'

        params = dict(
            scope='https://www.googleapis.com/auth/androidpublisher',
            response_type='code',
            access_type='offline',
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            approval_prompt='force',  # 加了这个参数，code才能兑换出refresh token。提示会增加一个离线访问权限
        )

        url = base_url + '?' + urllib.urlencode(params)

        return url

    def get_token(self, code):
        """登录之后，获取access_token
        """
        base_url = 'https://accounts.google.com/o/oauth2/token'

        data = dict(
            grant_type='authorization_code',
            code=code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )

        rsp = requests.post(base_url, data=data, verify=False)

        return rsp.json()
