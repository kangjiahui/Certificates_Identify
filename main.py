import time
import cv2
import re
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
img_path = 'test/2.jpg'
img = cv2.imread(img_path)
start = time.time()
result = ocr.ocr(img, cls=True)
print(result)
print(time.time() - start)
res = {}
for line in result:
    print(line)
    # 识别车牌
    match_car = re.search('^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z][A-Z][A-Z0-9]{4}[A-Z0-9挂学警港澳]$',
                      line[-1][0])
    if match_car:
        res["车牌"] = [match_car.group(), line[0]]
    # 识别身份证
    match_id = re.search("^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$",
                         line[-1][0])
    if match_id:
        print(match_id.group())
        res["身份证"] = [match_id.group(), line[0]]
    # 识别姓名关键字
    match_key = re.search("姓名", line[-1][0])
    match_name = re.search("^[\u4E00-\u9FA5]{2,4}$", line[-1][0])
    if match_key:
        res["姓名"] = [match_key.group(), line[0]]
print(res)

# 显示结果
from PIL import Image
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result8.jpg')
