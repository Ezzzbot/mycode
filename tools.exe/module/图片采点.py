import cv2

# 鼠标回调函数
def mouse_callback(event, x, y, flags, param):
    """鼠标回调函数，在点击时显示坐标并打印到终端"""
    global img, base_img  # 使用全局变量
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        print(f"点击坐标: ({x}, {y})")
        # 恢复基础图像
        img = base_img.copy()
        # 绘制新的点和坐标
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)  # 绘制红色圆点
        cv2.putText(img, f"({x}, {y})", (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  # 显示坐标文字

if __name__ == "__main__":
    try:
        # 读取图像
        base_img = cv2.imread("image/test.jpg")  # 替换为你的图像路径
        if base_img is None:
            raise ValueError("图像读取失败，请检查路径！")

        img = base_img.copy()  # 保持一份原始图像

        # 创建窗口并设置鼠标回调
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Image", 960, 720)  # 调整显示窗口大小
        cv2.setMouseCallback("Image", mouse_callback)

        print("请点击图像查看像素坐标，按 ESC 键退出")

        while True:
            cv2.imshow("Image", img)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # 按 ESC 键退出
                break

        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error: {e}")
