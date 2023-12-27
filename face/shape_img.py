# 修改图片尺寸

import cv2 as cv

img = cv.imread('gril.jpg')

print('原来的尺寸', img.shape)

resize_img = cv.resize(img, dsize=(600, 660))
print('现在的尺寸', resize_img.shape)

cv.imshow('resize_img', resize_img)
# cv.waitKey(0)
# 只有输入q到时候，退出
while True:
    code = cv.waitKey(0)
    if ord('q') == code:
        break
cv.destroyAllWindows()
