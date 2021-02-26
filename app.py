from flask import Flask, request, render_template
import module.utils.api as api
from flask_cors import CORS
import json
import yaml
from gevent import pywsgi
import base64

app = Flask(__name__)
CORS(app, resources=r'/*')

with open("confs/host.yaml", "r", encoding='UTF-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# 根据config文件重置空result字典
@app.route('/reset', methods=["POST"])
def reset():
    result = api.ocr_reset()
    return result


# 提取单张证件信息
@app.route('/ocr', methods=["POST"])
def ocr():
    if request.form['img_type'] == 'pic':
        input_data = request.files
        result = api.ocr_recog_one(base64.b64encode(input_data["user_image"].read()))
        return result
    else:
        return api.ocr_recog_one(request.form['user_image'])


# 现场人脸注册
@app.route('/register', methods=["POST"])
def register():
    if request.form['img_type'] == 'pic':
        input_data = request.files
        return api.face_register(base64.b64encode(input_data["user_image"].read()))
    else:
        return api.face_register(request.form['user_image'])


# 现场人脸核验
@app.route('/face', methods=["POST"])
def face():
    if request.form['img_type'] == 'pic':
        input_data = request.files
        return api.match_face_ocr(base64.b64encode(input_data["user_image"].read()))
    else:
        return api.match_face_ocr(request.form['user_image'])


# 现场车牌核验
@app.route('/car', methods=["POST"])
def car():
    if request.form['img_type'] == 'pic':
        input_data = request.files
        return api.car_plate_match(base64.b64encode(input_data["user_image"].read()))
    else:
        return api.car_plate_match(request.form['user_image'])


# 证件信息比对
@app.route('/match', methods=["POST"])
def match():
    result = api.info_match()
    return result


if __name__ == '__main__':
    server = pywsgi.WSGIServer((config["host"], config["port"]), app)
    server.serve_forever()
    # app.run(host='0.0.0.0', port=8100, debug=True)
    # app.run(host=config["host"], port=config["port"], debug=True, use_reloader=False)
