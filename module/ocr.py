# -*- coding: utf-8 -*-
"""
   File Name：     ocr.py
   Description :  wrapping for face recognition class, instantiation occurs in modules/face_server/utils/api.py
   Author :       KangJiaHui
   date：         2021/02/04
"""
import re
import os
import yaml
from datetime import datetime
from paddleocr import PaddleOCR
from module.utils.utils import base64_to_image
from module.utils.error import AimPose, NameRecFail
from module.face_recog.faceRecognition import FaceRecognition

face = FaceRecognition()


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
    else:
        raise AimPose
    return result


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


def get_info_by_location(result, info_regular, keyword_location, aim_pos, thresh=20):
    # TODO 查找阈值像素范围需要根据图像像素大小自适应
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
    matched_info = []
    for box in keyword_location:
        target = get_neighbor_box(result, box, aim_pos, thresh)
        for t in target:
            info = re.search(info_regular, t[-1][0])
            if info:
                matched_info.append(info.group(0))
    return matched_info


def filter_one(result):
    """
    Do something with the first vision of result, such as date transform, invalid string delete.
    :param result: dict, the result dict for one paper.
        e.x. {"有效期": ["2018年4月", "2021年4月"], "经营范围": ["危险化学品"], "车牌": ["鲁FBR932"]}
    :return: dict, the processed result dict for one paper.
        e.x. {"有效期": "2021-4", "经营范围": "危险化学品", "车牌": "鲁FBR932"}
    """
    for k, v in result.items():
        if k == "日期" and v:
            result[k] = []
            for i in v:
                if len(i.split("-")) == 3:
                    date = i.split("-")
                    today = datetime.today().strftime("%Y-%m-%d").split("-")
                    if (str(date[0]) > str(today[0])) or \
                            (str(date[0]) == str(today[0]) and str(date[1]) > str(today[1])) or \
                            (str(date[0]) == str(today[0]) and str(date[1]) == str(today[1]) and
                             str(date[2]) > str(today[2])):
                        result[k].append(i)
                if len(re.split("[年月]", i)) == 3:
                    date = re.split("[年月]", i)[:2]
                    date_str = date[0] + "-" + date[1]
                    today = datetime.today().strftime("%Y-%m-%d").split("-")
                    if (str(date[0]) > str(today[0])) or \
                            (str(date[0]) == str(today[0]) and str(date[1]) >= str(today[1])):
                        result[k].append(date_str)
            v = result[k]
        if k == "姓名" and v:
            v = result[k] = [i for i in v if i != "姓名"]
        if len(v) == 0:
            result[k] = None
        if len(v) == 1:
            result[k] = v[0]
    return result


class OCR(object):
    def __init__(self):
        self.model = PaddleOCR(use_angle_cls=True, lang="ch")
        with open(os.path.join(os.getcwd(), "confs/config.yaml"), "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
        self.tmp_result = {}
        self.reset()

    def reset(self):
        """
        New a init dict according to yaml file, which decides the format of result.
        :return: dict, e.x.{"特种设备使用登记证": None， "中华人民共和国道路运输证": None, "危险货物运输押运人员证": None,
                        "中华人民共和国机动车驾驶证": None, "中华人民共和国机动车行驶证": None, "道路危险货物运输驾驶员证": None}
        """
        for key in self.config["证件"]:
            self.tmp_result[key] = None
        return self.tmp_result

    def get_all(self, img):
        """
        Recognize all information from an image.
        :param img: numpy.ndarray
        :return: list, e.x.[[[[1319.0, 171.0], [1673.0, 173.0], [1673.0, 232.0], [1319.0, 230.0]], ('服务单位', 0.9971724)]
        , [[[333.0, 201.0], [414.0, 201.0], [414.0, 248.0], [333.0, 248.0]], ('姓名', 0.9986272)]]
        """
        result = self.model.ocr(img, cls=True)
        return result

    def name_recog(self, result):
        """
        Recognize witch certificate it is, according to the OCR result of image.
        :param result: list, the OCR result of input image.
        :return: string, the key of matched certificate.
        """
        for key in self.config["证件"]:
            regular = self.config["证件"][key]["证件名"]
            if isinstance(regular, str):
                if get_location(regular, result):
                    return key
            elif isinstance(regular, list):
                location = get_location(regular[0], result)
                if get_info_by_location(result, regular[2], location, regular[1], 100):
                    return key
        return None

    def recog_one(self, image_base64):
        """
        Recognize one image, and to update tmp_result dict
        :param tmp_result: e.x. {"特种设备使用登记证": {"发证日期": "2018年8月1日"}，"中华人民共和国道路运输证": None,
                                "危险货物运输押运人员证": None, "中华人民共和国机动车驾驶证": None,
                                "中华人民共和国机动车行驶证": None, "道路危险货物运输驾驶员证": None}
        :param image: numpy.ndarray, input image
        :param conf: dict, get from yaml file.
        :return: tmp_result: e.x. {"特种设备使用登记证": {"发证日期": "2018年8月1日"}，
                                "中华人民共和国道路运输证": {"有效期": None, "经营范围": "危险化学品", "车牌": "鲁FBR932"},
                                "危险货物运输押运人员证": None, "中华人民共和国机动车驾驶证": None,
                                "中华人民共和国机动车行驶证": None, "道路危险货物运输驾驶员证": None}
        """
        image = base64_to_image(image_base64)
        ocr_result = self.get_all(image)
        name = self.name_recog(ocr_result)
        if not name:
            raise NameRecFail
        result = {}
        if name in self.config["匹配"]["人脸"]:
            result["face"] = face.face_register(image_base64, 0.5)
        for key in self.config["证件"][name]:
            if key == "证件名":
                continue
            method = self.config["证件"][name][key]
            loc = get_location(method[0], ocr_result)
            result[key] = get_info_by_location(ocr_result, method[2], loc, method[1], 20)
        filter_one(result)
        self.tmp_result[name] = result
        return self.tmp_result
