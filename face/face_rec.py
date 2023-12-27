# 人脸检测

import cv2 as cv


def face_detect_demo(resize_img):
    gray = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
    # 加载特征数据
    face_detector = cv.CascadeClassifier(
        'D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(gray)
    for x, y, w, h in faces:
        cv.rectangle(resize_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

    cv.imshow('result', resize_img)


img = cv.imread('gril.jpg')
# resize_img = cv.resize(img, dsize=(600, 660))
#
face_detect_demo(img)
cv.waitKey(0)
cv.destroyAllWindows()
