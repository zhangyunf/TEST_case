#-*- endcoding:utf-8 -*-

class case(object):

    def __init__(self, caselist):
        self.caseNum = caselist[0].value
        self.module = caselist[1].value
        self.url = caselist[4].value
        self.is_run = caselist[5].value
        self.requests_type = caselist[6].value
        self.is_headers = caselist[7].value
        self.relevance_case = caselist[8].value
        self.relevance_data = caselist[9].value
        self.relevance_field = caselist[10].value
        self.requests_data = caselist[11].value
        self.expected_result = caselist[12].value
        self.actual_result = caselist[13].value

    def description(self):
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

