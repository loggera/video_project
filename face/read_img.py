import cv2 as cv

# 读取图片
img = cv.imread('gril.jpg')
# 显示图片
cv.imshow('read_img', img)

# 等待键盘输入  单位毫秒 传入0就是无限等待

cv.waitKey(3000)
# 释放内存

cv.destroyAllWindows()
