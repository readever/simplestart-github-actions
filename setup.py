from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import glob

# 获取simplestart目录下的所有C文件（由Cython生成）
top_level_files = [f for f in glob.glob("simplestart/*.c") if f != "simplestart/__init__.c"]

# 获取simplestart子目录下的所有C文件
core_files = [f for f in glob.glob("simplestart/core/*.c") if f != "simplestart/core/__init__.c"]
api_files = [f for f in glob.glob("simplestart/api/*.c") if f != "simplestart/api/__init__.c"]
modules_files = [f for f in glob.glob("simplestart/modules/*.c") if f != "simplestart/modules/__init__.c"]
ui_files = [f for f in glob.glob("simplestart/ui/*.c") if f != "simplestart/ui/__init__.c"]
system_files = [f for f in glob.glob("simplestart/system/*.c") if f != "simplestart/system/__init__.c"]

# 为每个模块创建单独的Extension
extensions = []

# 顶层模块
for file in top_level_files:
    module_name = "simplestart." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# core模块
for file in core_files:
    module_name = "simplestart.core." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# api模块
for file in api_files:
    module_name = "simplestart.api." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# modules模块
for file in modules_files:
    module_name = "simplestart.modules." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# ui模块
for file in ui_files:
    module_name = "simplestart.ui." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# system模块
for file in system_files:
    module_name = "simplestart.system." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

setup(
    name="simplestart",
    version="0.0.1.44",
    author="wy",
    description="build web app using python",
    ext_modules=extensions,
    packages=["simplestart", "simplestart.api", "simplestart.core", "simplestart.modules", "simplestart.ui", "simplestart.system"],
    package_dir={"simplestart": "simplestart"},
    entry_points={
        "console_scripts": [
            "ss = simplestart.launch:start",
            "simplestart = simplestart.launch:start",
            "pyramid = simplestart.pyramid:main"
        ]
    }
)