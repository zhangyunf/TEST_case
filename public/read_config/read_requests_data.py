#-*- endcoding:utf-8 -*-
from public.read_config.config import readConfig
from public.read_config.request_config_read import readRequest
from public.util.log import *

class readRequestsData(object):

    def __init__(self):
        file_path = readConfig().get_requestsDataPath
        self.reader = {}
        try:
            with open(file_path, "r", encoding="utf-8") as requestsDataFile:
                requests_data = requestsDataFile.read()
                self.reader = eval(requests_data)
                log("获取全部请求数据成功!")
        except:
            log("获取全部请求数据失败!")

    def get_request_data(self, case, data_pool):
        try:
            #读取请求数据
            req_data = self.reader[case.requests_data][0]
            if case.relevance_field != None:
                # 替换依赖数据
                exchange_list = case.relevance_field.split(",")
                relenance_case = case.relevance_case.split(",")
                for exchange_data, exchange_case in zip(exchange_list, relenance_case):
                    try:
                        eval(exchange_data)
                    except:
                        log("更换%s中保存的数据%s失败" % (exchange_case, exchange_data))
                        case.set_actual_result("False", "\n更换数据失败%s" % exchange_data)

            log("获取%s的请求数据成功" % case.caseNum)
            return req_data
        except:
            log("获取%s的请求数据失败" % case.caseNum)
            return False


    def get_requests_header(self, case):
        header = self.reader[case.requests_data][1]
        header["token"] = readRequest().get_token
        log("获取%s的heasers数据成功" % case.caseNum)
        return header

if __name__ == "__main__":
    with open(r"D:\测试\自动化\TEST-case\data\order.json", "r", encoding="utf-8") as requestsDataFile:
        data = requestsDataFile.read()
        print(type(data))