import yaml
import os

class GlobalConfig:
    def __init__(self, config_path):
        try:
            # 加载 YAML 配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            # 是否保存图片
            self.is_save_img = config.get('is_save_img')
            # 配置输出路径
            self.output_dir = config.get('output_dir')
            # 创建输出目录（如果不存在）
            os.makedirs(self.output_dir, exist_ok=True)
        except FileNotFoundError:
            raise FileNotFoundError(f"未找到配置文件 {config_path}，请检查文件路径！")  # 抛出异常
        except yaml.YAMLError as e:
            raise ValueError(f"解析 YAML 文件时出错: {e}")  # 抛出异常

class ModelConfig:
    def __init__(self, config_path, model_name):
        try:
            # 加载 YAML 配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            # 获取指定模型的配置
            model_config = config.get(model_name)
            if not model_config:
                raise ValueError(f"未找到模型 {model_name} 的配置，请检查 YAML 文件！")

            # 初始化模型参数
            self.model_path = model_config.get('model_path')
            self.image_path = model_config.get('image_path', None)  # 默认值为 None
            self.input_img_h = model_config.get('input_img_h')
            self.input_img_w = model_config.get('input_img_w')
            self.conf_classify = model_config.get('conf_classify')

            # 初始化 ROI 区域
            self.roi_regions = {}
            for region_name, region_config in model_config.items():
                if isinstance(region_config, dict) and all(key in region_config for key in ['start_x', 'start_y', 'end_x', 'end_y']):
                    self.roi_regions[region_name] = {
                        'start_x': region_config['start_x'],
                        'start_y': region_config['start_y'],
                        'end_x': region_config['end_x'],
                        'end_y': region_config['end_y']
                    }

        except FileNotFoundError:
            raise FileNotFoundError(f"未找到配置文件 {config_path}，请检查文件路径！")
        except yaml.YAMLError as e:
            raise ValueError(f"解析 YAML 文件时出错: {e}")

    def print_roi_regions(self):
        """打印所有 ROI 区域"""
        print("ROI 区域配置：")
        for region_name, region in self.roi_regions.items():
            #print(f"{region_name}: {region}")
            print(self.roi_regions)


# 使用示例
if __name__ == "__main__":
    config_path = './classify.yaml'  # YAML 配置文件路径
    model_name = "ganguo"           # 模型名称
    config = ModelConfig(config_path, model_name)

    # 打印加载的配置
    print("模型路径:", config.model_path)
    print("图像路径:", config.image_path)
    print("输入图像高度:", config.input_img_h)
    print("输入图像宽度:", config.input_img_w)
    print("分类置信度阈值:", config.conf_classify)

    # 打印 ROI 区域
    config.print_roi_regions()