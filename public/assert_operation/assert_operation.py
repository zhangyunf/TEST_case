#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from public.util.log import *

class AssertOperation(object):

    def assert_check(self, case, res):
        '''
        检查测试点
        :param case: 案例事例
        :param requests_body: 请求响应体
        '''

        if case.expected_result != None:
            # 拆分断言
            check_list = case.expected_result.split(",")
            report = ""
            for expect in check_list:
                if expect != "" and expect != None:
                    try:
                        result = eval(expect)
                        if result:
                            log("案例%s执行成功%s" % (case.caseNum, expect))
                        else:
                            report += "\n检查点%s失败" % expect
                            log("案例%s执行失败，检查点%s失败" % (case.caseNum, expect))
                    except Exception as error:
                        report += "\n检查点%s失败" % expect
                        log("案例%s执行失败，检查点%s失败，发生错误%s" % (case.caseNum, expect, error))

            if report == "":
                case.set_actual_result("Success")
            else:
                # 设置案例执行状态为失败
                case.set_actual_result("False", report)






