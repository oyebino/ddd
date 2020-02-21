"""
 Created by lgc on 2020/2/9 19:10.
 微信公众号：泉头活水
"""

import allure,os
import pytest

from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/recordInOut.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("pc查看进出场记录")


class TestSentryRecordInOut():

    """pc查看进出场记录"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"], 0, send_data["lightRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect["Message1"])

    def test_recordIn(self, sentryLogin, send_data, expect):
        """在pc端查看进场记录"""
        result2 = CarInOutHandle(sentryLogin).record_car_in()
        Assertions().assert_in_text(result2, expect['carNum1'])

    def test_mockCarout(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"], 1, send_data["lightRule_outClientID"])
        result = re.json()
        Assertions().assert_in_text(result2, expect['Message2'])

    def test_checkOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        result = CarInOutHandle(sentryLogin).normal_car_out(send_data['lightRule_parkUUID'])
        Assertions().assert_in_text(result3, expect["checkOutMsg"])

    def test_recordOut(self, sentryLogin, send_data, expect):

        """在pc端查看离场记录"""
        result4 = CarInOutHandle(sentryLogin).record_car_out()
        Assertions().assert_in_text(result4, expect['carNum2'])