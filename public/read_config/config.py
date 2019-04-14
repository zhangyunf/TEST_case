#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from public.util.config_operation import ConfigOperation

#配置文件路径
CONFIG_PATH = r"./config/config.ini"

class ReadConfig(ConfigOperation):

    # 获取配置文件中的信息
    def __init__(self):
        super(ReadConfig, self).__init__(CONFIG_PATH)

    @property
    def get_failure_color(self):
        # 获取案例执行失败时，cell中渲染的颜色
        failure_color = self.get_value("color", "failureColor")
        return failure_color

    @property
    def get_success_color(self):
        # 获取案例执行成功时，cell中渲染的颜色
        success_color = self.get_value("color", "successColor")
        return success_color

    @property
    def get_case_path(self):
        # 获取case.xlsx的文件路径
        case_path = self.get_value("path", "casePath")
        case_path = case_path.encode("gbk")
        case_path = case_path.decode("utf-8")
        return case_path

    @property
    def get_requests_path(self):
        # 获取请求数据配置文件路径
        requests_path = self.get_value("path", "requestsPath")

        return requests_path

    @property
    def get_requests_data_path(self):
        # 获取请求数据文件路径
        requests_data_path = self.get_value("path", "requestsDataPath")
        requests_data_path = requests_data_path.encode("gbk")
        requests_data_path = requests_data_path.decode("utf-8")
        return requests_data_path


if __name__ == "__main__":
    con = ReadConfig()
    a = con.get_case_path.encode("gbk")
    b = a.decode("utf-8")
    print(a, b)






