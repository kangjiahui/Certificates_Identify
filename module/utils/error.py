# -*- coding: utf-8 -*-
"""
   File Name：     error.py
   Description :  customized exception
   Author :       KangJiahui
   date：         2021/02/19
"""


class AimPose(Exception):
    def __init__(self):
        self.msg = "The aim pose flag is not exist! It should be 'RIGHT', 'LEFT', 'UP', 'DOWN' or 'SAME'."

    def __str__(self):
        return str(self.msg)


class NameRecFail(Exception):
    def __init__(self):
        self.msg = "Cannot identify the certificate name!"

    def __str__(self):
        return str(self.msg)


class FaceNum(Exception):
    def __init__(self):
        self.msg = "There must be one and only one face in the image!"

    def __str__(self):
        return str(self.msg)
