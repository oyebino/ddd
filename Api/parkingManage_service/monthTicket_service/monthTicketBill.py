#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 11:05
# @Author  : 叶永彬
# @File    : monthTicketBill.py

from common.Req import Req
from common.superAction import SuperAction as SA
from Api.index_service.index import Index
from urllib.parse import urlencode

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class MonthTicketBill(Req):
    """
    月票管理
    """
    data = SA().get_today_data()
    def openMonthTicketBill(self, carNum, ticketName, timeperiodListStr):
        """
        开通月票
        :param carNum:
        :param ticketName:
        :param timeperiodListStr: ‘2020-02-01 00:00:00 - 2020-02-29 23:59:59’
        :return:
        """
        if ',' in carNum:
            carNumList = carNum.split(',')
        else:
            carNumList = list()
            carNumList.append(carNum)
        ticketNameDict = self.getDictBykey(self.getValidCofigList().json(), 'ticketName', ticketName)
        if ticketNameDict['renewMethod'] == 'NATURAL_MONTH':
            openMonthNum = self.__getMonthCount(timeperiodListStr)
        elif ticketNameDict['renewMethod'] == 'CUSTOM':
            openMonthNum = self.__getDayCount(timeperiodListStr)
        price = self.__operationPrice(ticketNameDict['price'])

        json_data = {
        "monthTicketId": ticketNameDict['id'],
        "monthTicketName": ticketNameDict['ticketName'],
        "timeperiodListStr": timeperiodListStr,
        "userName": "pytest",
        "userPhone": "135{}".format(SA().create_randomNum(val=8)),
        "price": price,
        "totalValue": int(float(price) * openMonthNum * len(carNumList)),
        "openMonthNum": openMonthNum,
        "realValue": 10,
        "inviteCarTotal": len(carNumList),
        "dynamicCarportNumber": 1,
        "carCode": carNumList,
        }
        self.url = "mgr/monthTicketBill/open.do"
        re = self.post(self.api, data=json_data, headers=form_headers)
        return re

    def __getDayCount(self, str):
        """计算时间段的天数"""
        import time
        s1 = str.split(' - ')
        start = time.mktime(time.strptime(s1[0], '%Y-%m-%d %H:%M:%S'))
        end = time.mktime(time.strptime(s1[1], '%Y-%m-%d %H:%M:%S'))
        count_days = int((end - start) / (24 * 60 * 60))
        return count_days + 1

    def __getMonthCount(self, str):
        """计算时间段的月份个数"""
        from datetime import datetime
        s1 = str.split(' - ')
        end_date = s1[1]
        start_date = s1[0]
        year_end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').year
        month_end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').month
        year_start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').year
        month_start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').month
        interval = (year_end - year_start) * 12 + (month_end - month_start)
        return interval + 1


    def __operationPrice(self, price):
        """浮点数精度计算-针对月票单价/30=计算天数价格"""
        result = int(float(price) / 30 * 100) / 100 + 0.01
        return '{:.2f}'.format(result)

    def getMonthTicketBillList(self, parkName, carNum = "", combinedStatus=""):
        """
        获取已开通月票记录列表
        :param parkName:
        :param carNum:
        :param combinedStatus: 状态‘不在有效期，生效中，已退款’
        :return:
        """
        parkDict = self.getDictBykey(Index(self.Session).getParkingBaseDataTree().json(), 'name', parkName)
        statusDict = {
            "不在有效期":0,
            "生效中":1,
            "已退款":2,
            "":""
        }
        data = {
            "page":1,
            "rp":20,
            "query_parkId":parkDict['value'],
            "parkSysType":parkDict['parkSysType'],
            "query_carCode":carNum,
            "combinedStatus":statusDict[combinedStatus]
        }
        self.url = "/mgr/monthTicketBill/list.do?" + urlencode(data)
        re = self.get(self.api, headers=form_headers)
        return re

    def editOpenMonthTicketBill(self, parkName, carNum, editUser, status = '生效中'):
        """
        修改已开通月票
        :param parkName:
        :param carNum:
        :param editUser: 修改车主名
        :return:
        """
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, status).json(), 'carCode',carNum)
        isDynamicMode = self.__checkMonthTicketBillIsDynamicMode(monthTicketBillDict['id']).json()['data']['isDynamicMode']

        data = {
            "id":monthTicketBillDict['id'],
            "monthTicketId": monthTicketBillDict['monthTicketId'],
            "monthTicketName": monthTicketBillDict['ticketName'],
            "userName": editUser,
            "userPhone": monthTicketBillDict['userPhone'],
            "carCode": monthTicketBillDict['carCode'],
            "remark1":monthTicketBillDict['remark1'],
            "dynamicCarportNumber":monthTicketBillDict['dynamicCarportNumber'],
            "isDynamicMode": isDynamicMode,
            "supportVirtualCarcode":monthTicketBillDict['supportVirtualCarcode']
        }
        if self.__preeditMonthTicketBill(data).json()['status'] == 1:
            self.url = "/mgr/monthTicketBill/editMonthTicketBill.do"
            re =self.post(self.api, data = data, headers = form_headers)
            return re

    def __preeditMonthTicketBill(self, data):
        """预编辑"""
        self.url = "/mgr/monthTicketBill/preeditMonthTicketBill.do"
        re = self.post(self.api, data= data, headers = form_headers)
        return re

    def __checkMonthTicketBillIsDynamicMode(self, id):
        """查看月票记录详情"""
        data = {
            "id":id
        }
        self.url = "/mgr/monthTicketBill/checkMonthTicketBillIsDynamicMode.do?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def __findConfigNameList(self):
        """获取全部月票名"""
        self.url = "/mgr/commonFun/monthticket/findConfigNameList.do"
        re = self.get(self.api, headers = form_headers)
        return re

    def getValidCofigList(self):
        """获取月票类型list"""
        self.url = "/mgr/monthTicketBill/validConfigList.do"
        re = self.get(self.api, headers = form_headers)
        return re


    # def save_multipleSpace_multipleCar_monthTicketType(self,monthTicketName):
    #     """
    #
    #     创建月票类型（开启多位多车,开启在场转VIP）
    #     """
    #     self.url = "/mgr/monthTicketConfig/save.do"
    #     json_data = {
    #         "ticketName": monthTicketName,
    #         "ticketType": "OUTTER",
    #         "renew": 1,
    #         "price": 30,
    #         "renewMethod": "NATURAL_MONTH",
    #         "maxSellLimit": "NO",
    #         "financialParkId": 3751,
    #         "parkJson": const.parkJson,
    #         "renewFormerDays": 0,
    #         "inviteCarTotal": 1,
    #         "continueBuyFlag": 1,
    #         "supportVirtualCarcode": 0,
    #         "parkVipTypeJson": const.parkVipTypeJson_multipleCar,
    #         "inviteCarSwitcher": 0,
    #         "validTo": "2030-01-31 23:59:59",
    #         "sellFrom": SA().get_now_time(),
    #         "sellTo": SA().get_now_time(),
    #         "showMessage": const.showMessage
    #     }
    #     re = self.post(self.api, data=json_data, headers=self.api_headers)
    #     return re
    #
    #
    #
    # def open_last_monthTicket(self, carNum, monthTicketName):
    #     """
    #     开通月票(上个月月票，已过期)
    #     """
    #     self.url = "mgr/monthTicketBill/open.do"
    #     monthTicketIdSql = "select id from month_ticket_config where TICKET_NAME = '"+monthTicketName+"'"
    #     monthTicketId = db().select(monthTicketIdSql)
    #     json_data = {
    #     "monthTicketId": monthTicketId,
    #     "monthTicketName": monthTicketName,
    #     "timeperiodListStr": SA().get_last_natural_month(),
    #     "userName": "autotest",
    #     "userPhone": "15012345678",
    #     "price": 30,
    #     "totalValue": 30.00,
    #     "openMonthNum": 1,
    #     "realValue": 30,
    #     "inviteCarTotal": 1,
    #     "dynamicCarportNumber": 1,
    #     "carCode": carNum,
    #     }
    #     re = self.post(self.api, data=json_data, headers=self.api_headers)
    #     return re
    #
    # def renew_next_monthTicket(self, carNum, monthTicketName):
    #     """
    #     月票续费下个月的
    #     """
    #     self.url = "mgr/monthTicketBill/renew.do"
    #     monthTicketIdSql = "select id from month_ticket_config where TICKET_NAME = '"+monthTicketName+"'"
    #     monthTicketId = db().select(monthTicketIdSql)
    #     monthTicketBillIdSql = "select id from MONTH_TICKET_BILL where CAR_CODE = '"+carNum+"' ORDER BY id DESC LIMIT 1;"
    #     monthTicketBillId = db().select(monthTicketBillIdSql)
    #     json_data = {
    #     "monthTicketId": monthTicketId,
    #     "monthTicketName": monthTicketName,
    #     "monthTicketBillId": monthTicketBillId,
    #     "timeperiodListStr": SA().get_next_natural_month(),
    #     "userName": "autotest",
    #     "userPhone": "15012345678",
    #     "price": 30,
    #     "totalValue": 30.00,
    #     "openMonthNum": 1,
    #     "realValue": 30,
    #     "dynamicCarportNumber": 1,
    #     }
    #     re = self.post(self.api, data=json_data, headers=self.api_headers)
    #     return re
    #
    # def renew_two_monthTicket(self, carNum, monthTicketName):
    #     """
    #     月票续费这两个月的
    #     """
    #     self.url = "mgr/monthTicketBill/renew.do"
    #     monthTicketIdSql = "select id from month_ticket_config where TICKET_NAME = '"+monthTicketName+"'"
    #     monthTicketId = db().select(monthTicketIdSql)
    #     monthTicketBillIdSql = "select id from MONTH_TICKET_BILL where CAR_CODE = '"+carNum+"' ORDER BY id DESC LIMIT 1;"
    #     monthTicketBillId = db().select(monthTicketBillIdSql)
    #     json_data = {
    #     "monthTicketId": monthTicketId,
    #     "monthTicketName": monthTicketName,
    #     "monthTicketBillId": monthTicketBillId,
    #     "timeperiodListStr": SA().get_two_natural_month(),
    #     "userName": "autotest",
    #     "userPhone": "15012345678",
    #     "price": 30,
    #     "totalValue": 30.00,
    #     "openMonthNum": 1,
    #     "realValue": 30,
    #     "dynamicCarportNumber": 1,
    #     }
    #     re = self.post(self.api, data=json_data, headers=self.api_headers)
    #     return re

    def renewMonthTicketBill(self, parkName, carNum, refundValue, status):
        """
        月票续费，默认续费30天
        :param parkName:
        :param carNum:
        :param refundValue: 续费折扣价格
        :param status: 月票有效状态：
        :return:
        """
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, status).json(), 'carCode', carNum)
        self.url = "/mgr/monthTicketBill/renew.do"
        if monthTicketBillDict['renewMethod'] == 'NATURAL_MONTH':
            openMonthNum = 1
            timeperiodListStr = SA().cal_getTheMonth(n = openMonthNum - 1)
        else:
            openMonthNum = 30
            timeperiodListStr = SA().get_today_data() + " 00:00:00 - " + SA().cal_get_day(strType='%Y-%m-%d', days=int(openMonthNum)) + " 23:59:59"
        price = self.__operationPrice(monthTicketBillDict['price'])
        data = {
            "monthTicketId": monthTicketBillDict['monthTicketId'],
            "monthTicketName": monthTicketBillDict['ticketName'],
            "monthTicketBillId": monthTicketBillDict['id'],
            "timeperiodListStr": timeperiodListStr,
            "userName": monthTicketBillDict['userName'],
            "userPhone": monthTicketBillDict['userPhone'],
            "price": price,
            "totalValue": monthTicketBillDict['totalValue'],
            "openMonthNum": openMonthNum,
            "realValue": refundValue,
            "remark1": 'pytest续费',
            "dynamicCarportNumber": monthTicketBillDict['dynamicCarportNumber'],
        }
        re = self.post(self.api, data= data, headers = form_headers)
        return re


    def refundMonthTicketBill(self, parkName, carNum, refundValue):
        """
        月票退款
        """
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, '生效中').json(), 'carCode', carNum)
        realValue = (monthTicketBillDict['totalValue'] - monthTicketBillDict['reliefValue']) * 100
        json_data = {
        "monthTicketBillId": monthTicketBillDict['id'],
        "refundValue": refundValue,
        "remark": "pytest接口退款",
        "realValue": realValue
        }
        if realValue < refundValue * 100:
            print("退款金额不能大于实付金额")
        else:
            self.url = "mgr/monthTicketBill/refund.do"
            re = self.post(self.api, data=json_data, headers=self.api_headers)
            return re

    def getListBillUpdateRecord(self, parkName, carNum):
        """查看月票日志"""
        monthTicketBillDict = self.getDictBykey(self.getMonthTicketBillList(parkName, carNum, '生效中').json(), 'carCode',carNum)
        data = {
            "monthTicketBillId": monthTicketBillDict['id'],
            "page":1,
            "rp":1
        }
        self.url = '/mgr/monthTicketBill/listBillUpdateRecord?' + urlencode(data)
        re =self.get(self.api, headers = form_headers)
        return re

if __name__ == "__main__":
    pass