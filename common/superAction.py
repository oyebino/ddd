#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 15:41
# @Author  : 叶永彬
# @File    : superAction.py
import random,string
import datetime,time
from datetime import timedelta
import uuid
import calendar

class SuperAction:

    def create_carNum(self, uppercase_num=1, digits_num=5, carType=None):
        """创建随机车牌"""
        ascii_uppercase = 'ABCDEGHJKLMNPQRSTWXY'
        src_digits = string.digits  # string_数字
        src_uppercase = ascii_uppercase  # string_大写字母
        src_greenFlat = 'DF'
        # 生成字符串
        carNum = random.sample(src_uppercase, int(uppercase_num)) + random.sample(src_digits, int(digits_num))
        greenSmallCarNum = random.sample(src_uppercase, int(uppercase_num)) + random.sample(src_greenFlat,1) +random.sample(src_digits, int(digits_num))
        # 列表转字符串
        if carType == "民航":
            new_carNum = "民航" + ''.join(carNum)[1:]
        elif carType == "新能源大车":
            new_carNum = "粤" + ''.join(carNum) + random.sample(src_greenFlat, 1)[0]
        elif carType == "新能源小车":
            new_carNum = "粤" + ''.join(greenSmallCarNum)
        else:
            new_carNum = "粤" + ''.join(carNum)
        return new_carNum

    def get_time(self,strType = "%Y%m%d%H%M%S"):
        dt = datetime.datetime.now()
        return dt.strftime(strType)

    def get_today_data(self):
        dt = datetime.date.today()
        return str(dt)

    def get_utcTime(self,strType="%Y-%m-%dT%H:%M:%S.001Z"):
        now = datetime.datetime.now()
        date = now - datetime.timedelta(seconds= 28800)
        return date.strftime(strType)

    def cal_get_utcTime(self,strType="%Y-%m-%dT%H:%M:%S.001Z",second=60,style = "+"):
        now = datetime.datetime.now()
        if style=="+":
            date = now - datetime.timedelta(seconds=28800) + datetime.timedelta(seconds=second)
        else:
            date = now - datetime.timedelta(seconds=28800) - datetime.timedelta(seconds=second)
        return date.strftime(strType)

    def cal_get_time(self,strType ="%Y%m%d%H%M%S", seconds = 1, style ="+"):
        now = datetime.datetime.now()
        if style=="+":
            date = now + datetime.timedelta(seconds = int(seconds))
        else:
            date = now - datetime.timedelta(seconds= int(seconds))
        return date.strftime(strType)

    def cal_get_day(self,strType ="%Y%m%d", days = 1, style ="+"):
        now = datetime.date.today()
        if style=="+":
            date = (now + datetime.timedelta(days = int(days))).strftime(strType)
        else:
            date = (now - datetime.timedelta(days = int(days))).strftime(strType)
        return date

    def get_uuid(self):
        uuidlist = str(uuid.uuid1()).split("-")
        newstr = ""
        for i in range(1, len(uuidlist)):
            newstr += uuidlist[i]
        return newstr


    def create_random_name(self):
        src_digits = string.digits
        name= "月票"+"".join(random.sample(src_digits, 4))
        return name

    def create_randomNum(self,val= 4):
        src_digits = string.digits
        value = "".join(random.sample(src_digits, int(val)))
        return value

    def changeDate(self,json):
        """
        深度把json数据体具有unicode转换成中文
        :param json:
        :return:
        """
        for key in json.keys():
            typeName = type(json.get(key))
            if typeName == list:
                for lister in json.get(key):
                    self.changeDate(lister)
            elif typeName == dict:
                self.changeDate(json.get(key))
            elif typeName == str:
                json.get(key).encode()
        return json

    def timestamp_to_format(self, timestamp=None, format='%Y-%m-%d %H:%M:%S'):
        """时间缀转日期格式，timestamp为空即当前时间"""
        if timestamp:
            timestamp = timestamp/1000
            time_tuple = time.localtime(timestamp)
            res = time.strftime(format, time_tuple)
        else:
            res = time.strftime(format)
        return res

    def cal_getTheMonth(self,date = None, n = 0, style='+'):
        """
        获取前N个月或后N个月日期
        :param date: '2020-01-09';
        :param n: 0是当前月份
        :param str: +， -
        :return: 默认返回当月‘2020-01-01 00：00：00 - 2020-01-31 00：00：00‘
        """
        if date == None:
            date = datetime.datetime.today()
            first_date = datetime.date(date.year, date.month, 1)
        else:
            if isinstance(date, str):
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            first_date = datetime.date(date.year, date.month, 1)
        month = date.month
        year = date.year
        if style == '+':
            for i in range(int(n)):
                if month == 12:
                    year += 1
                    month = 1
                else:
                    month += 1
        else:
            for i in range(int(n)):
                if month == 1:
                    year -= 1
                    month = 12
                else:
                    month -= 1
        _, days_in_month = calendar.monthrange(year, month)
        nMonth_date = datetime.date(year,month,day=1)
        if first_date > nMonth_date:
            tempDate = nMonth_date
            nMonth_date = first_date
            first_date = tempDate
        first_date = (datetime.datetime(first_date.year,first_date.month,day=1)).strftime('%Y-%m-%d %H:%M:%S')
        nMonth_date = datetime.datetime(nMonth_date.year,nMonth_date.month,day=1)
        end_date = (nMonth_date + timedelta(days = days_in_month) - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')

        return first_date +" - "+ end_date


        # 获取当前时间的自然月
    def get_now_natural_month(self):
        import calendar
        import datetime
        today = datetime.datetime.today()
        now_month = '%s-%s' % (today.year, today.month)
        monthRange = calendar.monthrange(today.year, today.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(now_month, now_month, monthRange)
        return timeperiodListStr

    # 获取当前时间的下个月的自然月
    def get_next_natural_month(self):
        import calendar
        import datetime
        from dateutil.relativedelta import relativedelta
        next_month_day = datetime.date.today() - relativedelta(months=-1)
        next_nonth = '%s-%s' % (next_month_day.year, next_month_day.month)
        monthRange = calendar.monthrange(next_month_day.year, next_month_day.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(next_nonth, next_nonth, monthRange)
        return timeperiodListStr

    # 获取当前时间的两个月的自然月
    def get_two_natural_month(self):
        import calendar
        import datetime
        from dateutil.relativedelta import relativedelta
        today = datetime.datetime.today()
        now_month = '%s-%s' % (today.year, today.month)
        next_month_day = datetime.date.today() - relativedelta(months=-1)
        next_nonth = '%s-%s' % (next_month_day.year, next_month_day.month)
        monthRange = calendar.monthrange(next_month_day.year, next_month_day.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(now_month, next_nonth, monthRange)
        return timeperiodListStr

    # 获取当前时间格式为："%Y-%m-%d %H:%M:%S"
    def get_now_time(self, strType="%Y-%m-%d %H:%M:%S"):
        dt = datetime.datetime.now()
        return dt.strftime(strType)

    # 获取当前时间的上个月的自然月
    def get_last_natural_month(self):
        import calendar
        import datetime
        from dateutil.relativedelta import relativedelta
        last_month_day = datetime.date.today() - relativedelta(months=1)
        last_nonth = '%s-%s' % (last_month_day.year, last_month_day.month)
        monthRange = calendar.monthrange(last_month_day.year, last_month_day.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(last_nonth, last_nonth, monthRange)
        return timeperiodListStr

if __name__ == "__main__":
    SA = SuperAction()
    openMonthNum = 2
    # date = SA.cal_getTheMonth(n=openMonthNum -1)
    date = SA.cal_get_day(strType='%Y-%m-%d',days=60)
    print(date)
