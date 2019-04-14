#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from case.case import CaseModel
from public.util.excel_operation import ExcelOperation
from public.read_config.config import ReadConfig
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
        self.case_list = []
        self.relevance_data = {}

    def read_case(self):
        '''读取case数据'''
        try:
            config = ReadConfig()
            excel_operation = ExcelOperation(config.get_case_path)
            excel_operation.get_datas("case")
            reader = excel_operation.get_readers()
            for k, v in reader.items():
                if k != "CaseNum" and k != None:
                    case_data = CaseModel(v)
                    self.case_list.append(case_data)
        except Exception as error:
            log("读取案例数据发生错误%s", error)
        else:
            log("读取案例数据成功")

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
                        log("保存%s成功" % relevance)
            # 设置案例执行状态为失败
            case.set_actual_result("False", report)
