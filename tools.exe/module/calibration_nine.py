import cv2
import numpy as np
import yaml


def convert_matrix(pixel_coords, robot_coords):
    # 计算映射矩阵
    matrix, _ = cv2.estimateAffine2D(pixel_coords, robot_coords)
    return matrix


def transform_pixel_to_robot(matrix, pixel_point):
    transformed_point = cv2.transform(np.array([pixel_point], dtype=np.float32).reshape(1, -1, 2), matrix)
    return transformed_point.flatten()


def matrix_calculate(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # 从YAML文件中获取像素坐标和机器人坐标
    pixel_coords = np.array(config['pixel_coords'], dtype=np.float32)
    robot_coords = np.array(config['robots_coords'], dtype=np.float32)

    # 计算映射矩阵
    matrix = convert_matrix(pixel_coords, robot_coords)

    # 计算误差
    errors = []
    for i in range(len(pixel_coords)):
        pixel_point = pixel_coords[i]
        robot_point = robot_coords[i]
        # 使用映射矩阵转换像素坐标到机器人坐标
        transformed_point = transform_pixel_to_robot(matrix, pixel_point)
        # 计算误差
        error_x = robot_point[0] - transformed_point[0]
        error_y = robot_point[1] - transformed_point[1]
        errors.append([error_x, error_y])

    # 将 numpy 数据类型转换为 Python 原生类型
    matrix = matrix.tolist()  # 转换为列表
    matrix = [[float(value) for value in row] for row in matrix]  # 确保矩阵中的值是 float 类型

    # 转换误差列表中的值为原生 float 类型
    errors = [{"point": i + 1, "error_x": float(error[0]), "error_y": float(error[1])} for i, error in enumerate(errors)]

    # 返回矩阵和误差
    return matrix, errors
