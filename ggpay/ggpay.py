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

    def verify_bill(self, package_name, product_id, purchase_token, payload=None):
        """
        判断订单是否合法
        需要注意，如果验证payload，需要客户端在调用支付的时候需要把 payload 赋值
        文档: https://developers.google.com/android-publisher/api-ref/purchases/products/get?hl=zh
        http.rsp:
            {
              "kind": "androidpublisher#productPurchase",
              "purchaseTimeMillis": long,
              "purchaseState": integer,
              "consumptionState": integer,
              "developerPayload": string,
              "orderId": string,
              "purchaseType": integer,
              "acknowledgementState": integer
            }

            Property name	Value	Description	Notes
            acknowledgementState	integer	The acknowledgement state of the inapp product. Possible values are:
            Yet to be acknowledged
            Acknowledged
            consumptionState	integer	The consumption state of the inapp product. Possible values are:
            Yet to be consumed
            Consumed
            developerPayload	string	A developer-specified string that contains supplemental information about an order.
            kind	string	This kind represents an inappPurchase object in the androidpublisher service.
            orderId	string	The order id associated with the purchase of the inapp product.
            purchaseState	integer	The purchase state of the order. Possible values are:
            Purchased
            Canceled
            Pending
            purchaseTimeMillis	long	The time the product was purchased, in milliseconds since the epoch (Jan 1, 1970).
            purchaseType	integer	The type of purchase of the inapp product. This field is only set if this purchase was not made using the standard in-app billing flow. Possible values are:
            Test (i.e. purchased from a license testing account)
            Promo (i.e. purchased using a promo code)
            Rewarded (i.e. from watching a video ad instead of paying)
        :param package_name:
        :param product_id:
        :param purchase_token:
        :param payload:
        :return: 成功: Google订单ID；失败: False
        """
        logger.debug('purchase check start.')

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
            logger.error('purchase invalid. jdata: %s', jdata)
            return False

        if jdata['purchaseState'] == 0:
            if payload is not None and jdata['developerPayload'] != payload:
                logger.error('purchase valid. jdata: %s, payload: %s', jdata, payload)
                return False
            return jdata['orderId']
        else:
            logger.error('purchase valid. jdata: %s, payload: %s', jdata, payload)
            return False
