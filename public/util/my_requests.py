#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

import json
import requests
from public.util.log import *
from public.util.combination_data import GetData


class RunMain(object):

    def send_get(self, url, headers=None, data=None):
        '''
        发送get请求
        :param url:请求的网址
        :param headers:headers默认为空
        :param data:请求的数据
        :return:请求响应体，如果请求失败则返回False
        '''
        try:
            res = requests.get(url=url, headers=headers, json=data)
        except Exception as error:
            log("GET:%s发送发成错误%s" % (url, error))
            return False
        else:
            log("GET:%s发送成功" % url)
            return res.text

    def send_post(self, url, data, headers=None):
        '''
        发送POST请求
        :param url: 请求的网址
        :param data: 上传的数据
        :param headers: headers默认为空
        :return: 请求响应体，如果请求失败则返回False
        '''
        try:

            res = requests.post(url, headers=headers, data=json.dumps(data))
        except Exception as error:
            log("POST:%s发送发生错误%s" % (url, error))
            return False
        else:
            log("POST:%s发送成功" % url)
            return res.text


    def run_main(self, url,method, data=None, headers=None):
        '''
        发送请求，根据method进行选择发送请求的方式
        :param method: 发送请求的方式(GET/POST)
        '''
        res = ""
        if method == 'GET':
            res = self.send_get(url, headers, data)
        elif method == 'POST':
            res = self.send_post(url, data, headers)
        try:
            return json.loads(res)
        except Exception as error:
            log("接受数据个数错误%s，数据为%s" % (error, res))
            return None





#test
if __name__ == '__main__':
    url = "http://192.168.55.105/v1/funds/"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzMwMzcxNDA2MjQxOTk2ODAwLCJwaCI6IiIsImVtIjoiMTAxQHEuY29tIiwiYyI6IiIsImRlIjoiV2luZG93cyAxMC9DaHJvbWU3My4wLjM2ODMuODYiLCJpcCI6IjE5Mi4xNjguMTEzLjIzMCIsIm9zIjozLCJpYXQiOjE1NTQwOTc3NDB9.q7rVokSG_CeEoxI1buwVvrl0WBJvTt_oHOilkXGnwq4"
    headers = {"Content-Type": "application/json", "token": token}
    data1 = {"a":"fundProductList","appId":0,"d":{"pageSize":10,"pageNo":1,"productId":0}}
    getdata = GetData(data1)
    da1 = getdata.combinationData()
    run = RunMain()
    re1 = run.run_main(url, "POST", da1, headers)
    print(re1)







