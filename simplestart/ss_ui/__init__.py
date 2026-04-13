from .card import card, section, container
from .rate import rate
from .button import button, button_group
from .link import link
from .icon import icon, bootstrap_icon, icon_with_bg
from .space import space
from .splitter import splitter
## from .text import text, 通过懒加载加载
from .checkbox import checkbox, checkboxes
from .autocomplete import autocomplete
from .input import input, text_input
from .input_number import input_number
from .radio import radio
from .selectbox import selectbox
from .slider import slider
from .switch import switch
from .upload import upload
from .avatar import avatar
from .badge import badge
from .carousel import carousel
from .collapse import collapse
from .descriptions import descriptions
from .empty import empty
from .image import image
from .table import table
from .grid import grid
from .columns import columns
from .alert import alert
from .dialog import dialog
from .messagebox import messagebox
from .tabs import tabs
from .affix import affix
from .breadcrumb import breadcrumb
from .anchor import anchor
from .panel import panel
from .divider import divider
from .listbox import listbox
from .htmlview import htmlview
from .menu import menu
from .video import video
from .audio import audio
from .overlay import overlay
from .markdown import markdown, md
from .write import write
from .colorpicker import colorpicker
from .popconfirm import popconfirm
from .layout import row, col
from .timer import timer
from .plot import plot

#不太成熟，以后再弄
##from .echarts import echarts

__all__ = [
    'card', 'section', 'container',
    'rate',
    'button', 'button_group',
    'link',
    'icon', 'bootstrap_icon', 'icon_with_bg',
    'space',
    'splitter',
    'text',
    'checkbox', 'checkboxes',
    'autocomplete',
    'input', 'text_input',
    'radio',
    'selectbox',
    'slider',
    'switch',
    'upload',
    'avatar',
    'badge',
    'carousel',
    'collapse',
    'descriptions',
    'empty',
    'image',
    'table',
    'grid',
    'columns',
    'alert',
    'dialog',
    'messagebox',
    'tabs',
    'affix',
    'breadcrumb',
    'anchor',
    'panel',
    'divider',
    'listbox',
    'htmlview',
    'menu',
    'video',
    'audio',
    'overlay',
    'markdown', 'md',
    'write',
    'colorpicker',
    'popconfirm',
    'row', 'col',
    'timer',
    'plot'
]

import importlib

class LazyLoader:
    """
    一个用于实现模块级懒加载的包装器类。
    """
    def __init__(self, module_name):
        self.module_name = module_name
        self._module = None

    def _load(self):
        if self._module is None:
            # 这里才真正执行导入
            print("真得调入懒加载组件:", self.module_name)
            self._module = importlib.import_module(self.module_name)
        return self._module

    def __getattr__(self, name):
        # 当访问任何属性时（如 ss.text.style），先加载模块，然后返回模块中的对应属性
        module = self._load()
        return getattr(module, name)

    # --- 新增的关键方法 ---
    def __call__(self, *args, **kwargs):
        # 当对象被像函数一样调用时（如 ss.text(...)），执行此方法
        # 1. 首先加载真实的模块
        module = self._load()
        
        # 2. 假设模块中有一个与模块同名的函数/类。
        #    例如，从 '.text' 模块中获取 'text' 函数。
        #    我们使用 module.__name__.split('.')[-1] 来获取模块名的最后一部分。
        target_name = module.__name__.split('.')[-1]
        target_func = getattr(module, target_name)
        
        # 3. 调用这个真实的函数，并传入所有参数
        ##print("懒加载组件:", target_name)
        return target_func(*args, **kwargs)

# 1. 将直接导入改为懒加载代理
# 例如，text 组件
text = LazyLoader('ss_ui.text')