# -*- coding: utf-8 -*-
"""
   File Name：     api.py
   Description :  Instantiate OCR, FaceRecognition from ocr.py, faceRecognition.py. Give a clear API for user.
   Author :       KangJiaHui
   date：         2020/02/07
"""
import re
from datetime import datetime
import yaml
from module.ocr import OCR
import cv2

with open("../confs/config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ocr = OCR()

# TODO 查找阈值像素范围需要根据图像像素大小自适应


def reset(conf):
    """
    New a init dict according to yaml file, which decides the format of result.
    :param conf: dict, get from yaml file.
    :return: dict, e.x.{"特种设备使用登记证": None， "中华人民共和国道路运输证": None, "危险货物运输押运人员证": None,
                    "中华人民共和国机动车驾驶证": None, "中华人民共和国机动车行驶证": None, "道路危险货物运输驾驶员证": None}
    """
    init = {}
    for key in conf["证件"]:
        init[key] = None
    return init


def name_recog(lst, conf):
    """
    Recognize witch certificate it is, according to the OCR result of image.
    :param lst: list, the OCR result of input image.
    :param conf: dict, get from yaml file.
    :return: string, the key of matched certificate.
    """
    for key in conf["证件"]:
        regular = conf["证件"][key]["证件名"]
        if isinstance(regular, str):
            if ocr.get_location(regular, lst):
                return key
        elif isinstance(regular, list):
            location = ocr.get_location(regular[0], lst)
            if ocr.get_info_by_location(lst, regular[2], location, regular[1], 100):
                return key
    return None


def recog_one(image, conf, tmp_result):
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
    ocr_result = ocr.get_all(image)
    name = name_recog(ocr_result, conf)
    if not name:
        # TODO 此处需替换为 raise exception
        print("证件识别失败")
    result = {}
    for key in conf["证件"][name]:
        if key == "证件名":
            continue
        method = conf["证件"][name][key]
        loc = ocr.get_location(method[0], ocr_result)
        result[key] = ocr.get_info_by_location(ocr_result, method[2], loc, method[1], 20)
    tmp_result[name] = result
    return tmp_result


def result_filter(tmp_result):
    """
    Do something with the first vision of result, such as date transform, invalid string delete.
    :param tmp_result: dict, the result of recog_one()
    :return: dict, witch will be the final result.
    """
    for name, dic in tmp_result.items():
        if dic:
            for k, v in dic.items():
                if k == "日期" and v:
                    tmp_result[name][k] = []
                    for i in v:
                        if len(i.split("-")) == 3:
                            date = i.split("-")
                            today = datetime.today().strftime("%Y-%m-%d").split("-")
                            print("date is {}, today is {}".format(date, today))
                            if (str(date[0]) > str(today[0])) or \
                                    (str(date[0]) == str(today[0]) and str(date[1]) > str(today[1])) or \
                                    (str(date[0]) == str(today[0]) and str(date[1]) == str(today[1]) and
                                     str(date[2]) > str(today[2])):
                                tmp_result[name][k].append(i)
                        if len(re.split("[年月]", i)) == 3:
                            date = re.split("[年月]", i)[:2]
                            date_str = date[0] + "-" + date[1]
                            today = datetime.today().strftime("%Y-%m-%d").split("-")
                            if (str(date[0]) > str(today[0])) or \
                                    (str(date[0]) == str(today[0]) and str(date[1]) >= str(today[1])):
                                tmp_result[name][k].append(date_str)
                    v = tmp_result[name][k]
                if k == "姓名" and v:
                    v = tmp_result[name][k] = [i for i in v if i != "姓名"]
                if len(v) == 0:
                    tmp_result[name][k] = None
                if len(v) == 1:
                    tmp_result[name][k] = v[0]
    return tmp_result


if __name__ == '__main__':
    tmp = reset(config)
    while True:
        cwd = input("Please input an image file:")
        if cwd == 'q':
            result_filter(tmp)
            print(tmp)
            break
        img = cv2.imread(cwd)
        recog_one(img, config, tmp)
        print(tmp)
