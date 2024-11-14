import cv2
import numpy as np

# 设置棋盘格的大小
chessboard_size = (9, 6)
square_size = 0.025  # 每个格子的大小，单位为米

# 准备棋盘格世界坐标
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
objp *= square_size

# 存储角点坐标
objpoints = []  # 世界坐标
imgpoints_left = []  # 左相机图像坐标
imgpoints_right = []  # 右相机图像坐标

# 读取图像对并检测角点
for i in range(num_images):
    img_left = cv2.imread(f'left_{i}.jpg')
    img_right = cv2.imread(f'right_{i}.jpg')
    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

    ret_left, corners_left = cv2.findChessboardCorners(gray_left, chessboard_size, None)
    ret_right, corners_right = cv2.findChessboardCorners(gray_right, chessboard_size, None)

    if ret_left and ret_right:
        objpoints.append(objp)
        imgpoints_left.append(corners_left)
        imgpoints_right.append(corners_right)

# 单目标定
_, mtx_left, dist_left, _, _ = cv2.calibrateCamera(objpoints, imgpoints_left, gray_left.shape[::-1], None, None)
_, mtx_right, dist_right, _, _ = cv2.calibrateCamera(objpoints, imgpoints_right, gray_right.shape[::-1], None, None)

# 双目标定
_, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objpoints, imgpoints_left, imgpoints_right, 
    mtx_left, dist_left, mtx_right, dist_right, 
    gray_left.shape[::-1], criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6), 
    flags=cv2.CALIB_FIX_INTRINSIC
)

# 校正
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mtx_left, dist_left, mtx_right, dist_right, gray_left.shape[::-1], R, T)

# 保存标定结果
np.savez('stereo_calib.npz', mtx_left=mtx_left, dist_left=dist_left, mtx_right=mtx_right, dist_right=dist_right, R=R, T=T, R1=R1, R2=R2, P1=P1, P2=P2, Q=Q)
