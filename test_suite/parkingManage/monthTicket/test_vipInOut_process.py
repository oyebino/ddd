#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 14:35
# @Author  : 何涌
# @File    : test_vipInOut_process.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket import MonthTicket
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service
import time

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/monthTicket_service.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class Test_vip_in_out():
    """月票创建、开通、进出车"""

    # 月票类型创建
    def test_create_vip_type(self,userLogin,send_data,expect):
        re = MonthTicket(userLogin).save_monthTicketType(send_data["ticketName"])
        result = re.json()
        Assertions().assert_in_text(result,expect["message"])

    # 开通月票
    def test_open_vip(self,userLogin,send_data,expect):
        re = MonthTicket(userLogin).open_monthTicket(send_data["carNum"], send_data["ticketName"])
        result = re.json()
        Assertions().assert_in_text(result,expect["message2"])

    # 开通月票后进车
    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        screen = "{}\\\\{}".format(send_data["carNum"], send_data["ticketName"])
        voice = "${}${}".format(send_data["carNum"], send_data["ticketName"])
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, screen)
        Assertions().assert_in_text(result, voice)

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, send_data["carNum"])

    # 开通月票后出车
    def test_mockCarOut(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()
        screen = "{}\\\\{}".format(send_data["carNum"], send_data["ticketName"])
        voice = "${}${}".format(send_data["carNum"], send_data["ticketName"])
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, screen)
        Assertions().assert_in_text(result, voice)

    def test_CarLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, send_data["carNum"])
    # # 月票续费
    # def test_renew_vip(self,userLogin,send_data,expect):
    #     re = monthTicket(userLogin).renew_monthTicket(send_data["carNum"], send_data["ticketName"])
    #     result = re.json()
    #     Assertions().assert_in_text(result,expect["message3"])
    #
    # # 月票退款
    # def test_refund_monthTicket(self,userLogin,send_data,expect):
    #     re = monthTicket(userLogin).refund_monthTicket(send_data["carNum"])
    #     result = re.json()
    #     Assertions().assert_in_text(result,expect["message4"])

