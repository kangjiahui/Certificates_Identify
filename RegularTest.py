#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

print(re.match('www', 'www.runoob.com.www').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))  # 不在起始位置匹配
print(re.search('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.search('com', 'com.www.runoob.com.com'))  # 不在起始位置匹配
print(re.findall('com', 'com.www.runoob.com.com'))  # 查找所有
# lst = ["^[1-9]\d{5}(18|19|20|(3\d))\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$", "^[1-9]\d{5}(18|19|20|(3\d))\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"]
# print(re.match(lst[0], "37292619710625005X"))

if re.search('wed', 'www.runoob.com'):
    print(1)
else:
    print(2)

import yaml
from module.ocr import *

with open("confs/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
print(config)