#-*- endcoding:utf-8 -*-
from case.case_model import CaseModel
from case.case_set import CaseSet
from public.util.excel_operation import ExcelOperation
from public.read_config.config import ReadConfig
from public.util.log import *

class CaseExcelOperation(object):

    def __init__(self):
        self.case_list = []
        config = ReadConfig()
        self.excel_operation = ExcelOperation(config.get_case_path)

    def read_case(self, case_set):
        '''读取交易集中的案例数据'''
        try:
            case_reader = self.excel_operation.get_datas(case_set.set_name)
            for k, v in case_reader.items():
                if k != "CaseNum" and k != None:
                    case_data = CaseModel(v)
                    case_set.run_case.append(case_data)
                    if case_data.is_run != "YES":
                        case_set.no_run += 1

        except Exception as error:
            log("读取案例数据发生错误%s", error)
        else:
            log("读取案例数据成功")

    def read_all_case_set(self):
        '''获取所有用例集'''
        set_reader = self.excel_operation.get_datas("首页")
        for k, v in set_reader.items():
            case_set = CaseSet(v)
            if case_set.is_run == "YES":
                # 读取用例集下案例信息
                self.read_case(case_set)
                self.case_list.append(case_set)
        return self.case_list

if __name__ == "__main__":
    a = CaseExcelOperation()
    a.read_all_case_set()