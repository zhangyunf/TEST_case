#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from case.case_singleton import CaseSingleton
from public.read_config.read_requests_data import ReadRequestsData
from public.util.combination_data import GetData
from public.util.my_requests import RunMain
from public.util.log import *
from public.read_config.request_config_read import ReadRequest
from public.assert_operation.assert_operation import AssertOperation

class RunCase(object):

    def __init__(self):
        self.case_singleton = CaseSingleton()
        self.case_singleton.read_case()
        self.read_requests_data = ReadRequestsData()
        self.requests = RunMain()
        self.host = ReadRequest().get_url
        self.assert_operation = AssertOperation()

    def run_case(self):
        for case in self.case_singleton.case_list:
            if case.is_run == "YES":
                try:
                    log("开始执行案例%s" % case.caseNum)
                    # 读取json
                    requests_data = self.read_requests_data.get_request_data(case, self.case_singleton.relevance_data)
                    # 发送请求
                    res = ""
                    if "YES" in case.is_headers:
                        # 整理数据
                        # 获取token
                        token = self.case_singleton.relevance_data[case.is_headers.split(",")[-1]]
                        get_data = GetData(requests_data, token)
                        da1 = get_data.combination_data()
                        headers = self.read_requests_data.get_requests_header(case, token)
                        res = self.requests.run_main(self.host + case.url, case.requests_type, da1, headers)
                        if res != None:
                            self.save_assert(case, res)
                        else:
                            log("获取返回值为空")
                            case.set_actual_result("False", "获取返回值为空")
                    elif "NO" in case.is_headers:
                        # 整理数据
                        get_data = GetData(requests_data)
                        da1 = get_data.combination_data()
                        res = self.requests.run_main(self.host + case.url, case.requests_type, da1)
                        self.save_assert(case, res)
                    # 补充失败日志
                    if "False" in case.actual_result:
                        case.set_actual_result("False", "\n请求响应体：%s" % str(res))
                        log("案例%s执行失败" % case.caseNum)
                    else:
                        log("案例%s执行成功" % case.caseNum)
                except Exception as error:
                    log("执行案例%s发生错误%s" % case.caseNum, error)

    def save_assert(self, case, res):
        # 保存依赖数据的
        self.case_singleton.save_relevance_data(case, res)
        # 比较预期结果
        self.assert_operation.assert_check(case, res)

    def create_report(self):
        log("开始生成测试报告")
        from public.util.excel_operation import ExcelOperation
        from public.read_config.config import ReadConfig
        # 打开excel表读取数据
        config = ReadConfig()
        excel_operation = ExcelOperation(config.get_case_path)
        excel_operation.get_datas("case")
        reader = excel_operation.get_readers()
        # 填写结果
        for case in self.case_singleton.case_list:
            if case.is_run == "YES":
                try:
                    # 如果结果为空则写入执行失败
                    if case.actual_result == None:
                        case.set_actual_result("Flase", "执行失败，日志为空。")
                    color = config.get_success_color if "Success" in case.actual_result else config.get_failure_color
                    excel_operation.set_cell(reader[case.caseNum][13], color, case.actual_result)
                except Exception as error:
                    log("测试案例%s测试报告生成发生错误%s" % case.caseNum, error)
                    continue
        log("测试报告生成完成")














