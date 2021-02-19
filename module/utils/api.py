# -*- coding: utf-8 -*-
"""
   File Name：     api.py
   Description :  Instantiate OCR, FaceRecognition from ocr.py, faceRecognition.py. Give a clear API for user.
   Author :       KangJiaHui
   date：         2020/02/07
"""

import json
from module.ocr import OCR
from module.face_recog.faceRecognition import FaceRecognition
from module.utils.error import AimPose, NameRecFail

ocr = OCR()
print("OCR created!")
face = FaceRecognition()
print("FaceRcognition created!")


def ocr_reset():
    # try:
    ocr.reset()
    #     result_json = json.dumps({"result": 0, "message": "SUCCESS"})
    # except Exception as e:
    #     msg = str(e)
    #     result_json = json.dumps({"result": -1, "message": msg})
    # return result_json


def ocr_recog_one(image_base64):
    # try:
    #     result = ocr.recog_one(image)
    #     result_json = json.dumps({"result": 0, "message": "SUCCESS", "ocr": result}, ensure_ascii=False)
    # except Exception as e:
    #     msg = str(e)
    #     result_json = json.dumps({"result": -1, "message": msg})
    # return result_json
    return ocr.recog_one(image_base64)


def match_face(thresh, score_rec, image_base64_1, image_base64_2):
    """
    Match the input feature vector and vector for each face in one image.
    Once a face matched, it will return True.
    If path and image coexist, then path will cover image.
    :param image_base64_2: image encoded in base64
    :param image_base64_1: image encoded in base64
    :param score_rec: float, the score of detected faces should be larger than score_rec
    :param thresh: distance between face and matched face should be smaller than thresh
    :return:json:
        e.x. {"result": 0, "message": "SUCCESS", "flag": True}
    """
    try:
        flag = face.match_identity(thresh, score_rec, image_base64_1, image_base64_2)
        result_json = json.dumps({"result": 0, "message": "SUCCESS", "flag": flag})
    except Exception as e:
        msg = str(e)
        result_json = json.dumps({"result": -1, "message": msg})
    return result_json

