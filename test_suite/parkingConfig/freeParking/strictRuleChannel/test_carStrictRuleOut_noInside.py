#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/06 11:15
# @Author  : 叶永彬
# @File    : test_carStrictRuleOut_noInside.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/freeParking/strictRuleChannel/carStrictRuleOutNoInside.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestCarLightRuleOutNoInside(BaseCase):
    """临时车无在场严出"""
    def test_mockCarOut(self,send_data,expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()
        self.save_data('carOut_jobId', result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkCarOut(self,sentryLogin,send_data,expect):
        """岗亭端登记放出"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],send_data['carOut_jobId'])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['voice'], expect["checkCarOutVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarOutIsOpenGate"])
        Assertions().assert_in_text(result['screen'], expect["checkCarOutScreen"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])

