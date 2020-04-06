from setuptools import setup, find_packages
setup(
    name="ggpay",
    version="0.3.2",
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['requests'],
    scripts=[],
    url="https://github.com/dantezhu/ggpay",
    license="MIT",
    author="dantezhu",
    author_email="dantezhu@qq.com",
    description="google支付订单验证",
)
