#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/06 11:15
# @Author  : 叶永彬
# @File    : test_carStrictRuleOut_noInside.py

import pytest
import allure
from common.utils import YmlUtils
from common.baseCase import BaseCase
from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/carInOut_service/carStrictRuleOutNoInside.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestCarLightRuleOutNoInside(BaseCase):
    """临时车无在场严出"""
    def test_mockCarOut(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()
        self.save_data('carOut_jobId', result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_mockCheckCarOut(self,send_data,expect):
        re = cloudparking_service().check_car_out(send_data['carNum'],send_data['carOutJobId'])
        result = re.json()['biz_content']['result']['open_gate']
        Assertions().assert_in_text(result, expect["isOpenGate"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])

