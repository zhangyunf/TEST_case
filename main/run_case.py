#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from public.read_config.read_requests_data import ReadRequestsData
from public.util.combination_data import GetData
from public.util.my_requests import RunMain
from public.util.log import *
from public.read_config.request_config_read import ReadRequest
from public.assert_operation.assert_operation import AssertOperation
from public.util.database_operation import MysqlOperation
import time

class RunCase(object):

    def __init__(self, case_set, case_singleton):
        self.case_singleton = case_singleton
        self.assert_operation = AssertOperation()
        # 用例集
        self.case_set = case_set

    def run_case(self):
        # 执行案例
        read_requests_data = ReadRequestsData(self.case_set.set_name)
        requests = RunMain()
        host = "http://" + ReadRequest().get_url
        for case in self.case_set.run_case:
            if case.is_run == "YES":
                try:
                    log("开始执行案例%s" % case.caseNum)
                    # 执行sql
                    self.database_operation(case)
                    # 读取json
                    requests_data = read_requests_data.get_request_data(case, self.case_singleton.relevance_data)
                    # 发送请求
                    headers = None
                    token = None
                    if "YES" in case.is_headers:
                        # 整理数据
                        # 获取token
                        try:
                            token = self.case_singleton.relevance_data[case.is_headers.split(",")[-1]]
                        except Exception as error:
                            log("获取数据失败!")
                            continue
                        headers = read_requests_data.get_requests_header(case, token)
                        if headers == None or token == None:
                            log("执行案例%s发生错误" % case.caseNum)
                            continue
                    get_data = GetData(requests_data, token)
                    da1 = get_data.combination_data()
                    res = requests.run_main(host + case.url, case.requests_type, da1, headers)
                    if res != None:
                        self.save_assert(case, res)
                    else:
                        log("获取返回值为空")
                        case.set_actual_result("False", "获取返回值为空")
                    # 补充失败日志
                    if "False" in case.actual_result:
                        case.set_actual_result("False", "\n请求体：%s" % str(da1))
                        case.set_actual_result("False", "\n请求响应体：%s" % str(res))
                        log("案例%s执行失败" % case.caseNum)
                    else:
                        case.set_actual_result("Success", "\n请求响应体:%s" % str(res))
                        log("案例%s执行成功" % case.caseNum)
                except Exception as error:
                    log("执行案例%s发生错误%s" % case.caseNum, error)
            self.__end_time = time.time()

    def save_assert(self, case, res):
        # 保存依赖数据的
        self.case_singleton.save_relevance_data(case, res)
        # 比较预期结果
        self.assert_operation.assert_check(case, res, self.case_singleton.relevance_data)

    def database_operation(self, case):
        if case.database:
            s = MysqlOperation()
            s.database_operation(case, self.case_singleton.relevance_data)

    def create_report(self):
        '''生成EXCEL测试报告'''
        log("开始生成测试报告")
        from public.util.excel_operation import ExcelOperation
        from public.read_config.config import ReadConfig
        # 打开excel表读取数据
        config = ReadConfig()
        excel_operation = ExcelOperation(config.get_case_path)
        reader =  excel_operation.get_datas("case")
        # 填写结果
        for case in self.case_set.run_case:
            if case.is_run == "YES":
                try:
                    # 如果结果为空则写入执行失败
                    if case.actual_result == None:
                        case.set_actual_result("Flase", "执行失败，日志为空。")
                    color = config.get_success_color if "Success" in case.actual_result else config.get_failure_color
                    excel_operation.set_cell(reader[case.caseNum][14], color, case.actual_result)
                except Exception as error:
                    log("测试案例%s测试报告生成发生错误%s" % case.caseNum, error)
                    continue
        log("测试报告生成完成")

    def get_start_time(self):
        # 返回开始时间
        return time.strftime("%Y-%m-%d %H:%M", time.gmtime(self.__start_time))

    def get_elapsed_time(self):
        # 返回执行总时间
        return int(self.__end_time - self.__start_time)

    def get_cases(self):
        # 计算成功、失败的案例个数
        for case in self.case_set.run_case:
            if "YES" in case.is_run:
                if "Success" in case.actual_result:
                    self.case_set.pass_count += 1
                elif "False" in case.actual_result:
                    self.case_set.faile_count += 1















