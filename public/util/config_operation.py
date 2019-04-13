#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

import configparser


class ConfigOperation(object):
    def __init__(self, file_name):
        self.conf = configparser.ConfigParser()
        self.conf.read(file_name)

    def get_value(self, section, option):
        '''获取数据'''
        return self.conf.get(section=section, option=option)



