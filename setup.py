import os
import re
import sys
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

# --- 1. 辅助函数：读取版本号 ---
def get_version(package_path):
    """从 __init__.py 中读取 __version__"""
    init_file = os.path.join(package_path, "__init__.py")
    if not os.path.exists(init_file):
        return "0.0.1" # 默认版本
    
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if match:
            return match.group(1)
    return "0.0.1"

# --- 2. 配置编译参数 ---
# 针对 macOS 的 Universal2 支持 (Intel + Apple Silicon)
extra_compile_args = []
extra_link_args = []

if sys.platform == "darwin":
    # 这一步很关键：告诉编译器同时生成 x86_64 和 arm64 的代码
    extra_compile_args.append("-arch")
    extra_compile_args.append("x86_64")
    extra_compile_args.append("-arch")
    extra_compile_args.append("arm64")
    
    extra_link_args.append("-arch")
    extra_link_args.append("x86_64")
    extra_link_args.append("-arch")
    extra_link_args.append("arm64")

# --- 3. 自动发现 Cython/C 扩展 ---
def get_extensions(package_dir):
    extensions = []
    # 遍历 simplestart 目录
    for root, dirs, files in os.walk(package_dir):
        # 忽略 __pycache__ 等目录
        if "__pycache__" in root:
            continue
            
        # 查找 .c 文件 (如果是发布模式) 或 .py 文件 (如果是开发模式)
        # 这里优先找 .c，因为你在 GitHub Actions 中似乎已经生成了 .c
        source_files = [f for f in files if f.endswith(".c") or (f.endswith(".py") and f != "__init__.py")]
        
        for source_file in source_files:
            # 排除 setup.py 本身（如果在根目录）
            if source_file == "setup.py":
                continue

            full_path = os.path.join(root, source_file)
            
            # 将文件路径转换为模块名，例如 simplestart/ss_core/base.c -> simplestart.ss_core.base
            # 注意：Windows 下是 \\，需要替换
            relative_path = os.path.relpath(full_path, os.path.dirname(package_dir))
            module_name = os.path.splitext(relative_path.replace(os.sep, "."))[0]
            
            # 创建扩展模块
            ext = Extension(
                name=module_name,
                sources=[full_path],
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args,
                language="c"
            )
            extensions.append(ext)
            print(f"发现扩展模块: {module_name} (源文件: {full_path})")
            
    return extensions

# --- 4. 执行 Setup ---
# 假设你的包名是 simplestart
PACKAGE_NAME = "simplestart"

setup(
    name="simplestart",
    version=get_version(PACKAGE_NAME),
    packages=find_packages(include=[f"{PACKAGE_NAME}*",]), # 找到所有包
    ext_modules=get_extensions(PACKAGE_NAME), # 注入 C 扩展
    zip_safe=False, # 包含 C 扩展时必须设为 False
    cmdclass={
        'build_ext': build_ext
    },
    # 如果你还有其他非代码数据文件（如 html, css, js），需要在这里声明
    # 但你的 .so/.c 文件已经通过 ext_modules 处理了，不需要放在 package_data 里
    package_data={
        f"{PACKAGE_NAME}": ["static/**/*", "*.py", "ss_api/*.py", "ss_modules/*.py", "ss_ui/*.py", "ss_system/*.py"],
    },
)