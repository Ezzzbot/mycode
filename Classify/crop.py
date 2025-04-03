"""
    crop.py
    用于分割图片指定区域并保存
    author: tlq 2025.4.1
"""




import numpy as np
import cv2
import time
import yaml
from config import ModelConfig

import os, datetime


class Crop:
    def __init__(self, task):
        # 加载配置文件
        self.model_config = ModelConfig(config_path=r'C:\Users\13053\OneDrive\Code\Classify\classify.yaml', model_name=task)
        # 打印 ROI 区域
        # ModelConfig.print_roi_regions(self.config)

        # 分割区域次数
        self.times = 0

        # 输出路径
        self.output_dir = r'C:\Users\13053\OneDrive\Code\Classify\crop_image'
        print(f"图像保存路径:{self.output_dir}")



    # 裁剪区域
    def ROI(self, image):
        # print("image ", image.shape)
        # 初始化一个字典用于存储预处理后的图像
        preprocessed_images = {}

        # 遍历每个区域并裁剪保存
        for region_name, region_coords in self.model_config.roi_regions.items():
            # 提取区域坐标
            x_start = region_coords['start_x']
            y_start = region_coords['start_y']
            x_end = region_coords['end_x']
            y_end = region_coords['end_y']

            # print("x_start ", x_start, x_end, y_start, y_end)
            # 裁剪区域
            cropped_image = image[y_start:y_end, x_start:x_end]

            # 保存裁剪后的图片

            filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            img_filename = '{}-{}.jpg'.format(filename, region_name)

            output_path = os.path.join(self.output_dir, img_filename)  # f"cropped_{region_name}.jpg")
            cv2.imwrite(output_path, cropped_image)
            # print("cropped_image ", cropped_image.shape)

            self.times = self.times + 1

        print("图像处理完成！")
        return 'ok'


if __name__ == '__main__':

    task = 'fangzhi'
    # 初始化 Crop 类
    crop = Crop(task)

    # 定义图片所在的文件夹路径
    folder_path = r'C:\Users\13053\OneDrive\Code\Classify\danjia_images'

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为图片（可以根据需要扩展支持的格式）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # 构造完整的图片路径
            image_path = os.path.join(folder_path, filename)

            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                print(f"无法读取图片: {image_path}")
                continue

            # 对图片进行 crop 处理
            result = crop.ROI(image)
