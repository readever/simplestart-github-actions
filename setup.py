from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import glob

# 获取simplestart目录下的所有C文件（由Cython生成）
top_level_files = [f for f in glob.glob("simplestart/*.c") if f != "simplestart/__init__.c"]

# 获取simplestart子目录下的所有C文件
core_files = [f for f in glob.glob("simplestart/ss_core/*.c") if f != "simplestart/ss_core/__init__.c"]
api_files = [f for f in glob.glob("simplestart/ss_api/*.c") if f != "simplestart/ss_api/__init__.c"]
modules_files = [f for f in glob.glob("simplestart/ss_modules/*.c") if f != "simplestart/ss_modules/__init__.c"]
ui_files = [f for f in glob.glob("simplestart/ss_ui/*.c") if f != "simplestart/ss_ui/__init__.c"]
system_files = [f for f in glob.glob("simplestart/ss_system/*.c") if f != "simplestart/ss_system/__init__.c"]

# 为每个模块创建单独的Extension
extensions = []

# 顶层模块
for file in top_level_files:
    module_name = "simplestart." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# core模块
for file in core_files:
    module_name = "simplestart.ss_core." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# api模块
for file in api_files:
    module_name = "simplestart.ss_api." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# modules模块
for file in modules_files:
    module_name = "simplestart.ss_modules." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# ui模块
for file in ui_files:
    module_name = "simplestart.ss_ui." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

# system模块
for file in system_files:
    module_name = "simplestart.ss_system." + os.path.splitext(os.path.basename(file))[0]
    extensions.append(Extension(module_name, [file]))

setup(
    name="simplestart",
    version="0.0.1.44",
    author="wy",
    description="build web app using python",
    ext_modules=extensions,
    packages=["simplestart", "simplestart.ss_api", "simplestart.ss_core", "simplestart.ss_modules", "simplestart.ss_ui", "simplestart.ss_system"],
    package_dir={"simplestart": "simplestart"},
    package_data={
        "simplestart": ["*.py", "ss_core/*.py", "ss_api/*.py", "ss_modules/*.py", "ss_ui/*.py", "ss_system/*.py", "static/*", "static/**/*"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ss = simplestart.launch:start",
            "simplestart = simplestart.launch:start",
            "pyramid = simplestart.pyramid:main"
        ]
    }
)