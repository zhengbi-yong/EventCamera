import dv_processing as dv
import cv2 as cv
import numpy as np

# 打开指定的相机
left_capture = dv.io.CameraCapture(cameraName="DAVIS346_00001055")  # 左眼
right_capture = dv.io.CameraCapture(cameraName="DAVIS346_00001054")  # 右眼

# 检查相机是否成功启动
if not left_capture.isRunning() or not right_capture.isRunning():
    print("One or both cameras failed to start.")
    exit(1)

# 定义窗口名称和初始大小
window_name = "Stereo Preview"
initial_width, initial_height = 1600, 800

# 初始化可调整大小的预览窗口
cv.namedWindow(window_name, cv.WINDOW_NORMAL)
cv.resizeWindow(window_name, initial_width, initial_height)  # 设置窗口大小

# 运行循环，直到用户按下 'q' 键
while left_capture.isRunning() and right_capture.isRunning():
    # 从两个相机读取帧
    left_frame = left_capture.getNextFrame()
    right_frame = right_capture.getNextFrame()

    # 检查是否成功获取帧
    if left_frame is not None and right_frame is not None:
        # 打印接收的包时间范围
        print(f"Left eye frame at time [{left_frame.timestamp}], Right eye frame at time [{right_frame.timestamp}]")

        # 获取图像
        left_image = left_frame.image
        right_image = right_frame.image

        # 检查图像通道，如果是单通道，转换为三通道
        if len(left_image.shape) == 2:
            left_image = cv.cvtColor(left_image, cv.COLOR_GRAY2BGR)
        if len(right_image.shape) == 2:
            right_image = cv.cvtColor(right_image, cv.COLOR_GRAY2BGR)

        # 水平拼接图像（左图在左，右图在右）
        stereo_image = np.hstack((left_image, right_image))

        # 获取拼接后图像的尺寸
        stereo_height, stereo_width = stereo_image.shape[:2]

        # 计算缩放比例以适应预定义的窗口大小，同时保持纵横比
        scale = min(initial_width / stereo_width, initial_height / stereo_height)
        new_width = int(stereo_width * scale)
        new_height = int(stereo_height * scale)

        # 调整图像大小
        resized_stereo = cv.resize(stereo_image, (new_width, new_height), interpolation=cv.INTER_LINEAR)

        # 创建一个与窗口大小相同的黑色画布
        canvas = np.zeros((initial_height, initial_width, 3), dtype=np.uint8)

        # 计算图像在画布中的偏移量以居中显示
        x_offset = (initial_width - new_width) // 2
        y_offset = (initial_height - new_height) // 2

        # 将调整大小后的图像放置在画布上
        canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_stereo

        # 显示画布
        cv.imshow(window_name, canvas)

    # 检查退出条件
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Exit signal received. Exiting...")
        break

# 释放资源
left_capture.close()
right_capture.close()
cv.destroyAllWindows()
