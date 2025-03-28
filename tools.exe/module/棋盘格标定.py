#!/usr/bin/env python3
import cv2
import numpy as np
import glob

# 设置寻找亚像素角点的参数
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 棋盘格规格
w = 11  # 内部角点的列数
h = 8  # 内部角点的行数

# 生成棋盘格在世界坐标系中的三维点
objp = np.zeros((w * h, 3), np.float32)
objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2) * 20  # 每个格子的大小为 mm

# 储存棋盘格角点的世界坐标和图像坐标
objpoints = []
imgpoints = []

# 加载图像
images = glob.glob('./image/*.jpg')
print(f"Found {len(images)} images for calibration.")

for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print(f"Failed to load image: {fname}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (w, h), None)

    if ret:
        # 寻找亚像素角点
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners)

        # 可视化检测结果
        cv2.drawChessboardCorners(img, (w, h), corners, ret)
        cv2.imshow('findCorners', img)
        cv2.waitKey(200)
    else:
        print(f"Chessboard corners not found in image: {fname}")

cv2.destroyAllWindows()

# 标定
if objpoints and imgpoints:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    print("tools.exe successful.")
    print("Camera matrix:\n", mtx)
    print("Distortion coefficients:\n", dist)
else:
    print("No valid corners found, calibration failed.")