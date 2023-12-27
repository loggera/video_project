import cv2

import mediapipe as mp
import time
import loguru

lg = loguru.logger
# 调用摄像头
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    hands_result = results.multi_hand_landmarks
    if hands_result:
        for handLms in hands_result:
            num_points = len(handLms.landmark)
            lg.info(f'{"num_points":} = {num_points}')
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # if id == 0:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            if num_points == 2:
                # 在图像上添加“拍照”文字
                cv2.putText(img, "拍照", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                # 拍照并保存图像
                cv2.imwrite("photo.jpg", img)
                break  # 如果已经拍了一张照片，就跳出循环，以便不重复保存同一张照片

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
    # if ord('q') == cv2.waitKey(0):
    #     break
# cv2.destroyAllWindows()
# cap.release()


# import cv2
# import mediapipe as mp
# import time
#
# # 调用摄像头
# cap = cv2.VideoCapture(0)
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils
# pTime = 0
# cTime = 0
#
# while True:
#     success, img = cap.read()
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#     hands_result = results.multi_hand_landmarks
#     if hands_result:
#         for handLms in hands_result:
#             if len(handLms) >= 2:  # 如果检测到两个或以上的手指
#                 for id, lm in enumerate(handLms.landmark):
#                     h, w, c = img.shape
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
#                 mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
#                 # 在图像上添加“拍照”文字
#                 cv2.putText(img, "拍照", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
#                 # 拍照并保存图像
#                 cv2.imwrite("photo.jpg", img)
#                 break  # 如果已经拍了一张照片，就跳出循环，以便不重复保存同一张照片
#             else:
#                 mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
#     cv2.imshow('Image', img)
#     cv2.waitKey(1)
#     # if ord('q') == cv2.waitKey(0):
#     #     break
# # cv2.destroyAllWindows()
# # cap.release()
