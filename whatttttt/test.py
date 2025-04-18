import os
import logging

def log_init():
    # 创建一个 Logger，使用模块名作为名称
    mylogger = logging.getLogger(__name__)
    mylogger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 创建文件处理器，用于将日志写入文件
    file_handler = logging.FileHandler('demo.log', mode='a')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 创建控制台处理器，用于将日志输出到控制台
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # 将处理器添加到 Logger
    mylogger.addHandler(file_handler)
    mylogger.addHandler(console_handler)

    return mylogger

if __name__ == '__main__':
    # 初始化日志记录器
    logger = log_init()

    # 记录日志
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")