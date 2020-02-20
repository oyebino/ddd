#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/19 15:19
# @Author  : 叶永彬
# @File    : test_adjustCarNumAndType.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOut_service.checkInOut_service import CheckInOut
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/carInOut_service/adjustCarNumAndType.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestAdjustCarNumAndType(BaseCase):
    """临时车进场车牌校正（同时校正车牌和车辆类型）"""
    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],0,send_data['inClientID'])
        result = re.json()
        self.save_data('carIn_jobId', result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarInMsg"])

    def test_adjustCarInNum(self,sentryLogin,send_data,expect):
        """校正进场车辆"""
        re = CheckInOut(sentryLogin).adjust_carNum_carType(send_data['parkUUID'],send_data['adjustCarNum'],send_data['adjustCarType'])
        result = re.json()['content']
        Assertions().assert_in_text(result['carNo'], expect["adjustCarNum"])
        Assertions().assert_in_text(result['carSizeTypeInt'], expect["adjustCarType"])

    def test_checkCarIn(self,sentryLogin,send_data,expect):
        """岗亭端登记放行"""
        re = CheckInOut(sentryLogin).check_car_in_out(send_data['parkUUID'])
        result = re
        Assertions().assert_in_text(result, expect["checkCarInMsg"])

    def test_checkCarInInof(self,send_data,expect):
        """查看校正后进场车辆屏显语音开闸"""
        re = cloudparking_service().get_car_msg_ytj(send_data['carIn_jobId'])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["checkCarInScreen"])
        Assertions().assert_in_text(result['voice'], expect["checkCarInVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarInOpenGate"])

    def test_checkAdjustCarInWaterNum(self,userLogin,send_data,expect):
        """查看校正进场车辆流水"""
        re = Information_controller(userLogin).getAdjustCarWaterNum(send_data['adjustCarNum'], send_data['parkId'])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["adjustCarInWaterNumMsg"])

    def test_mockCarOut(self,send_data,expect):
        """离场"""
        re = cloudparking_service().mock_car_in_out(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()
        self.save_data('carOut_jobId',result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_adjustCarOutNum(self,sentryLogin,send_data,expect):
        """校正出场车辆"""
        re = CheckInOut(sentryLogin).adjust_carNum_carType(send_data['parkUUID'], send_data['adjustCarNum'],send_data['adjustCarType'])
        result = re.json()['content']
        Assertions().assert_in_text(result['leaveCarNo'], expect["adjustCarNum"])
        Assertions().assert_in_text(result['carSizeTypeInt'], expect["adjustCarType"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费"""
        re = CheckInOut(sentryLogin).normal_car_out(send_data['parkUUID'])
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkCarOutInfo(self,send_data,expect):
        """查看车辆离场信息"""
        re = cloudparking_service().get_car_msg_ytj(send_data['carOut_jobId'])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['voice'], expect['checkCarOutVoice'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_checkAdjustCarOutWaterNum(self,userLogin,send_data,expect):
        """查看校正出场车辆流水"""
        re = Information_controller(userLogin).getAdjustCarWaterNum(send_data['adjustCarNum'], send_data['parkId'])
        result = re.json()
        Assertions().assert_in_text(result, expect["adjustCarOutWaterNumMsg"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["adjustCarNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
