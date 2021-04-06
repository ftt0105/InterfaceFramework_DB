import requests
import json


class HttpClient(object):
    def __init__(self):
        pass

    def request(self, reqUlr, reqMethode, paramsType, requestData, headers=None, cookies=None):
        # 处理所有http请求，包括post，get等
        if reqMethode.lower() == "post":
            if paramsType == "form":
                response = self.__post(reqUlr, data=json.dumps(requestData), headers=headers, cookies=cookies)
                return response
            elif paramsType == "json":
                response = self.__post(reqUlr, json=requestData, headers=headers, cookies=cookies)
                return response
        elif reqMethode.lower() == "get":
            if paramsType == "url":
                # 说明是将参数直接拼接到URL中
                reqUlr = "%s%s" % (reqUlr, requestData)
                response = self.__get(reqUlr, headers=headers, cookies=cookies)
                return response
            elif paramsType == "params":
                response = self.__get(reqUlr, requestData, headers=headers, cookies=cookies)
                return response

    def __post(self, url, data=None, json=None, headers=None, cookies=None):
        # 处理post类型中各种情况的请求
        response = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        return response

    def __get(self, url, params=None, headers=None, cookies=None):
        # 处理get类各种请求情况
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        return response



