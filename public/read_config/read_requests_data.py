#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from public.read_config.config import ReadConfig
from public.read_config.request_config_read import ReadRequest
from public.util.log import *

class ReadRequestsData(object):

    '''读取请求数据文件中的数据'''

    def __init__(self):
        '''读取请求数据'''
        file_path = ReadConfig().get_requests_data_path
        self.reader = {}
        try:
            with open(file_path, "r", encoding="utf-8") as requests_data_file:
                requests_data = requests_data_file.read()
                self.reader = eval(requests_data)
                log("获取全部请求数据成功!")
        except:
            log("获取全部请求数据失败!")

    def get_request_data(self, case, data_pool):
        '''将有依赖的数据用数据池中对应的数据进行替换'''
        try:
            # 获取案例对应的请求数据的key值
            req_data = self.reader[case.requests_data][0]
            if case.relevance_field != None:
                # 获取需要替换的数据
                exchange_list = case.relevance_field.split(",")
                relenance_case = case.relevance_case.split(",")
                # 替换依赖数据
                for exchange_data, exchange_case in zip(exchange_list, relenance_case):
                    try:
                        eval(exchange_data)
                    except:
                        log("更换%s中保存的数据%s失败" % (exchange_case, exchange_data))
                        case.set_actual_result("False", "\n更换数据失败%s" % exchange_data)

            log("获取%s的请求数据成功" % case.caseNum)
            return req_data
        except:
            log("获取%s的请求数据失败" % case.caseNum)
            return False


    def get_requests_header(self, case):
        '''将对应的token替换进headers并返回headers'''
        headers = self.reader[case.requests_data][1]
        headers["token"] = ReadRequest().get_token
        log("获取%s的heasers数据成功" % case.caseNum)
        return headers

if __name__ == "__main__":
    with open(r"D:\测试\自动化\TEST-case\data\order.json", "r", encoding="utf-8") as requestsDataFile:
        data = requestsDataFile.read()
        print(type(data))