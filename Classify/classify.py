import cv2
import time
from config import ModelConfig, GlobalConfig
import os
import argparse


class Classify:
    def __init__(self, task, config_path):
        # 加载配置文件
        self.model_config = ModelConfig(config_path,model_name=task)
        self.global_config = GlobalConfig(config_path)

        # 打印 ROI 区域
        #ModelConfig.print_roi_regions(self.config)

        # 加载 ONNX 模型
        try:
            self.model_crucible_classify = cv2.dnn.readNetFromONNX(self.model_config.model_path)
            print("ONNX 模型加载成功:", self.model_config.model_path)
        except Exception as e:
            raise ValueError(f"加载 ONNX 模型失败: {e}")

        #分割区域次数
        self.times = 0

        #输出路径
        self.output_dir = self.global_config.output_dir
        print(f"图像保存路径:{self.global_config.output_dir}")


    # 预处理输入图像
    def preprocess_image(self, image):
        # 调整图像大小为模型输入大小
        resized_image = cv2.resize(image, (self.model_config.input_img_w, self.model_config.input_img_h))

        # 转换为模型输入格式 (1, C, H, W)
        blob_ = cv2.dnn.blobFromImage(resized_image, scalefactor=1 / 255, swapRB=True)

        #print("预处理后的输入形状:", blob_.shape)
        return blob_

    def ROI(self, image):
        # 初始化一个字典用于存储预处理后的图像
        preprocessed_images = {}

        # 遍历每个区域并裁剪保存
        for region_name, region_coords in self.model_config.roi_regions.items():
            # 提取区域坐标
            x_start = region_coords['start_x']
            y_start = region_coords['start_y']
            x_end = region_coords['end_x']
            y_end = region_coords['end_y']

            # 裁剪区域
            cropped_image = image[y_start:y_end, x_start:x_end]
            # 检查裁剪后的图像是否为空
            if cropped_image.size == 0:
                print(f"警告: 裁剪区域 {region_name} 为空。")
                continue  # 跳过空区域的处理

            # 保存裁剪后的图片
            if self.global_config.is_save_img is True:
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
            print("推理时间: {:.6f} 秒".format(e - s))

            # 处理输出结果
            result = self._classify_result(outputs_cl)
            results[region_name] = result


        # 返回结果
        return results


    # 分类逻辑  现在只有两个分类的情况，后续可以扩展
    def _classify_result(self, outputs_cl):
        if outputs_cl[0][0] > self.model_config.conf_classify and outputs_cl[0][0] - outputs_cl[0][1] > self.model_config.conf_classify / 2:
            out_is = 'Y'
        elif outputs_cl[0][1] > self.model_config.conf_classify and outputs_cl[0][1] - outputs_cl[0][0] > self.model_config.conf_classify / 2:
            out_is = 'N'
        else:
            out_is = 'Q'
        #print("-----------model_crucible_classify------------> ", out_is)
        return out_is




if __name__ == '__main__':
    #解析参数
    argparse = argparse.ArgumentParser("Classify")
    argparse.add_argument('--task', type=str, default='Re2000_top', help='任务名称')
    argparse.add_argument('--img', type=str, default=r'C:\Users\13053\OneDrive\Code\Classify\Image_20250410184107042.jpg', help='图片路径')
    argparse.add_argument('--config_path', type=str, default='classify.yaml', help='配置文件路径')
    args = argparse.parse_args()

    #主任务
    image = cv2.imread(args.img)
    print(f"任务：{args.task}")
    print("图像读取完成")
    # 初始化分类器
    classify = Classify(args.task, args.config_path)
    result = classify.predict(image)
    print("分类结果:", result)