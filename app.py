from flask import Flask, request, render_template
import module.utils.api as api
from flask_cors import CORS
import json
import yaml
from gevent import pywsgi

app = Flask(__name__)
CORS(app, resources=r'/*')

with open("confs/host.yaml", "r", encoding='UTF-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# 根据config文件重置空result字典
@app.route('/reset', methods=["GET"])
def reset():
    result = api.ocr_reset()
    return result


# 提取单张证件信息
@app.route('/ocr', methods=["POST"])
def ocr():
    input_data = json.loads(request.data)
    image_base64 = input_data["image"]
    result = api.ocr_recog_one(image_base64)
    return result


# 现场人脸核验
@app.route('/face', methods=["POST"])
def face():
    input_data = json.loads(request.data)
    image_base64 = input_data["image"]
    result = api.match_face_ocr(image_base64)
    return result


# 证件信息比对
@app.route('/match', methods=["GET"])
def match():
    result = api.info_match()
    return result


if __name__ == '__main__':
    server = pywsgi.WSGIServer((config["host"], config["port"]), app)
    server.serve_forever()
    # app.run(host='0.0.0.0', port=8100, debug=True)
    # app.run(host=config["host"], port=config["port"], debug=True, use_reloader=False)
