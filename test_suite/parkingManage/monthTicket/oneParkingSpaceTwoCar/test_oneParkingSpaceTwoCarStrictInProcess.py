#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/07 14:35
# @Author  : 何涌
# @File    : test_oneParkingSpaceTwoCarStrictInProcess.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/oneParkingSpaceTwoCar/oneParkingSpaceTwoCarStrictInProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块-一位两车")
@allure.story('多位多车VIP转临时车严进')
class TestOneParkingSpaceTwoCarStrictInInProcess():
    """多位多车VIP转临时车严进"""

    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建多位多车月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'],isDynamicMode=send_data['isDynamicMode'])
        result = re
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用自多位多车月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNumList'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    # 多位多车VIP第一辆车进车
    def test_mockCarInA(self, sentryLogin, send_data, expect):
        """模拟车辆A进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["inscreenAMsg"])
        Assertions().assert_in_text(result['voice'], expect["invoiceAMsg"])

    def test_sentryCheckCarInHandleA(self,sentryLogin,send_data, expect):
        """岗亭端登记放行车辆A"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNumA'],send_data['carInHandleType'],'${mytest.carIn_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect["sentryCheckCarInHandleA"])

    def test_presentCarA(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNumA"])
        result = re[0]
        Assertions().assert_in_text(result['carNo'], expect["presentCarAMsg"])
        Assertions().assert_in_text(result['vipType'], expect["presentCarAvipTypeMsg"])

    # 多位多车VIP第二辆车进车
    def test_mockCarInB(self, send_data, expect):
        """模拟车B辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["inscreenB"])
        Assertions().assert_in_text(result['voice'], expect["invoiceB"])

    def test_sentryCheckCarInHandleB(self,sentryLogin,send_data, expect):
        """岗亭端登记放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNumB'],send_data['carInHandleType'],'${mytest.carIn_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect["sentryCheckCarInHandleB"])

    def test_presentCarB(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result['carNo'], expect["presentCarBMsg"])
        Assertions().assert_in_text(result['vipType'], expect["presentCarBvipTypeBMsg"])

    # 多位多车VIP第一辆车出车
    def test_mockCarOutA(self, send_data, expect):
        """模拟车辆A离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],1,send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["outScreenA"])
        Assertions().assert_in_text(result['voice'], expect["outVoiceA"])

    def test_sentryCheckOutCarA(self,sentryLogin,send_data, expect):
        """岗亭端确认放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNumA'], send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect["sentryCheckCarOutHandleA"])

    def test_carLeaveHistoryA(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNumA"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["carAInOutVipTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["carAInOutVipTypeMsg"])

    # 多位多车VIP第二辆车出车
    def test_mockCarOutB(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],1,send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["outscreenB"])
        Assertions().assert_in_text(result['voice'], expect["outvoiceB"])

    def test_sentryPay(self, sentryLogin,send_data, expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["carNumB"], send_data['carOutHandleType'], '${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect["sentryPayMsg"])

    def test_parkingBillDetail(self, userLogin, send_data, expect):
        """查看车辆B收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result, expect["parkingBillDetailB"])

    def test_carLeaveHistoryB(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["carInOutVipTypeStrMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["carInOutVipTypeStrMsg"])