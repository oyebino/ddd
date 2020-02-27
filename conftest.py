# -*- coding: utf-8 -*-
# @File  : conftest.py
# @Author: 叶永彬
# @Date  : 2019/11/22
# @Desc  :

from common.Req import Req
from Api.Login import Login, SentryLogin, AompLogin, WeiXinLogin
import pytest

@pytest.fixture(scope="class")
def userLogin(request):
    if hasattr(request,'param'):
        L = Login(request.param['user'],request.param['pwd'])
    else:
        L = Login()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="class")
def sentryLogin(request):
    if hasattr(request,'param'):
        L = SentryLogin(request.param['user'], request.param['pwd'])
    else:
        L = SentryLogin()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="class")
def aompLogin(request):
    if hasattr(request, 'param'):
        L = AompLogin(request.param['user'], request.param['pwd'])
    else:
        L = AompLogin()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="class")
def weiXinLogin(request):
    if hasattr(request,'param'):
        L = WeiXinLogin(request.param['user'], request.param['pwd'])
    else:
        L = WeiXinLogin()
    Session = L.login()
    return Req(Session)


"""

@pytest.fixture(scope="class")
def Login():

    S = requests.Session()

    headers ={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

    seccode = "http://47.106.221.58:5002/mgr/normal/authz/seccode.do"

    re = S.get(seccode)

    verify_seccode = "http://47.106.221.58:5002/mgr/normal/authz/verify_seccode.do"

    data = {"seccode": 9999}

    re = S.post(verify_seccode,data=data)

    print(re.text)


    url = "http://47.106.221.58:5002/mgr/normal/ajax/login.do"

    data = {
    "username": "autotest",
    "password": "123456",
    "seccode": 9999}

    re = S.post(url,data,headers=headers)

    return Req(S)

"""

#
# if __name__ == "__main__":
#
#     SYS()