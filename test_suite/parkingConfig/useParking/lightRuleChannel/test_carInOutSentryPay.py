#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/19 11:32
# @Author  : 叶永彬
# @File    : test_carInOutSentryPay.py


import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/useParking/lightRuleChannel/carInOutSentryPay.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-收费停车场")
@allure.story('临时车宽进-需缴费宽出(岗亭收费处收费放行)')
class TestCarInOutSentryPay(BaseCase):
    """临时车宽进，需缴费宽出（岗亭收费处收费放行）"""
    def test_mockCarIn(self, sentryLogin,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['carNum'],0,send_data['inClientID'])
        result = re
        Assertions().assert_in_text(result['screen'], expect["mockCarInScreen"])
        Assertions().assert_in_text(result['voice'], expect["mockCarInVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["mockCarInOpenGate"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        """离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费,看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['voice'], expect['checkCarOutVoice'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
