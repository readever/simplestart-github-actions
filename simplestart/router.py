'''
Router module - contains all route definitions
This file is NOT converted to C to avoid ASGI parameter issues
'''
import asyncio
import contextlib
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import Response, JSONResponse, FileResponse, PlainTextResponse, HTMLResponse
from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
import sys
import uuid
import random
import json
import copy
import importlib
import io
from io import BytesIO
import mimetypes
import time
from pathlib import Path

# 导入 server 模块中的业务函数
import server

package_path = os.path.dirname(os.path.abspath(__file__))

# 中间件配置
middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["*"])
]

# ============ 路由处理函数定义 ============

# 媒体文件处理路由 - 支持 /media/ 路径
async def _media_handler(request):
    ##myprint("媒体请求", request)
    return await server.media_handler(request)

# 从routing.py合并的路由装饰器
async def _home(request):
    return await server.home(request)

# 为 favicon.ico 添加专门的路由
async def _favicon(request):
    return FileResponse(path=f"{package_path}/static/favicon.ico")

# 为 favicon.ico/ 添加专门的路由（处理末尾有斜杠的情况）
async def _favicon_with_slash(request):
    return FileResponse(path=f"{package_path}/static/favicon.ico")

# 为 config.js 添加专门的路由
async def _config_js(request):
    return FileResponse(path=f"{package_path}/static/config.js")

# 为 config.js/ 添加专门的路由（处理末尾有斜杠的情况）
async def _config_js_with_slash(request):
    return FileResponse(path=f"{package_path}/static/config.js")
    
# Serve static files
async def _static_root(request):
    return await server.send_static(request)

#这个对于发布后的版本刷新 /pages/...有用
async def _send_static(request):
    print("static root for /pages/...")
    return await server.send_static(request)

#支持basepath了
async def _send_static_with_basepath(request):
    print("static root for /basepath/pages/...")
    return await server.send_static(request)

async def _send_static_resource(request):
    return await server.send_static_resource(request)

# WebSocket 路由
async def _websocket_endpoint(websocket):   
    await server.websocket_endpoint(websocket)

# Upload 路由
async def _upload_file(request: Request):
    return await server.upload_file(request)

# 资源路由
async def _resource(request: Request):
    return await server.resource(request)

# API 路由
async def _init_system(request):
    return await server.init_system(request)

async def _init_system2(request):
    return await server.init_system(request)

async def _init_main(request):   
    return await server.init_main(request)

#将来和上面合并，用这个替代上面？还是单独吧
async def _page_init(request):      
    return await server.page_init(request)

async def _page_init_sub(request):      
    return await server.page_init(request)

# Users 路由
async def _get_users(request):
    print("users")
    pass


# ============ 路由列表定义 ============
routes = [
    # 媒体文件处理路由
    Route('/media/{filename:path}', _media_handler),
    # 主页路由
    Route('/hello', _home),
    # favicon.ico 路由
    Route('/favicon.ico', _favicon),
    Route('/favicon.ico/', _favicon_with_slash),
    # config.js 路由
    Route('/config.js', _config_js),
    Route('/config.js/', _config_js_with_slash),
    # 静态文件路由
    Route('/', _static_root),
    Route('/{basepath}/', _static_root),
    Route('/pages/{path:path}', _send_static),
    Route('/{basepath}/pages/{path:path}', _send_static_with_basepath),
    Route('/assets/{path}', _send_static_resource),
    # Upload 路由
    Route('/upload', _upload_file, methods=['POST']),
    # 资源路由
    Route('/ss/res/{url}', _resource),
    # API 路由
    Route('/api/init', _init_system),
    Route('/api/init/{pre_clientid}', _init_system2),
    Route('/api/page/main/{clientid}', _init_main),
    Route('/api/page/more/{pagename}/{clientid}', _page_init),
    Route('/api/page/more/{sub}/{pagename}/{clientid}', _page_init_sub),
    # Users 路由
    Route('/users', _get_users, methods=['GET']),
    # WebSocket 路由
    WebSocketRoute('/api/stream', _websocket_endpoint),
]


# ============ Lifespan 机制（替代 on_event）============
@contextlib.asynccontextmanager
async def lifespan(app):
    # 启动时执行
    await server._startup(app)
    yield
    # 关闭时执行
    await server._shutdown(app)


# 创建 app 对象
app = Starlette(middleware=middleware, routes=routes, lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key='asecret')
app.workpath = os.getcwd()