# -*- coding: utf-8 -*-

"""
#=============================================================================
#
#     FileName: ggpay.py
#         Desc: 
#
#       Author: dantezhu
#        Email: dantezhu@qq.com
#     HomePage: http://www.vimer.cn
#
#      Created: 2015-04-03 17:48:34
#      Version: 0.0.1
#      History:
#               0.0.1 | dantezhu | 2015-04-03 17:48:34 | init
#
#=============================================================================
"""

import logging
import datetime
import requests

logger = logging.getLogger('ggpay')


class GGPay(object):
    """google支付"""

    client_id = None
    client_secret = None
    access_token = None

    refresh_token = None
    access_token_create_time = None
    access_token_expire_time = None

    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def alloc_new_access_token(self):
        """
        通过refresh_token获取access token
        """

        base_url = 'https://accounts.google.com/o/oauth2/token'

        data = dict(
            grant_type='refresh_token',
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=self.refresh_token,
            )

        try:
            rsp = requests.post(base_url, data=data, verify=False)
            jdata = rsp.json()

            if 'access_token' in jdata:
                self.access_token = jdata['access_token']
                self.access_token_create_time = datetime.datetime.now()
                self.access_token_expire_time = self.access_token_create_time + datetime.timedelta(
                    seconds=jdata['expires_in'] * 2 / 3
                )
                return True
            else:
                logger.error('no access_token: %s', rsp.text)
                return False
        except:
            logger.error('exc occur.', exc_info=True)
            return False

    def should_alloc_new_access_token(self):
        """
        判断是否要重新获取access_token
        """
        if not self.access_token:
            return True

        now = datetime.datetime.now()
        if now >= self.access_token_expire_time:
            return True

        return False

    def verify_bill(self, bill_id, package_name, product_id, purchase_token):
        """
        判断订单是否合法
        需要注意，客户端在调用支付的时候需要把 bill_id 传给 extra 字段
        文档: https://developers.google.com/android-publisher/api-ref/purchases/products/get?hl=zh
        """
        logger.debug('purchase check start.bill_id: %s', bill_id)

        if self.should_alloc_new_access_token():
            if not self.alloc_new_access_token():
                return False

        # 这是老版
        # url_tpl = 'https://www.googleapis.com/androidpublisher/v1.1/applications/{packageName}/inapp/{productId}/purchases/{token}'
        url_tpl = 'https://www.googleapis.com/androidpublisher/v2/applications/{packageName}/purchases/products/{productId}/tokens/{token}'

        url = url_tpl.format(
            packageName=package_name,
            productId=product_id,
            token=purchase_token,
        )

        rsp = requests.get(url, params=dict(
            access_token=self.access_token,
        ), verify=False)

        if not rsp.ok:
            logger.error('purchase invalid. status_code: %s, rsp: %s', rsp.status_code, rsp.text)
            return False

        jdata = rsp.json()

        if 'purchaseState' not in jdata:
            logger.error('purchase invalid.bill_id: %s jdata: %s', bill_id, jdata)
            return False

        if jdata['purchaseState'] == 0 and str(jdata['developerPayload']) == str(bill_id):
            logger.error('purchase valid.bill_id: %s jdata: %s', bill_id, jdata)
            return True
        else:
            logger.error('purchase invalid.bill_id: %s jdata: %s', bill_id, jdata)
            return False
