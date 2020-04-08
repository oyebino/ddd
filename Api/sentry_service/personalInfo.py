"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""
from urllib.parse import urlencode
from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}

class PersonalInfo(Req):
    """个人中心"""

    def webHandOverDuty(self,handUser,pwd):

        """交接班"""
        self.url = "/ydtp-backend-service/api/web_hand_over_duty"
        data = {
            "user_id": handUser,
            "password": pwd
        }
        re = self.post(url=self.zby_api,data=data, headers=form_headers)
        return re


    def offduty(self):

        """退出登录"""
        self.url = "/ydtp-backend-service/api/offduty"
        re = self.post(url=self.zby_api, headers=form_headers)
        return re

    def dutyInfo(self):

        """个人信息"""
        self.url = "/ydtp-backend-service/api/duty"
        re =self.get(url=self.zby_api, headers=form_headers)
        return re

    def __shiftRecords(self):
        """收费汇总列表"""
        data = {
            "pageNumber": 1,
            "pageSize": 1
        }
        self.url = "/ydtp-backend-service/api/shift_records?" + urlencode(data)
        re = self.get(self.zby_api)
        return re

    def shiftMoneys(self):
        """查看收费流水清单"""
        id = self.__shiftRecords().json()['list'][0]['id']
        data = {
            "pageNumber": 1,
            "pageSize": 20
        }
        self.url = "/ydtp-backend-service/api/shift_records/{}/shift_moneys?{}".format(id,urlencode(data))
        re = self.get(self.zby_api)
        return re.json()['list']


# class SentryLogin():
#     """sentryDutyRoom url"""
#
#     def __init__(self, token="", host="https://zbcloud.k8s.yidianting.com.cn"):
#         self.S = requests.Session()
#         self.token = token
#         self.host = host
#
#     def login(self,user_id,password):
#         """登录并获取token"""
#         url = self.host + "/user-service/api/sessions"
#         data = {
#             "user_id": user_id,
#             "password": password
#         }
#         r = self.S.post(url=url, data=data, headers=form_headers)
#         r_json = json.loads(r.text)
#         # d = r.json()
#         self.token = r_json['token']
#         print("token值为：", self.token)
#         return self.token
#
#     def select_channel(self,inChannelCode="2022",outChannelCode="2023"):
#         """登陆pc收费端"""
#         url = self.host + "/ydtp-backend-service/api/duty"
#         data = {
#             "channel_ids": "{},{}".format(inChannelCode, outChannelCode)
#         }
#         form_headers['user'] = self.token
#         form_headers['type'] = 'ydtp-pc'
#         r = self.S.post(url=url,data=data,headers=form_headers)
#         print("登录后返回：",r.text)  # 登录后没有任何内容返回，故需要status方法
#
#     def quit(self):
#         """退出登录"""
#         url = self.host + "/ydtp-backend-service/api/offduty"
#         form_headers['user'] = self.token
#         form_headers['type'] = 'ydtp-pc'
#         self.S.post(url=url, headers=form_headers)
#
#     def status(self):
#         """登录或退出检查点"""
#         url = self.host + "/ydtp-backend-service/api/duty_channel_status"
#         form_headers['user'] = self.token
#         form_headers['type'] = 'ydtp-pc'
#         r = self.S.get(url=url, headers=form_headers)
#         r_json = r.json()
#         print(r_json)
#         if 'message' in r_json:  # 未登录时返回的json有带message，已登录则没有
#             return "未登录"
#         else:
#             return "已登录"
