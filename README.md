# ggpay
google支付订单验证工具，包括一些辅助方法

### 使用说明

1. 去google developer api后台(https://console.developers.google.com/)

    1. 创建 project
    2. 进入创建好的project，找到 Google Play Android Developer API，并启用
    3. 创建 凭据。依次选择 OAuth 客户端ID -> 网页应用，注意配置的 Authorized redirect URIs(已获授权的重定向 URI)，必须与 test_token.py 中配置的一模一样，不能留空
    4. 将生成的 client id 和 client secret 填入 test_token.py
    5. 到 google play的应用详情页面，点击左侧 开发工具->服务和API，在右侧页面选择 在此应用中使用google play游戏服务，选择对应的project。之后在需要 关联应用 的时候，一定记得选择 网页应用，而不是安卓应用，并且一定要选择刚刚已经创建好的网页应用。

2. 先调用 test_token.py, 生成链接，放到浏览器中。

3. 登录授权，从跳转后的浏览器url中，copy出 code= 后面的那一段

    返回结果:
    https://www.example.com/oauth2callback?code=4/rHzLhBN6fLvHkDkuE1xSL84Fd9RAt6bMEh6VcAB-uMc.ktj2Uqik8dsagrKXntQAax0UZ6vJlwI

4. 修改 test_token.py 中的 step_index = 2, 并将 code 参数为刚才的参数，获取到access_token 以及 refresh_token 之类的数据。
返回结果:
{
    u'access_token': u'ya29.xwEFH0HUrmyxxx3Fb5bVK4q01QNtm9_EqyOD_URc2jsNT0TTwRPV9ZZ0VQEk4yCIVuu5', 
    u'token_type': u'Bearer', 
    u'expires_in': 3600, 
    u'refresh_token': u'1/31LHsuI-1-xxxxWCn77NMduH7V5_cULy3dw_qXLmA14'
}

此时获取的access_token其实没什么用，因为这个access_token会自动过期，真正用的access_token是用refresh_token兑换来的

5. 调用 test_verify_bill 来做验证


### 参考链接
    
验证支付:  
    https://developers.google.com/android-publisher/api-ref/purchases/products/get

身份认证:  
    https://developers.google.com/android-publisher/authorization
