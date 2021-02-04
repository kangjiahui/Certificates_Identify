# -*- coding: utf-8 -*-
"""
   File Name：     ocr.py
   Description :  wrapping for face recognition class, instantiation occurs in modules/face_server/utils/api.py
   Author :       KangJiaHui
   date：         2021/02/04
"""

import time
import cv2
import re
from paddleocr import PaddleOCR, draw_ocr


class OCR(object):
    def __init__(self):
        self.model = PaddleOCR(use_angle_cls=True, lang="ch")

    def get_all_results(self, img):
        """
        Recognize all infomations from an image.
        :param img: numpy.ndarray
        :return: list, e.x.[[[[1319.0, 171.0], [1673.0, 173.0], [1673.0, 232.0], [1319.0, 230.0]], ('服务单位', 0.9971724)]
        , [[[333.0, 201.0], [414.0, 201.0], [414.0, 248.0], [333.0, 248.0]], ('姓名', 0.9986272)]]
        """
        pass

    def get_keywords_location(self, keyword_list):
        """
        Match keywords in keyword_list, and give the location for each matched keyword.
        :param keyword_list: list, element could be regular expression. e.x.["姓名", "危险｜爆炸"]
        :return: dict, e.x.{"姓名": [[1319.0, 171.0], [1673.0, 173.0], [1673.0, 232.0], [1319.0, 230.0]],
        "危险": [[333.0, 201.0], [414.0, 201.0], [414.0, 248.0], [333.0, 248.0]}
        """
        pass

    def get_infomation_from_keyword_location(self, keyword_location):
        """
        Get information from keyword location.
        :param keyword_location: dict, return from self.get_keywords_location()
                e.x.{"姓名":[[1319.0, 171.0], [1673.0, 173.0], [1673.0, 232.0], [1319.0, 230.0]],
                    "危险":[[333.0, 201.0], [414.0, 201.0], [414.0, 248.0], [333.0, 248.0]}
        :return: dict, e.x.{"姓名": "康佳慧", "危险": True}
        """
        pass

