import cv2 as cv

img = cv.imread('gril.jpg')
resize_img = cv.resize(img, dsize=(600, 650))
# 左上角的坐标 是（x,y） 矩阵的宽带和高度是（w,h）
x, y, w, h = 100, 100, 100, 100
# cv.rectangle(resize_img, (x, y), (x + w, y + h), color=(0, 255, 255), thickness=2)
x, y, r =320,220, 150
cv.circle(resize_img, center=(x,y), radius=r, color=(0, 0, 255), thickness=2)
cv.imshow('rectangle_img', resize_img)
cv.waitKey(0)
cv.destroyAllWindows()
