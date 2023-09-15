import cv2

def capture_video():
    # 创建视频捕捉对象
    cap = cv2.VideoCapture(0)  # 0表示默认摄像头，如果有多个摄像头可以尝试不同的索引值

    while True:
        # 读取一帧图像
        ret, frame = cap.read()

        # 显示图像
        cv2.imshow('Video', frame)

        # 按下 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

# 调用函数开始捕捉视频
capture_video()
