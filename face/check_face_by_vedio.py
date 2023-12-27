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
        # cv.circle(resize_img, center=(x + w // 2, y + h // 2), radius=w // 3, color=(0, 255, 0), thickness=2)
    cv.imshow('result', resize_img)


cap = cv.VideoCapture(0)
while True:
    flag, frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord('q') == cv.waitKey(0):
        break

cv.destroyAllWindows()
cap.release()
