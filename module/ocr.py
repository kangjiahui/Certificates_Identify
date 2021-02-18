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


def get_neighbor_box(lst, box, aim_pos, thresh):
    """
    From box location to find its neighbor, according to direction(FLAG) and distance(thresh).
    :param lst: list, return of get_all().
    :param box: list, e.x.[[1299.0, 480.0], [1448.0, 477.0], [1449.0, 514.0], [1300.0, 517.0]]
    :param aim_pos: str, in range of options: "RIGHT", "LEFT", "DOWN", "UP", "SAME"
    :param thresh: int, in mode "RIGHT", "LEFT", "DOWN" and "UP",
            thresh means how far the target could be away with keyword.
    :return: list, all lines matched. e.x.
    """
    result = [box]
    if aim_pos == "RIGHT":
        for line in lst:
            if 0 < abs(line[0][3][0] - box[0][2][0]) < thresh * 10 and 0 < abs(line[0][3][1] - box[0][2][1]) < thresh:
                result.append(line)
    elif aim_pos == "LEFT":
        for line in lst:
            if 0 < abs(line[0][2][0] - box[0][3][0]) < thresh * 10 and 0 < abs(line[0][2][1] - box[0][3][1]) < thresh:
                result.append(line)
    elif aim_pos == "DOWN":
        for line in lst:
            if 0 < abs(line[0][1][1] - box[0][2][1]) < thresh and \
                    0 < min(abs(line[0][2][0] - box[0][2][0]), abs(line[0][3][0] - box[0][3][0])) \
                    < abs(line[0][2][0] - line[0][3][0] - box[0][2][0] + box[0][3][0]) / 2:
                result.append(line)
    elif aim_pos == "UP":
        for line in lst:
            if 0 < abs(line[0][2][1] - box[0][1][1]) < thresh and \
                    0 < min(abs(line[0][2][0] - box[0][2][0]), abs(line[0][3][0] - box[0][3][0])) \
                    < abs(line[0][2][0] - line[0][3][0] - box[0][2][0] + box[0][3][0]) / 2:
                result.append(line)
    elif aim_pos == "SAME":
        pass
    # else:
    #     # TODO 定义FLAG输入错误的异常类
    #     raise Exception
    return result


class OCR(object):
    def __init__(self):
        self.model = PaddleOCR(use_angle_cls=True, lang="ch")

    def get_all(self, img):
        """
        Recognize all information from an image.
        :param img: numpy.ndarray
        :return: list, e.x.[[[[1319.0, 171.0], [1673.0, 173.0], [1673.0, 232.0], [1319.0, 230.0]], ('服务单位', 0.9971724)]
        , [[[333.0, 201.0], [414.0, 201.0], [414.0, 248.0], [333.0, 248.0]], ('姓名', 0.9986272)]]
        """
        result = self.model.ocr(img, cls=True)
        return result

    @staticmethod
    def get_location(keyword_regular, result):
        """
        Match the regular expression of keyword and give all locations for each matched keyword.
        :param result: list, return of get_all().
        :param keyword_regular: string, could be regular expression. e.x."姓名", "危险｜爆炸"
        :return: list, e.x.[[[[1299.0, 480.0], [1448.0, 477.0], [1449.0, 514.0], [1300.0, 517.0]], ('危险', 0.99250406)],
                        [[[1663.0, 480.0], [1886.0, 480.0], [1886.0, 510.0], [1663.0, 510.0]], ('爆炸', 0.8288886)]]
        """
        location = []
        for line in result:
            if re.search(keyword_regular, line[-1][0]):
                location.append(line)
        return location

    @staticmethod
    def get_info_by_location(result, info_regular, keyword_location, aim_pos, thresh=20):
        """
        Get information by keyword location.
        :param result: list, return of get_all().
        :param info_regular: the regular expression to match information.
        :param keyword_location: list, return from self.get_keywords_location()
                e.x.[[[1299.0, 480.0], [1448.0, 477.0], [1449.0, 514.0], [1300.0, 517.0]], ('危险', 0.99250406)]
        :param aim_pos: str, optional by following :["RIGHT", "LEFT", "DOWN", "UP", "SAME"]
                "RIGHT" means to find information in boxes at the right of keyword_location box.
                "LEFT", "DOWN", "UP" mean the same as "RIGHT".
                "SAME" means to find information in the same box as keyword_location.
        :param thresh: int, in mode "RIGHT", "LEFT", "DOWN" and "UP",
                thresh means how far the target could be away with keyword.
        :return: list, contains all matched info strings.
                e.x.[['鲁FBR932', [[305.0, 561.0], [457.0, 556.0], [458.0, 593.0], [307.0, 598.0]]],
                ['鲁GLN851挂', [[1663.0, 480.0], [1886.0, 480.0], [1886.0, 510.0], [1663.0, 510.0]]]]
        """
        print("info_regular is {}".format(info_regular))
        matched_info = []
        for box in keyword_location:
            print("keyword_location is {}".format(box))
            target = get_neighbor_box(result, box, aim_pos, thresh)
            print("target is {}".format(target))
            for t in target:
                info = re.search(info_regular, t[-1][0])
                if info:
                    matched_info.append(info.group(0))
        print(matched_info)
        return matched_info
