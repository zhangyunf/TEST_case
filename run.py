#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ZhangYunFei

from main.run_case import RunCase


if __name__ == "__main__":
    runCase = RunCase()
    runCase.run_case()
    runCase.create_report()
