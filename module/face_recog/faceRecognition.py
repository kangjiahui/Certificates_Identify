# -*- coding: utf-8 -*-
"""
   File Name：     faceRecognition.py
   Description :  wrapping for face recognition class, instantiation occurs in modules/face_server/utils/api.py
   Author :       KangJiaHui
   date：         2020/01/14
"""

import dlib
import cv2
import numpy as np
import os
import urllib.request
from module.utils.utils import base64_to_image
from module.utils.error import FaceNum


def calculate_distance(vector1, vector2):
    """
    Calculates Euclidean distance between two vectors.
    :param vector1:vector presents a face feature
    :param vector2:vector presents a face feature
    :return:disance:the Euclidean distance between vector1 and vector2.
    """
    temp = vector1 - vector2
    distance = np.linalg.norm(temp)
    return distance


def download_from_url(filepath, save_dir):
    """
    download file from URL
    :param filepath: str, URL
    :param save_dir: str, save path without filename
    :return: None
    """
    print('\nDownloading file from {}'.format(filepath))
    filename = filepath.split('/')[-1]
    save_path = os.path.join(save_dir, filename)
    urllib.request.urlretrieve(filepath, save_path)
    print('\nSuccessfully downloaded to {}'.format(save_path))


def resize(image):
    if image.shape[0] > 1000 or image.shape[1] > 1000:
        if image.shape[0] > image.shape[1]:
            proportion = 1000 / image.shape[0]
        else:
            proportion = 1000 / image.shape[1]
        image = cv2.resize(image, None, fx=proportion, fy=proportion, interpolation=cv2.INTER_AREA)
    return image


class FaceRecognition(object):
    def __init__(self):
        self.predictor_path = os.path.join(os.getcwd(), 'module/face_recog/params',
                                           'shape_predictor_68_face_landmarks.dat')
        self.face_rec_model_path = os.path.join(os.getcwd(), 'module/face_recog/params',
                                                'dlib_face_recognition_resnet_model_v1.dat')
        if not os.path.exists('module/face_recog/params'):
            os.makedirs('module/face_recog/params')
        if not os.path.exists(self.predictor_path):
            download_from_url("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2",
                              os.path.join(os.getcwd(), 'module/face_recog/params'))
            os.system('bzip2 -d module/face_recog/params/shape_predictor_68_face_landmarks.dat.bz2')
        if not os.path.exists(self.face_rec_model_path):
            download_from_url("http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2",
                              os.path.join(os.getcwd(), 'module/face_recog/params'))
            os.system('bzip2 -d module/face_recog/params/dlib_face_recognition_resnet_model_v1.dat.bz2')
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)

    def face_register(self, image_base64, score_reg):
        """
        Registers only one face in one picture.
        :param score_reg: float, the score of the face to be registered should be larger than score_reg
        :param image_base64: image encoded in base64
        :return: list: the feature vector of the face in input image
        """
        image = base64_to_image(image_base64)
        # print(image.shape[0], image.shape[1])
        if image.shape[0] > 1000 or image.shape[1] > 1000:
            if image.shape[0] > image.shape[1]:
                proportion = 1000 / image.shape[0]
            else:
                proportion = 1000 / image.shape[1]
            image = cv2.resize(image, None, fx=proportion, fy=proportion, interpolation=cv2.INTER_AREA)
        faces, scores, idx = self.detector.run(image, 1, score_reg)
        if len(faces) != 1:
            raise FaceNum
        shape = self.sp(image, faces[0])
        face_chip = dlib.get_face_chip(image, shape)
        feature_vector = list(self.facerec.compute_face_descriptor(face_chip))
        return feature_vector

    def match_two_images(self, thresh, score_rec, image_base64_1, image_base64_2):
        """
        Match face in two images.
        Once a face matched, it will return True.
        :param image_base64_1: image encoded in base64
        :param image_base64_2: image encoded in base64
        :param score_rec: float, the score of detected faces should be larger than score_rec
        :param thresh: distance between face and matched face should be smaller than thresh
        :return:bool: True means face matched, False means face not matched.
        """
        image_1 = resize(base64_to_image(image_base64_1))
        image_2 = resize(base64_to_image(image_base64_2))
        faces_1, scores_1, idx_1 = self.detector.run(image_1, 1, score_rec)
        faces_2, scores_2, idx_2 = self.detector.run(image_2, 1, score_rec)
        if len(faces_1) != 1 or len(faces_2) != 1:
            raise FaceNum
        shape_1 = self.sp(image_1, faces_1[0])
        face_chip_1 = dlib.get_face_chip(image_1, shape_1)
        face_descriptor_1 = np.array(self.facerec.compute_face_descriptor(face_chip_1))
        shape_2 = self.sp(image_2, faces_2[0])
        face_chip_2 = dlib.get_face_chip(image_2, shape_2)
        face_descriptor_2 = np.array(self.facerec.compute_face_descriptor(face_chip_2))
        distance = calculate_distance(face_descriptor_1, face_descriptor_2)
        if distance < thresh:
            return True  # True means face matched
        return False  # False means face not matched

    @staticmethod
    def match_two_features(thresh, feature_1, feature_2):
        """
        Match two face features.
        :param thresh: float, distance between face and matched face should be smaller than thresh
        :param feature_1: vector presents a face feature
        :param feature_2: vector presents a face feature
        :return: bool, True means face matched, False means face not matched.
        """
        distance = calculate_distance(feature_1, feature_2)
        if distance < thresh:
            return True  # True means face matched
        return False  # False means face not matched

    def match_identity(self, feature_vector, thresh, score_rec, image_base64):
        """
        Match the input feature vector and vector for each face in one image.
        Once a face matched, it will return True.
        :param score_rec: float, the score of detected faces should be larger than score_rec
        :param feature_vector: list, the feature vector to be matched
        :param thresh: distance between face and matched face should be smaller than thresh
        :param image_base64: image encoded in base64
        :return: bool, True means face matched, False means face not matched.
        """
        image = resize(base64_to_image(image_base64))
        faces, scores, idx = self.detector.run(image, 1, score_rec)
        for face in faces:
            shape = self.sp(image, face)
            face_chip = dlib.get_face_chip(image, shape)
            face_descriptor = np.array(self.facerec.compute_face_descriptor(face_chip))
            distance = calculate_distance(face_descriptor, np.array(feature_vector))
            # print(distance)
            if distance < thresh:
                return True  # True means face matched
        return False  # False means face not matched

    def match_in_ocr(self, ocr_result, image_base64):
        """
        Match face in input image with the faces in all certificates. Once a certificate matched, return True.
        :param ocr_result: dict, the result of all certificates' extracted information.
        :param image_base64: image encoded in base64
        :return: bool, True means face matched, False means face not matched.
        """
        for key, value in ocr_result.items():
            if "人脸" in value.keys():
                if self.match_identity(value["人脸"], 0.5, 0.5, image_base64):
                    return True
        return False



