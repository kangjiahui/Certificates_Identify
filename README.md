# 证件识别
本工程的图像文字检测识别深度学习模型使用paddleocr。

代码定义了一种基于paddleocr识别结果，提取证件信息的通用逻辑。针对不同证件，通过修改配置文件 confs/certificate.yaml 进行设定。

##环境安装：
安装cmake  
pip install paddlepaddle==2.0.0rc1 -i https://mirror.baidu.com/pypi/simple  
pip install paddleocr==2.0.2 -i https://mirror.baidu.com/pypi/simple  
pip install dlib  
pip install flask  
pip install flask_cors  
pip install gevent  
pip install opencv-python

##返回值示例：
curl localhost:8100/reset:  
{"result": 0, "message": "SUCCESS"}

curl -H "Content-Type:application/json" -H "Data_Type:msg" -X POST -d@certificate_image_1.json localhost:8100/ocr   
{"result": 0, "message": "SUCCESS", "ocr": {"特种设备使用登记证": null, "中华人民共和国道路运输证": null, "道路危险货物运输驾驶员证": null, : "刘超", "身份证号": "23028119820318091X"}, "中华人民共和国机动车驾驶证": null, "中华人民共和国机动车行驶证": null}}

curl -H "Content-Type:application/json" -H "Data_Type:msg" -X POST -d@face_image_1.json localhost:8100/face:  
{"result": 0, "message": "SUCCESS", "flag": false}

curl localhost:8100/match:  
{"result": 0, "message": "SUCCESS", "match": {"车牌": {"LNG车": false}, "姓名": {"驾驶员": false}, "人脸": {"驾驶员": false}}}

##module.utils.api接口文档:

NAME
    module.utils.api

DESCRIPTION
    File Name：     api.py
    Description :  Instantiate OCR, FaceRecognition from ocr.py, faceRecognition.py. Give a clear API for user.
    Author :       KangJiaHui
    date：         2020/02/07

FUNCTIONS

    info_match()
        Match information between two or more certificates according to config["匹配"]
        :return: dict, e.x. {"车牌": {"LNG车": True}, "姓名": {"驾驶员": True}, "人脸": {"驾驶员": True}}
    
    match_face_ocr(image_base64_1)
        Match face in input image with the faces in all certificates. Once a certificate matched, return True.
        :param image_base64_1: image encoded in base64
        :return:json:
            e.x. {"result": 0, "message": "SUCCESS", "flag": True}
    
    ocr_recog_one(image_base64)
        Extract information from an image.
        :param image_base64: image encoded in base64
        :return: json,
            e.x. {"result": 0, "message": "SUCCESS", "ocr": {"特种设备使用登记证": {"发证日期": null},
            "中华人民共和国道路运输证": {"有效期": "2021-04", "经营范围": null, "车牌": "鲁YZ393挂"},
            "道路危险货物运输驾驶员证": {"有效期": null, "姓名": "安孔全"},
            "危险货物运输押运人员证": {"有效期": null, "姓名": "刘超", "身份证号": "23028119820318091X"},
            "中华人民共和国机动车驾驶证": {"有效期": "2022-01-04", "姓名": "方海桥"},
            "中华人民共和国机动车行驶证": {"有效期": "2821-07", "车牌": "鲁FBR932"}}}
    
    ocr_reset()
        Generate initial result.
        :return: json, no new info return, just success or not.

DATA
    ocr = <module.ocr.OCR object>

FILE
    /Users/kjh/OCR/OCRServer/module/utils/api.py
