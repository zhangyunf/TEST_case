#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

class CaseModel(object):

    def __init__(self, caselist):

        # 案例编号
        self.caseNum = caselist[0].value

        # 模块名称
        self.module = caselist[1].value

        # 网址
        self.url = caselist[4].value

        # 是否执行
        self.is_run = caselist[5].value

        # 请求类型（POST/GET）
        self.requests_type = caselist[6].value

        # 是否携带headers
        self.is_headers = caselist[7].value

        # 依赖案例编号
        self.relevance_case = caselist[8].value

        # 需要保存的数据
        self.relevance_data = caselist[9].value

        # 依赖的数据
        self.relevance_field = caselist[10].value

        # 请求数据
        self.requests_data = caselist[11].value

        # 期望值
        self.expected_result = caselist[12].value

        # 实际运行结果
        self.actual_result = caselist[13].value

    def description(self):
        # 打印案例数据
        print("%s--%s--%s--%s--%s--%s--%s--%s--%s--%s--%s" %
              (self.caseNum, self.module, self.url, self.is_run,
               self.requests_type, self.relevance_case,
               self.relevance_data, self.relevance_field, self.requests_data, self.expected_result, self.actual_result))

    def set_actual_result(self, status, report=None):
        '''
        没有实际结果：成功失败都可以写入
        实际结果为成功,要写入的结果为失败：进行替换
        实际结果为失败，要写入的结果为失败：进行补充
        '''
        if self.actual_result == None:
            if status == "Success":
                self.actual_result = status
            else:
                self.actual_result = status + report
        elif "Success" in self.actual_result and status == "False":
            self.actual_result = status + report
        elif "False" in self.actual_result and status == "False":
            self.actual_result += report
