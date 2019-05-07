#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from main.run_case import RunCase
from case.case_singleton import CaseSingleton
from public.util.log import *
from  public.util.HTML_test_report import HTMLTestRunner
from public.util.send_email import SendEmail
class Run(object):

    def __init__(self):
        self.case_singleton = CaseSingleton()

    def run(self):
        self.case_singleton.get_case_data()
        for case_set in self.case_singleton.case_list:
            try:
                log("开始执行用例集%s" % case_set.set_name)
                runCase = RunCase(case_set, self.case_singleton)
                runCase.run_case()
                runCase.get_cases()
            except Exception as error:
                log("发生错误%s,用例集执行%s失败" % (error, case_set.set_name))
                continue
            else:
                log("用例集%s执行完成"% case_set.set_name)


    def report(self):
        log("开始生成HTML报告")
        # 整理数据
        all_data = self.case_singleton.get_all_case_count()
        all_data.append(self.case_singleton.case_list)
        # 生成测试报告
        html_report = HTMLTestRunner("接口自动化测试报告")
        html_report.generateReport(all_data)
        log("结束生成HTML报告")
        return html_report.SUBJECTHTML

    def send_report(self, message_body):
        log("开始发送邮件")
        send = SendEmail()
        send.send_email(message_body)
        log("结束发送邮件")



if __name__ == "__main__":
    a = Run()
    a.run()
    email_object = a.report()
    a.send_report(email_object)
