# -*- coding: utf-8 -*-
"""
   File Name：     error.py
   Description :  customized exception
   Author :       KangJiahui
   date：         2021/01/28
"""


class RegisterFaceNum(Exception):
    def __init__(self):
        self.msg = "There must be one and only one face in the image!"

    def __str__(self):
        return str(self.msg)


class FaceArea(Exception):
    def __init__(self):
        self.msg = "Face area should occupy more proportion in the image!"

    def __str__(self):
        return str(self.msg)
