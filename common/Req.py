# -*- coding: utf-8 -*-
# @File  : base.py
# @Author: 叶永彬
# @Date  : 2018/11/15
# @Desc  :
import requests
import time
from common.superAction import SuperAction as SA
from  Config.parameter import Parameter

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Config.Config import Config

from common.logger import logger

from urllib.parse import urljoin


class Req(requests.Session):
    """
    http请求的基础类
    """

    def __init__(self,Session=None):
        super(Req, self).__init__()

        self.conf = Config()
        self.host = self.conf.host
        if Session == None:
            self.Session = requests.Session()
        else:
            self.Session = Session

    def _api(self,url):
        """host + api_url"""
        full_url = urljoin(self.host,url)
        return full_url

    @property
    def api(self):
        """调用接口地址"""
        return self._api(self.url)

    @property
    def api_headers(self):
        return self.api_headers

    def request(self, method, url, name=None, **kwargs):
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method:
            method for the new :class:`Request` object.
        :param url:
            URL for the new :class:`Request` object.
        :param name: (optional)
            Placeholder, make compatible with Locust's HttpSession
        :param params: (optional)
            Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional)
            Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional)
            Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional)
            Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How long to wait for the server to send data before giving up, as a float, or \
            a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Set to True by default.
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional)
            whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional)
            if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        # response = requests.Session.request(self, method, url, **kwargs)
        response = self.Session.request(method, url, **kwargs)
        # logger.info("Request Method:{}".format(method))
        # logger.info("Request URL:{}".format(url))
        # logger.info("Request Payload:{}".format(kwargs))
        # logger.info("Response Data :{}".format(response.text))
        return response

    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        result = self.request('GET', url, **kwargs)
        self.getLogFormat(url,kwargs,result)
        return result

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        result = self.request('POST', url, data=data, json=json, **kwargs)
        self.postLogFormat(url,data,json,result)
        time.sleep(5)
        return result

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('DELETE', url, **kwargs)

    def postLogFormat(self,url,data,json,result):
        """
        日志打印格式
        :param url:
        :param data:
        :param json:
        :param result:
        :return:
        """
        logger.info("===请求方式:{}".format('POST'))
        logger.info("===请求路径:{}".format(url))
        if json == None:
            logger.info("===请求参数:{}".format(data))
        else:
            logger.info("===请求参数:{}".format(json))
        logger.info("===返回状态码:{}".format(result.status_code))
        if "mock" in url:
            logger.info("===返回结果:{}".format(SA().changeDate(eval(result.text))))
        else:
            logger.info("===返回结果:{}".format(result.text))


    def getLogFormat(self,url,kwargs,result):
        """
        get方式的日志打印格式
        :param url:
        :param kwargs:
        :param result:
        :return:
        """
        logger.info("===请求方式:{}".format('GET'))
        logger.info("===请求路径:{}".format(url))
        logger.info("===请求参数:{}".format(kwargs))
        logger.info("===返回状态码:{}".format(result.status_code))
        logger.info("===返回结果:{}".format(result.text))



