import numpy as np
import cv2
import time
import yaml
from config import ModelConfig
import os


class Classify:
    def __init__(self, task):
        # 加载配置文件
        self.config = ModelConfig(config_path='classify.yaml',model_name=task)

        # 打印 ROI 区域
        #ModelConfig.print_roi_regions(self.config)

        # 加载 ONNX 模型
        self.model_crucible_classify = cv2.dnn.readNetFromONNX(self.config.model_path)

        #分割区域次数
        self.times = 0

        #输出路径
        self.output_dir = './images'
        os.makedirs(self.output_dir, exist_ok=True)


    # 预处理输入图像
    def preprocess_image(self, image):
        # 调整图像大小为模型输入大小
        resized_image = cv2.resize(image, (self.config.input_img_w, self.config.input_img_h))

        # 转换为模型输入格式 (1, C, H, W)
        blob_ = cv2.dnn.blobFromImage(resized_image, scalefactor=1 / 255, swapRB=True)

        #print("预处理后的输入形状:", blob_.shape)
        return blob_
    # 裁剪区域
    def ROI(self, image):
        # 初始化一个字典用于存储预处理后的图像
        preprocessed_images = {}

        # 遍历每个区域并裁剪保存
        for region_name, region_coords in self.config.roi_regions.items():
            # 提取区域坐标
            x_start = region_coords['start_x']
            y_start = region_coords['start_y']
            x_end = region_coords['end_x']
            y_end = region_coords['end_y']

            # 裁剪区域
            cropped_image = image[y_start:y_end, x_start:x_end]

            # 保存裁剪后的图片
            output_path = os.path.join(self.output_dir, f"cropped_{region_name}.jpg")
            cv2.imwrite(output_path, cropped_image)

            image_pre = self.preprocess_image(cropped_image)

            # 将预处理后的图像存储到字典中
            preprocessed_images[region_name] = image_pre

            self.times = self.times + 1

        print("图像处理完成！")
        return preprocessed_images
    # 运行模型预测，如果不需要裁剪区域，直接预处理即可
    def predict(self, image):
        if image is None:  # 检查图像是否成功读取,错误为0
            raise ValueError(f"无法读取图像")
        # 存储每个区域的预测结果
        results = {}
        #图像预处理
        preprocessed_images = self.ROI(image)
        # 遍历每个区域的预处理图像
        for region_name, image_pre in preprocessed_images.items():
            # 设置模型输入
            self.model_crucible_classify.setInput(image_pre)
            # 运行模型预测
            s = time.time()
            outputs_cl = self.model_crucible_classify.forward()
            e = time.time()
            print("模型类别概率: [{:.6f}, {:.6f}]".format(outputs_cl[0][0], outputs_cl[0][1]))
            #print("推理时间: {:.6f} 秒".format(e - s)

            # 处理输出结果
            result = self._classify_result(outputs_cl)
            results[region_name] = result


        # 返回结果
        return results


    # 分类逻辑  现在只有两个分类的情况，后续可以扩展
    def _classify_result(self, outputs_cl):
        if outputs_cl[0][0] > self.config.conf_classify and outputs_cl[0][0] - outputs_cl[0][1] > self.config.conf_classify / 2:
            out_is = 'p'
        elif outputs_cl[0][1] > self.config.conf_classify and outputs_cl[0][1] - outputs_cl[0][0] > self.config.conf_classify / 2:
            out_is = 'n'
        else:
            out_is = 'q'
        #print("-----------model_crucible_classify------------> ", out_is)
        return out_is




if __name__ == '__main__':

    task = 'ganguo'
    image = cv2.imread('Image_20250327100352268.jpg')

    # 初始化分类器
    classify = Classify(task)
    result = classify.predict(image)
    print("分类结果:", result)