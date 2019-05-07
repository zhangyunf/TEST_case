#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei
from case.case_excel_operation import CaseExcelOperation
from public.util.log import *

def SingletonDecorator(cls, *args, **kwargs):
    instance = {}

    def wrapper_singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
            return instance[cls]
    return wrapper_singleton


@SingletonDecorator
class CaseSingleton(object):

    def __init__(self):
        # 需要执行的案例
        self.case_list = []
        # 数据池
        self.relevance_data = {}

    def get_case_data(self):
        case_excel_operation = CaseExcelOperation()
        self.case_list = case_excel_operation.read_all_case_set()

    def get_all_case_count(self):
        '''获取通过的案例总数、失败的案例总数、未执行的总数'''
        all_count = 0
        pass_count = 0
        faile_count = 0
        no_run = 0
        for case_set in self.case_list:
            all_count += case_set.count
            pass_count += case_set.pass_count
            faile_count += case_set.faile_count
            no_run += case_set.no_run
        return [all_count,pass_count, faile_count, no_run]


    def save_relevance_data(self, case, res):
        '''
        保存依赖数据
        '''
        if case.relevance_data != None:
            relevance_list = case.relevance_data.split(",")
            report = ""
            for relevance in relevance_list:
                if relevance != "" and relevance != None:
                    try:
                        self.relevance_data.update(eval(relevance))
                    except Exception as error:
                        report = "\n保存%s失败" % relevance
                        log("保存%s发生错误%s" % (relevance, error))
                        log(res)
                    else:
                        log("保存%s----%s成功" % (relevance, self.relevance_data))
            if report != "":
                # 设置案例执行状态为失败
                case.set_actual_result("False", report)



