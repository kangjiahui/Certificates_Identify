import time
import cv2
from paddleocr import PaddleOCR, draw_ocr
import module.utils.api as api
from module.utils.utils import image_to_base64


def ocr_once():
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    img_path = 'test/12.png'
    img = cv2.imread(img_path)
    start = time.time()
    result = ocr.ocr(img, cls=True)
    print(result)
    print(time.time() - start)

    # 显示结果
    from PIL import Image
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('result/result12.jpg')


if __name__ == '__main__':
    api.ocr_reset()
    # t1 = time.time()
    api.ocr_recog_one(image_to_base64(cv2.imread("test/1.jpg")))
    api.ocr_recog_one(image_to_base64(cv2.imread("test/3.jpg")))
    api.ocr_recog_one(image_to_base64(cv2.imread("test/7.jpg")))
    api.ocr_recog_one(image_to_base64(cv2.imread("test/8.jpg")))
    api.ocr_recog_one(image_to_base64(cv2.imread("test/10.jpg")))
    result = api.ocr_recog_one(image_to_base64(cv2.imread("test/12.png")))
    print(result)
    # print(time.time() - t1)
    print(api.match_face_ocr(image_to_base64(cv2.imread("test/8.jpg"))))
    print(api.match_face_ocr(image_to_base64(cv2.imread("test/5.jpg"))))
    print(api.match_face_ocr(image_to_base64(cv2.imread("test/9.jpg"))))
