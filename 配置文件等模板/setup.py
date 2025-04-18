from setuptools import setup, find_packages

# 定义项目的元数据
setup(
    name="tools_exe",  # 包的名称
    version="0.1.0",           # 版本号
    author="TLQ",        # 作者名
    author_email="tanlinquanqaq@gmail.com",  # 作者邮箱
    description="小谭的工具箱",  # 简短描述
    #long_description=open("README.md").read(),          # 长描述，通常从 README 文件读取
    #long_description_content_type="text/markdown",      # 长描述的内容类型
    url="https://https://github.com/Ezzzbot/mycode",    # 项目主页（如 GitHub 地址）
    packages=find_packages(),  # 自动查找所有需要包含的包
    classifiers=[               # 分类器，帮助 PyPI 分类你的包
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",    # 指定支持的 Python 版本
)