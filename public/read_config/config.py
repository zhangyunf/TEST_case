#-*- endcoding:utf-8 -*-
from public.util.config_operation import configOperation
file_name = r"./config/config.ini"

class readConfig(configOperation):

    def __init__(self):
        super(readConfig, self).__init__(file_name)

    @property
    def get_failureColor(self):
        failureColor = self.get_value("color", "failureColor")
        return failureColor

    @property
    def get_successColor(self):
        successColor = self.get_value("color", "successColor")
        return successColor

    @property
    def get_casePath(self):
        casePath = self.get_value("path", "casePath")
        casePath = casePath.encode("gbk")
        casePath = casePath.decode("utf-8")
        return casePath

    @property
    def get_requestsPath(self):
        requestsPath = self.get_value("path", "requestsPath")

        return requestsPath

    @property
    def get_requestsDataPath(self):
        requestsDataPath =  self.get_value("path", "requestsDataPath")
        requestsDataPath = requestsDataPath.encode("gbk")
        requestsDataPath = requestsDataPath.decode("utf-8")
        return requestsDataPath


if __name__ == "__main__":
    con = readConfig()
    a = con.get_casePath.encode("gbk")
    b = a.decode("utf-8")
    print(a, b)






