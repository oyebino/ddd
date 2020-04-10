#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 11:15
# @Author  : 叶永彬
# @File    : test_carStrictRuleInOut_noPay.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/freeParking/strictRuleChannel/carStrictRuleInOutNoPay.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-免费停车场")
@allure.story('临时车严进-不需缴费严出')
class TestCarStrictRuleInOutNoPay(BaseCase):
    """临时车严进，不需缴费严出"""
    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['carNum'],0,send_data['inClientID'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkCarIn(self,sentryLogin,send_data,expect):
        """岗亭端登记放入,查看车辆进场屏显，声音，开闸信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['inType'],send_data['carIn_jobId'])
        result = re
        Assertions().assert_in_text(result['voice'], expect["checkCarInVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarInIsOpenGate"])
        Assertions().assert_in_text(result['screen'], expect["checkCarInScreen"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkCarOut(self,sentryLogin,send_data,expect):
        """岗亭端登记放出,查看车辆进场屏显，声音，开闸信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['outType'],send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['voice'], expect["checkCarOutVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarOutIsOpenGate"])
        Assertions().assert_in_text(result['screen'], expect["checkCarOutScreen"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])

