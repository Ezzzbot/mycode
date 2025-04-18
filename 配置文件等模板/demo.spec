# -*- mode: python ; coding: utf-8 -*-

#主要修改，入口脚本，pathex，binaries，datas可加也可以后期把配置文件之类的自己拖过去

# 定义基本信息
block_cipher = None  # 如果需要加密二进制文件，可以设置一个块加密器
# 定义分析阶段
a = Analysis(
    ['VersionArm6DCL.py'],  # 主入口脚本，打包时会从这个文件开始分析依赖关系
    pathex=['../../ZyzVersionAndArm', '.'],  # 指定模块搜索路径，确保 PyInstaller 能找到所有依赖模块
    binaries=[],  # 额外的二进制文件（例如动态链接库），可以添加格式为 ('源文件路径', '目标路径')
    datas=[],  # 额外的数据文件（例如配置文件、图片等），可以添加格式为 ('源文件路径', '目标路径')
    hiddenimports=[],  # 手动指定隐藏的模块导入，PyInstaller 可能无法自动检测到这些模块
    hookspath=[],  # 自定义钩子文件路径，用于扩展 PyInstaller 的功能
    hooksconfig={},  # 钩子配置项，通常不需要修改
    runtime_hooks=[],  # 运行时钩子文件路径，用于在运行时执行自定义逻辑
    excludes=[],  # 排除不需要打包的模块，减少最终文件大小
    noarchive=False,  # 是否将 Python 字节码存储为单独的文件而不是归档到一个文件中
    optimize=0,  # 优化级别，0 表示不优化，1 和 2 分别表示不同的优化级别
)

# 创建 PYZ 归档文件（包含所有的 Python 字节码）
pyz = PYZ(a.pure)  # 将纯 Python 模块打包成一个归档文件

# 定义 EXE 构建选项
exe = EXE(
    pyz,  # 包含 Python 字节码的归档文件
    a.scripts,  # 主脚本文件
    a.binaries,  # 二进制文件（如动态链接库）
    a.datas,  # 数据文件
    [],  # 其他额外的参数，通常为空
    name='VersionArm6DCL',  # 输出的可执行文件名称
    debug=False,  # 是否启用调试模式
    bootloader_ignore_signals=False,  # 是否忽略信号（主要用于 macOS）
    strip=False,  # 是否剥离二进制文件中的符号表（减小文件大小）
    upx=True,  # 是否使用 UPX 压缩工具来压缩可执行文件
    upx_exclude=[],  # 排除不需要 UPX 压缩的文件
    runtime_tmpdir=None,  # 指定运行时临时目录，默认为 None
    console=True,  # 是否显示控制台窗口（True 显示，False 不显示）
    disable_windowed_traceback=False,  # 禁用窗口化应用程序的错误回溯（仅适用于 Windows）
    argv_emulation=False,  # 是否模拟命令行参数（主要用于 macOS）
    target_arch=None,  # 目标架构（例如 x86_64、arm64），默认为 None 表示自动检测
    codesign_identity=None,  # macOS 代码签名身份，默认为 None
    entitlements_file=None,  # macOS 权限文件路径，默认为 None
)