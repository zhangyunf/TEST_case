from case.case_singleton import caseSingleton
from public.read_config.read_requests_data import readRequestsData
from public.util.combination_data import getData
from public.util.my_requests import RunMain
from public.util.log import *
from public.read_config.request_config_read import readRequest
from public.assert_operation.assert_operation import assertOperation

class runCase(object):

    def __init__(self):
        self.case_singleton = caseSingleton()
        self.case_singleton.read_case()
        self.read_requests_data = readRequestsData()
        self.requests = RunMain()
        self.token = readRequest().get_token
        self.host = readRequest().get_url
        self.assert_operation = assertOperation()

    def run_case(self):
        for case in self.case_singleton.caseList:
            if case.is_run == "YES":
                try:
                    log("开始执行案例%s" % case.caseNum)
                    # 读取json
                    requests_data = self.read_requests_data.get_request_data(case, self.case_singleton.relevance_data)
                    # 整理数据
                    getdata = getData(requests_data, self.token)
                    da1 = getdata.combinationData()
                    # 发送请求
                    res = ""
                    if case.is_headers == "YES":
                        headers = self.read_requests_data.get_requests_header(case)
                        res = self.requests.run_main(self.host + case.url, case.requests_type, da1, headers)
                        if res != None:
                            self.save_assert(case, res)
                        else:
                            log("获取返回值为空")
                            case.set_actual_result("False", "获取返回值为空")

                    elif case.is_headers == "NO":
                        res = self.requests.run_main(self.host + case.url, case.requests_type, da1)
                        self.save_assert(case, res)
                    # 补充失败日志
                    if "False" in case.actual_result:
                        case.set_actual_result("False", "\n请求响应体：%s" % str(res))
                        log("案例%s执行失败" % case.caseNum)
                    else:
                        log("案例%s执行成功" % case.caseNum)
                except:
                    log("执行案例%s失败" % case.caseNum)


    def save_assert(self, case, res):
        # 保存依赖数据的
        self.case_singleton.save_relevance_data(case, res)
        # 比较预期结果
        self.assert_operation.assert_check(case, res)

    def create_report(self):
        log("开始生成测试报告")
        from public.util.excel_operation import exceOperation
        from public.read_config.config import readConfig
        #打开excel表读取数据
        config = readConfig()
        exce_operation = exceOperation(config.get_casePath)
        exce_operation.get_datas("case")
        reader = exce_operation.get_readers()
        # 填写结果
        for case in self.case_singleton.caseList:
            if case.is_run == "YES":
                try:
                    #如果结果为空则写入执行失败
                    if case.actual_result == None:
                        case.set_actual_result("Flase", "执行失败，日志为空。")
                    color = config.get_successColor if "Success" in case.actual_result else config.get_failureColor
                    exce_operation.set_cell(reader[case.caseNum][-1], color, case.actual_result)
                except:
                    log("测试案例%s测试报告生成失败" % case.caseNum)
                    continue
        log("测试报告生成完成")














