# -*- coding: utf-8 -*-
"""
   File Name：     api.py
   Description :  Instantiate OCR, FaceRecognition from ocr.py, faceRecognition.py. Give a clear API for user.
   Author :       KangJiaHui
   date：         2020/02/07
"""

import json
from module.ocr import OCR
import copy
from module.utils.error import AimPose, NameRecFail

ocr = OCR()
print("OCR created!")


def ocr_reset():
    """
    Generate initial result.
    :return: json, no new info return, just success or not.
    """
    try:
        ocr.reset()
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def ocr_recog_one(image_base64):
    """
    Extract information from an image.
    :param image_base64: image encoded in base64
    :return: json,
        e.x. {"result": 0, "message": "SUCCESS", "ocr": {"特种设备使用登记证": {"发证日期": null},
        "中华人民共和国道路运输证": {"有效期": "2021-04", "经营范围": null, "车牌": "鲁YZ393挂"},
        "道路危险货物运输驾驶员证": {"有效期": null, "姓名": "安孔全"},
        "危险货物运输押运人员证": {"有效期": null, "姓名": "刘超", "身份证号": "23028119820318091X"},
        "中华人民共和国机动车驾驶证": {"有效期": "2022-01-04", "姓名": "方海桥"},
        "中华人民共和国机动车行驶证": {"有效期": "2821-07", "车牌": "鲁FBR932"}}}
    """
    try:
        result = ocr.recog_one(image_base64)
        result_out = copy.deepcopy(result)
        for key, value in result_out.items():
            if value:
                result_out[key] = {k: v for k, v in value.items() if k != "人脸"}
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "ocr": result_out}, ensure_ascii=False)
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def match_face_ocr(image_base64_1):
    """
    Match face in input image with the faces in all certificates. Once a certificate matched, return True.
    :param image_base64_1: image encoded in base64
    :return:json:
        e.x. {"result": 0, "message": "SUCCESS", "flag": True}
    """
    try:
        flag = ocr.face_match(image_base64_1)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "flag": flag})
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json

