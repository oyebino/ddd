#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 11:08
# @Author  : 叶永彬
# @File    : test_freeCouponVems.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.businessCoupon_service.coupon import Coupon
from Api.parkingManage_service.businessCoupon_service.weiXin import WeiXin
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/businessCoupon/freeCoupon.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-优惠劵管理")
@allure.story('免费券创建并使用')
class TestFreeCoupon():
    """免费券创建并使用"""
    def test_addCoupon(self,userLogin,send_data,expect):
        """新增优惠劵"""
        re = Coupon(userLogin).addCoupon(send_data["couponName"],send_data["parkName"],send_data["traderName"],send_data["couponType"])
        result = re
        Assertions().assert_in_text(result, expect["addCouponMessage"])

    def test_addSell(self,userLogin,send_data,expect):
        """售卖优惠劵"""
        re = Coupon(userLogin).addSell(send_data["couponName"],send_data["parkName"],send_data["traderName"])
        result = re
        Assertions().assert_in_text(result, expect["addSellMessage"])

    def test_sendCoupon(self,weiXinLogin,send_data,expect):
        """发放优惠劵"""
        re = WeiXin(weiXinLogin).grantCouponToCar(send_data["couponName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["sendCouponMessage"])

    def test_mockCarIn(self, sentryLogin,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarOut(self,send_data, expect):
        """模拟车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkParkingBillDetail(self,userLogin,send_data,expect):
        """查看收费流水"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkParkingBillDetailMessage"])

    def test_checkCouponSendList(self,userLogin,send_data,expect):
        """查看发放流水"""
        re = Coupon(userLogin).getCouponGrantList(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkCouponGrantListMessage"])

    def test_checkCouponUsedList(self,userLogin,send_data,expect):
        """查看使用流水"""
        re = Coupon(userLogin).getCouponSerialList(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["checkSerialListMessage"])