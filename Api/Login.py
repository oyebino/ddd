# -*- coding: utf-8 -*-
# @File  : parkVisitorlist.py
# @Author: 叶永彬
# @Date  : 2019/11/16
# @Desc  :

from Config.Config import Config
from urllib.parse import urljoin
from common.logger import logger as log
import requests
import json

json_headers = {"Content-Type": "application/json;charset=UTF-8"}
form_headers = {"content-type": "application/x-www-form-urlencoded"}

class Login():
    def __init__(self,user=None,pwd=None):
        self.conf = Config()
        self.host = self.conf.host
        self.Seesion = requests.Session()
        if user == None and pwd == None:
            self.user = Config().getValue("user")
            self.password = Config().getValue("password")
        else:
            self.user = user
            self.password =pwd

    def login(self):
        seccode = urljoin(self.host,"/mgr/normal/authz/seccode.do")
        verify_seccode = urljoin(self.host,"/mgr/normal/authz/verify_seccode.do")
        url = urljoin(self.host,"/mgr/normal/ajax/login.do")
        headers ={
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        re = self.Seesion.get(seccode)
        data = {"seccode": 9999}
        re = self.Seesion.post(verify_seccode,data=data)
        data = {
            "username": self.user,
            "password": self.password,
            "seccode": 9999
        }
        re = self.Seesion.post(url,data,headers=headers)
        log.info(re.json()['message'])
        return self.Seesion


class SentryLogin():
    """岗亭端"""
    def __init__(self, host="https://zbcloud.k8s.yidianting.com.cn"):
        self.S = requests.Session()
        self.host = host
        self.user = Config().getValue("user")
        self.password = Config().getValue("password")

    def login(self):
        """登录并获取token"""
        url = self.host + "/user-service/api/sessions"
        data = {
            "user_id": self.user,
            "password": self.password
        }
        r = self.S.post(url=url, data=data, headers=form_headers).json()
        token = r['token']
        self.S.headers.update({"user": token,"type": "ydtp-pc"})

        if r['onDuty'] == 0:
            self.__select_channel()
        return self.S

    def __get_allChannel(self):
        """获取当前用户的全部通道"""
        url = self.host + "/ydtp-backend-service/api/sentry_user_parking"
        re = self.S.get(url=url)
        channelList = []
        channelInfoList = re.json()[0]['channels']
        for channelDict in channelInfoList:
            channelList.append(channelDict['id'])
        return channelList

    def __select_channel(self):
        """选择通道上班"""
        url = self.host + "/ydtp-backend-service/api/duty"
        channelCodeList = self.__get_allChannel()
        data = {
            "channel_ids": channelCodeList
        }
        r = self.S.post(url=url, data=data)
        print("***********",r.text)  # 登录成功后返回内容为空
        # if not r.json()['status'] == 200:
        #     log.info(r.json()['message'])


class AompLogin(object):

    def __init__(self):
        self.conf = Config()
        self.host = self.conf.aomp_host
        self.Session = requests.session()
        self.user = self.conf.aomp_user
        self.password = self.conf.aomp_pwd

    def checkCode(self):

        """"校验验证码"""
        loginUrl = self.host + "/checkLogin.do"
        data = {
            "user": "{}".format(self.user),
            "pwd": "{}".format(self.password),
            "validateCode": "9999",
            "isOnLine": "isOnLine",
            "flag": "-1"
        }
        self.Session.post(loginUrl, data)

    def login(self):

        """登陆aomp"""
        self.checkCode()
        path = self.host + "/admin/loginTomanage.do?flag=admin&flag=admin"
        data = {
            "flag": "admin"
        }
        self.Session.post(path, data)
        return self.Session

class WeiXin():
    def __init__(self):
        self.conf = Config()
        self.host = self.conf.weiXin_host
        self.S = requests.session()
        self.user = self.conf.aomp_user
        self.password = self.conf.aomp_pwd

    def login(self):
        loginUrl = self.host + "/mgr-weixin/passport/signin.do"
        data = {
            "username": "13531412589",
            "password": "123456"
        }
        self.S.post(loginUrl, data)
        return self.S


if __name__ == "__main__":

    # L = SentryLogin()

    # L.login()
    L = WeiXin()

    L.login()


