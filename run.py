#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from main.run_case import RunCase


if __name__ == "__main__":
    runCase = RunCase()
    runCase.run_case()
    dic = runCase.get_cases()
    print("通过案例数%d\n失败案例数%d\n执行时间%d\n" % (dic["success_cases"], dic["false_cases"], runCase.get_elapsed_time()))
    runCase.create_report()
