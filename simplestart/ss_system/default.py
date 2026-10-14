"""
简洁文件侧边栏使用示例
"""
import os

# 从 modules.menu 导入 create_sidebar 函数
from ss_modules.menu import create_sidebar
import simplestart as ss

# 创建侧边栏菜单
mysidebar = create_sidebar()

# 应用级侧边栏扩展：若应用主脚本定义了 sidebar_ext()，则在其底部追加内容
if mysidebar:
    main_mod = ss.modules.get("main")
    hook = getattr(main_mod, "sidebar_ext", None) if main_mod else None
    if hook:
        with mysidebar:
            hook()
