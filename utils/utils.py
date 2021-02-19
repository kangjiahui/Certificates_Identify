# -*- coding: utf-8 -*-
"""
   File Name：     tool.py
   Description :  convert between numpy.ndarray and base64
   Author :       kangjiahui
   date：         2020/09/08
"""
import base64
import cv2
import numpy as np
import hashlib
import json
import time
from functools import wraps


def image_to_base64(image_np):
    """
    Convert numpy.ndarray image into base64.
    :param image_np:
    :return: encoded base64 image
    """
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


def base64_to_image(base64_code):
    """
    Convert base64 into numpy.ndarray image.
    :param base64_code: encoded base64 image
    :return: decoded numpy.ndarray image
    """
    # base64 decode
    img_data = base64.b64decode(base64_code)
    # convert into numpy
    img_array = np.fromstring(img_data, np.uint8)
    # convert into cv image
    img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img

