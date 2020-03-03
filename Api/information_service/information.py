#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 16:00
# @Author  : 叶永彬
# @File    : information.py

from common.Req import Req
from common.superAction import SuperAction as SA
import time
from urllib.parse import urlencode

class Information(Req):
    """
    信息查询
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}
    data = SA().get_today_data()

    def getPresentCar(self,parkName,carNum):
        """
        获取在场车场
        :param parkId:
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(),'name',parkName)
        data = {
            "page":1,
            "rp":1,
            "approchTimeFrom":self.data +" 00:00:00",
            "approchTimeTo":self.data +" 23:59:59",
            "parkIds":parkDict['value'],
            "parkSysType":1,
            "plate":carNum
        }
        self.url = "/mgr/park/presentCar/getPresentCar.do?" + urlencode(data)
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getCarLeaveHistory(self,parkName,carNum):
        """
        获取进出场记录
        :param parkId:
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":1,
            "fromLeaveTime":self.data + " 00:00:00",
            "toLeaveTime":self.data +" 23:59:59",
            "query_carNo":carNum,
            "parkIds":parkDict['value'],
            "parkSysType":1
        }
        self.url = "/mgr/park/carLeaveHistory/pageListParkingRecord.do?" + urlencode(data)
        time.sleep(5)
        re = self.get(self.api,headers= self.api_headers)
        return re

    def getParkingBillDetail(self,parkName,carNum):
        """
        获取收费记录
        :param parkId:
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        time.sleep(5)
        data = {
            "page":1,
            "rp":1,
            "query_payTimeFrom":self.data + " 00:00:00",
            "query_payTimeTo":self.data + " 23:59:59",
            "query_carCode":carNum,
            "parkIds":parkDict['value']
        }
        self.url = "/mgr/park/parkingBillDetail/list.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def getAdjustCarWaterNum(self,newCarCode,parkName):
        """
        获取校正流水
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "newCarCode":newCarCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkDict['value']
        }
        self.url = "/mgr/park/adjustCarRecord/getAdjustCarRecord.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re


    def getAbnormalInCar(self, parkName, carCode):
        """
        获取异常进场记录
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "carCode": carCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkDict['value'],
            "parkSysType": 1
        }
        self.url = "mgr/park/abnormalInCar/getAbnormalInCar.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def getAbnormalPicCar(self, parkName, carCode):
        """
        获取异常拍照记录
        :return:
        """
        parkDict = self.getDictBykey(self.__getParkingBaseTree().json(), 'name', parkName)
        data = {
            "page":1,
            "rp":20,
            "carCode": carCode,
            "modifyDateFrom": self.data + " 00:00:00",
            "modifyDateTo":self.data +" 23:59:59",
            "parkIds":parkDict['value'],
            "parkSysType": 1
        }
        self.url = "mgr/park/parkAbnormalPicCar/getParkAbnormalPicCar.do?" + urlencode(data)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def __getParkingBaseTree(self):
        """获取当前用户车场树信息"""
        self.url = "/mgr/parkingBaseData/getParkingBaseDataTree.do"
        re = self.get(self.api,headers=self.api_headers)
        return re

if __name__ == '__main__':
    # central("https://zbcloud.k8s.yidianting.com.cn").centralGetCharge()
    # re =Information_controller().centralPay("粤Q12347")
    re = Information()
    print(re.json())


