"""
简洁文件侧边栏使用示例
"""
import os

# 从 modules.menu 导入 create_sidebar 函数
from ss_modules.menu import create_sidebar

# 从环境变量获取语言参数
lang = os.environ.get("ss_lang", None)
print(f"执行了 default.py，语言参数: {lang}")
if lang == None:
    lang = ""

# 创建侧边栏菜单
create_sidebar(lang=lang)
