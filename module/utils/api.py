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
        "中华人民共和国道路运输证": {"有效期": "2021-04", "经营范围": null, "车牌": "鲁YZ666挂"},
        "道路危险货物运输驾驶员证": {"有效期": null, "姓名": "貂蝉"},
        "危险货物运输押运人员证": {"有效期": null, "姓名": "姜子牙", "身份证号": "23057219650517091X"},
        "中华人民共和国机动车驾驶证": {"有效期": "2022-01-04", "姓名": "杨戬"},
        "中华人民共和国机动车行驶证": {"有效期": "2821-07", "车牌": "鲁FBR888"}}}
    """
    try:
        result, pos = ocr.recog_one(image_base64)
        result_out = copy.deepcopy(result)
        for key, value in result_out.items():
            if value:
                result_out[key] = {k: v for k, v in value.items() if k != "人脸"}
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "pos": pos, "ocr": result_out}, ensure_ascii=False)
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def face_register(image_base64):
    """
    get face feature from certificate image, stored in ocr.face_feature
    :param image_base64: image encoded in base64
    :return: json, no new info return, just success or not.
    """
    try:
        ocr.face_register(image_base64)
        result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def match_face_ocr(image_base64):
    """
    Match face in input image with the faces in all certificates. Once a certificate matched, return True.
    :param image_base64: image encoded in base64
    :return:json:
        e.x. {"result": 0, "message": "SUCCESS", "flag": True}
    """
    try:
        flag = ocr.face_match(image_base64)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "flag": flag})
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def car_plate_match(image_base64):
    """
    Match car plate in input image with all car plates in certificates. Once a certificate matched, return True.
    :param image_base64: image encoded in base64
    :return: json
        e.x. {"result": 0, "message": "SUCCESS", "flag": True}
    """
    try:
        flag = ocr.car_plate_match(image_base64)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "flag": flag})
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json


def info_match():
    """
    Match information between two or more certificates according to config["匹配"]
    :return: dict, e.x. {"车牌": {"LNG车": True}, "姓名": {"驾驶员": True}, "人脸": {"驾驶员": True}}
    """
    try:
        result = ocr.info_match()
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "match": result}, ensure_ascii=False)
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json

