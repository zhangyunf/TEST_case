#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from public.util.config_operation import ConfigOperation
from public.read_config.config import ReadConfig

# 配置文件中请求配置的section名称
SECTION = "requests"

class ReadRequest(ConfigOperation):

    def __init__(self):
        self.readConfig = ReadConfig()
        super(ReadRequest, self).__init__(self.readConfig.get_requests_path)

    @property
    def get_url(self):
        '''获取网址'''
        return self.get_value(SECTION, "url")

    @property
    def get_secretKey(self):
        '''获取secrekey'''
        return self.get_value(SECTION, "secretKey")

    @property
    def get_token(self):
        '''获取token'''
        return self.get_value(SECTION, "token")



if __name__ == "__main__":
    con = ConfigOperation()
