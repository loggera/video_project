import cv2 as cv


def face_detect_demo(resize_img):
    gray = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)
    # 加载特征数据
    face_detector = cv.CascadeClassifier(
        'D:/opencv/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(gray)
    for x, y, w, h in faces:
        print(x, y, w, h)
        cv.rectangle(resize_img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
        cv.circle(img, center=(x + w // 2, y + h // 2), radius=w // 3, color=(0, 255, 0), thickness=2)
    cv.imshow('result', resize_img)


# 加载图片
img = cv.imread('small.jpg')
# 调用人脸检查方法
# resize_img = cv.resize(img, dsize=(600, 660))
#
face_detect_demo(img)
cv.waitKey(0)
cv.destroyAllWindows()
