from .card import card, section, container
## from .rate import rate, 通过懒加载加载
from .button import button, button_group
## from .link import link, 通过懒加载加载
## from .icon import icon, bootstrap_icon, icon_with_bg
## from .space import space
## from .splitter import splitter, 通过懒加载加载
## from .text import text, 通过懒加载加载
## from .checkbox import checkbox, checkboxes 通过懒加载加载
## from .autocomplete import autocomplete, 通过懒加载加载
## from .input import input, text_input 通过懒加载加载
## from .input_number import input_number
## from .radio import radio 通过懒加载加载
## from .selectbox import selectbox
## from .slider import slider
## from .switch import switch, 通过懒加载加载
## from .upload import upload, 通过懒加载加载
## from .avatar import avatar, 通过懒加载加载
## from .badge import badge, 通过懒加载加载
## from .carousel import carousel, 通过懒加载加载
## from .collapse import collapse, 通过懒加载加载
## from .descriptions import descriptions, 通过懒加载加载
## from .empty import empty
## from .image import image
## from .table import table, 通过懒加载加载
## from .grid import grid, 通过懒加载加载
## from .columns import columns, 通过懒加载加载
## from .alert import alert, 通过懒加载加载
## from .dialog import dialog, 通过懒加载加载
## from .messagebox import messagebox
## from .tabs import tabs 通过懒加载加载
## from .affix import affix 通过懒加载加载
## from .breadcrumb import breadcrumb 通过懒加载加载
## from .anchor import anchor, 通过懒加载加载
## from .panel import panel, 通过懒加载加载
## from .divider import divider, 通过懒加载加载
## from .listbox import listbox, 通过懒加载加载 
## from .htmlview import htmlview, 通过懒加载加载
## from .menu import menu, 通过懒加载加载
## from .video import video, 通过懒加载加载
## from .audio import audio, 通过懒加载加载
## from .overlay import overlay, 通过懒加载加载
from .markdown import markdown, md
from .write import write
## from .colorpicker import colorpicker, 通过懒加载加载
## from .popconfirm import popconfirm, 通过懒加载加载
from .layout import row, col ###, 通过懒加载加载
## from .timer import timer, 通过懒加载加载
## from .plot import plot, 通过懒加载加载
from ss_core.print import myprint

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
    def __init__(self, module_name, attr_name=None):
        self.module_name = module_name
        self.attr_name = attr_name
        self._module = None
        self._target = None

    def _load(self):
        if self._module is None:
            # 这里才真正执行导入
            myprint("真得调入懒加载组件:", self.module_name, color = "red")
            self._module = importlib.import_module(self.module_name)
            
            # 如果指定了属性名，获取该属性
            if self.attr_name:
                self._target = getattr(self._module, self.attr_name)
        return self._module

    def __getattr__(self, name):
        # 当访问任何属性时（如 ss.text.style），先加载模块
        self._load()
        
        # 如果有目标属性，从目标属性获取
        if self._target:
            return getattr(self._target, name)
        # 否则从模块获取
        return getattr(self._module, name)

    # --- 新增的关键方法 ---
    def __call__(self, *args, **kwargs):
        # 当对象被像函数一样调用时（如 ss.text(...)），执行此方法
        # 1. 首先加载真实的模块
        self._load()
        
        # 2. 如果有目标属性，直接调用它
        if self._target:
            return self._target(*args, **kwargs)
        
        # 3. 否则，假设模块中有一个与模块同名的函数/类
        #    例如，从 '.text' 模块中获取 'text' 函数
        module = self._module
        target_name = module.__name__.split('.')[-1]
        target_func = getattr(module, target_name)
        
        # 4. 调用这个函数/类，并返回其结果
        return target_func(*args, **kwargs)

# 1. 将直接导入改为懒加载代理
# 例如，text 组件
checkbox = LazyLoader('ss_ui.checkbox')
checkboxes = LazyLoader('ss_ui.checkbox')
rate = LazyLoader('ss_ui.rate')
link = LazyLoader('ss_ui.link')
splitter = LazyLoader('ss_ui.splitter')
text = LazyLoader('ss_ui.text')
autocomplete = LazyLoader('ss_ui.autocomplete')
upload = LazyLoader('ss_ui.upload')
table = LazyLoader('ss_ui.table')
menu = LazyLoader('ss_ui.menu')
video = LazyLoader('ss_ui.video')
audio = LazyLoader('ss_ui.audio')
input = LazyLoader('ss_ui.input')
text_input = LazyLoader('ss_ui.input')
input_number = LazyLoader('ss_ui.input_number')
radio = LazyLoader('ss_ui.radio')
selectbox = LazyLoader('ss_ui.selectbox')
slider = LazyLoader('ss_ui.slider')
tabs = LazyLoader('ss_ui.tabs')
affix = LazyLoader('ss_ui.affix')
breadcrumb = LazyLoader('ss_ui.breadcrumb')
grid = LazyLoader('ss_ui.grid')
columns = LazyLoader('ss_ui.columns')
image = LazyLoader('ss_ui.image')
alert = LazyLoader('ss_ui.alert')
dialog = LazyLoader('ss_ui.dialog')
messagebox = LazyLoader('ss_ui.messagebox')
upload = LazyLoader('ss_ui.upload')
avatar = LazyLoader('ss_ui.avatar')
badge = LazyLoader('ss_ui.badge')
carousel = LazyLoader('ss_ui.carousel')
collapse = LazyLoader('ss_ui.collapse')
descriptions = LazyLoader('ss_ui.descriptions')
empty = LazyLoader('ss_ui.empty')
switch = LazyLoader('ss_ui.switch')
anchor = LazyLoader('ss_ui.anchor')
panel = LazyLoader('ss_ui.panel')
divider = LazyLoader('ss_ui.divider')
listbox = LazyLoader('ss_ui.listbox')
htmlview = LazyLoader('ss_ui.htmlview')
overlay = LazyLoader('ss_ui.overlay')
colorpicker = LazyLoader('ss_ui.colorpicker')
popconfirm = LazyLoader('ss_ui.popconfirm')
timer = LazyLoader('ss_ui.timer')
# 特殊处理 plot，因为 line 等方法是 Plot 类的实例方法
plot = LazyLoader('ss_ui.plot', 'plot')
space = LazyLoader('ss_ui.space')

# 正确写法 - 需要分别懒加载每个函数
icon = LazyLoader('ss_ui.icon', 'icon')
bootstrap_icon = LazyLoader('ss_ui.icon', 'bootstrap_icon')
icon_with_bg = LazyLoader('ss_ui.icon', 'icon_with_bg')