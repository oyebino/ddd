# -*- coding: utf-8 -*-
# @File  : conftest.py
# @Author: 叶永彬
# @Date  : 2019/11/22
# @Desc  :

from common.Req import Req
from common.parseTemplate import ParseTemplate
from Api.Login import Login, SentryLogin, AompLogin, CenterMonitorLogin,WeiXinLogin, OpenYDTLogin

import pytest
@pytest.fixture(scope="function")
def userLogin(request):
    if hasattr(request,'param'):
        user = ParseTemplate().formatExpected(request.param['user'])
        pwd = ParseTemplate().formatExpected(request.param['pwd'])
        L = Login(user,pwd)
    else:
        L = Login()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="function")
def sentryLogin(request):
    if hasattr(request,'param'):
        user = ParseTemplate().formatExpected(request.param['user'])
        pwd = ParseTemplate().formatExpected(request.param['pwd'])
        L = SentryLogin(user,pwd)
    else:
        L = SentryLogin()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="function")
def aompLogin(request):
    if hasattr(request, 'param'):
        user = ParseTemplate().formatExpected(request.param['user'])
        pwd = ParseTemplate().formatExpected(request.param['pwd'])
        L = AompLogin(user,pwd)
    else:
        L = AompLogin()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="function")
def weiXinLogin(request):
    if hasattr(request,'param'):
        user = ParseTemplate().formatExpected(request.param['user'])
        pwd = ParseTemplate().formatExpected(request.param['pwd'])
        L = WeiXinLogin(user,pwd)
    else:
        L = WeiXinLogin()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="function")
def centerMonitorLogin(request):
    if hasattr(request, 'param'):
        user = ParseTemplate().formatExpected(request.param['user'])
        pwd = ParseTemplate().formatExpected(request.param['pwd'])
        L = CenterMonitorLogin(user, pwd)
    else:
        L = CenterMonitorLogin()
    Session = L.login()
    return Req(Session)

@pytest.fixture(scope="function")
def openYDTLogin():
    """开放平台"""
    L = OpenYDTLogin()
    Session = L.login()
    return Req(Session)

#
# if __name__ == "__main__":
#
#     SYS()