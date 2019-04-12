#-*- endcoding:utf-8 -*-
from case.case import case
from public.util.excel_operation import exceOperation
from public.read_config.config import readConfig
from public.util.log import *

def singletonDecorator(cls, *args, **kwargs):
    instance = {}

    def wrapperSingleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
            return  instance[cls]
    return wrapperSingleton


@singletonDecorator
class caseSingleton(object):

    def __init__(self):
        self.caseList = []
        self.relevance_data = {}

    def read_case(self):
        '''读取case数据'''
        try:
            config = readConfig()
            exce_operation = exceOperation(config.get_casePath)
            exce_operation.get_datas("case")
            reader = exce_operation.get_readers()
            for key, j in reader.items():
                if key != "CaseNum" and key != None:
                    case_data = case(j)
                    self.caseList.append(case_data)
            log("读取案例数据成功")
        except:
            log("读取案例数据失败")

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
                        log("保存%s成功" % relevance)
                    except:
                        report = "\n保存%s失败" % relevance
                        log("保存%s失败" % relevance)
                        log(res)
            # 设置案例执行状态为失败
            case.set_actual_result("False", report)





















