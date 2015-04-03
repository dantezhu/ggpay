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
import requests

logger = logging.getLogger('ggpay')


class GGPay(object):
    """google支付"""

    client_id = None
    client_secret = None
    access_token = None

    def __init__(self, client_id, client_secret, access_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        
    def verify_bill(self, bill_id, package_name, product_id, purchase_token):
        """
        判断是否合法
        文档: https://developers.google.com/android-publisher/api-ref/purchases/products/get?hl=zh
        """
        logger.debug('purchase check start.bill_id: %s', bill_id)

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
        ))

        jdata = rsp.json()

        if 'purchaseState' not in jdata:
            logger.error('purchase invalid.bill_id: %s jdata: %s', bill_id, jdata)
            return False

        if jdata['purchaseState'] == 0 and jdata['developerPayload'] == 'DeveloperPayloadITEM%s' % bill_id:
            logger.error('purchase valid.bill_id: %s jdata: %s', bill_id, jdata)
            return True
        else:
            logger.error('purchase invalid.bill_id: %s jdata: %s', bill_id, jdata)
            return False
