# ggpay
google支付订单验证工具，包括一些辅助方法

### 使用说明

1. 去google developer api后台

    1. 创建 project
    2. 创建 web application
    3. 授权 google developer api
    4. 关联google play和该project

2. 先调用 test_token.py, 生成链接，放到浏览器中。

3. 登录授权，从跳转后的浏览器url中，copy出 code= 后面的那一段

    返回结果:
    https://www.example.com/oauth2callback?code=4/rHzLhBN6fLvHkDkuE1xSL84Fd9RAt6bMEh6VcAB-uMc.ktj2Uqik8dsagrKXntQAax0UZ6vJlwI

4. 修改 test_token.py 中的 step_index = 2, 并将 code 参数为刚才的参数，获取到token 以及 access_token 之类的数据。
返回结果:
{
  "access_token":"1/fFAGRNJru1FTz70BzhT3Zg",
  "expires_in":3920,
  "token_type":"Bearer"
}

5. 调用 test_verify_bill 来做验证
