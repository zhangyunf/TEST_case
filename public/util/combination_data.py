#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

import collections
import datetime
import time
import hashlib
from urllib import parse
from public.read_config.request_config_read import ReadRequest

class GetData(object):

    def __init__(self, data, token):
        self.data = data
        self.token = token

    def _flatten_dict(self, d, new_dic=None):
        """
        遍历data中的a、b，并重新组成字典
        :param d:
        :param new_dic:
        :return:
        """
        if new_dic is None:
            new_dic = dict()
        for k, v in d.items():
            if isinstance(v, list):
                continue
            if isinstance(v, dict):
                self._flatten_dict(v, new_dic)
            else:
                new_dic[k] = v
        return new_dic

    def flatten_dict(self, dic):
        """
        字典按字母大小排序并转码
        :param dic:
        :return:
        """
        od = collections.OrderedDict()
        for k, v in sorted(self._flatten_dict(dic).items(), key=lambda x: x[0]):
            if v != "":
                od[k] = v
        res = parse.urlencode(od)
        return res

    def create_sig(self, s):
        """
        创建sig
        :param s:
        :return:
        """
        sha256 = hashlib.sha256()
        md5_inner = hashlib.md5()
        md5_outer = hashlib.md5()
        md5_inner.update(s.encode('utf-8'))
        md5_outer.update(md5_inner.hexdigest().encode('utf-8'))
        sha256.update(md5_outer.hexdigest().encode('utf-8'))
        res = sha256.hexdigest().lower()
        return res

    def combination_data(self):
        '''
        :param sig:
        :return:read_config
        '''
        self.data.update({"token": self.token})
        readR = ReadRequest()
        timestamp = int(time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')))
        self.data.update({"ts": timestamp})
        sig = '{}{}'.format(self.flatten_dict(self.data), readR.get_secretKey)
        sig = self.create_sig(sig)
        self.data.pop("token")
        self.data.update({"sig": sig})
        return self.data

#test
if __name__ == "__main__":
    # pass
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mjg2OTM5MjQyOTQ3NDIwMTYwLCJwaCI6IiIsImVtIjoiMjQ1MTI0MDg1QHFxLmNvbSIsImMiOiIiLCJkZSI6IldpbmRvd3MgMTAvQ2hyb21lNzAuMC4zNTM4LjExMCIsImlwIjoiMTkyLjE2OC44LjE4MiIsIm9zIjozLCJhdWQiOiJzdG9jayIsImlhdCI6MTU0MzMwODg1OX0.4ndRGTf4XI52i8vqQFfKFSUKx6sr0HJWSwip1WHlIyI"
    data = {
        "a": "fp",
        "appId": 0,
        "d": {"id": 0},
        "token": token}
    getdata = GetData(data, token)
    data = getdata.combination_data()
    print(data)
