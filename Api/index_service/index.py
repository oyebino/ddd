#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 17:58
# @Author  : 叶永彬
# @File    : index.py

from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class Index(Req):
    """首页接口"""
    def getNewMeun(self):
        self.url = "/mgr/main/newmenu.do"
        re = self.get(self.api, headers = json_headers)
        return re