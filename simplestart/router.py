'''
Router module - contains all route definitions
This file is NOT converted to C to avoid ASGI parameter issues
'''
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
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

# 创建 app 对象（必须在 @app.route 装饰器之前定义）
app = Starlette(middleware=middleware, routes=[])
app.add_middleware(SessionMiddleware, secret_key='asecret')
app.workpath = os.getcwd()


# ============ 路由定义 ============

# 媒体文件处理路由 - 支持 /media/ 路径
@app.route('/media/{filename:path}')
async def _media_handler(request):
    ##myprint("媒体请求", request)
    return await server.media_handler(request)

# ============ 路由定义 ============

# 从routing.py合并的路由装饰器
@app.route('/hello')
async def _home(request):
    return await server.home(request)

# 为 favicon.ico 添加专门的路由
@app.route("/favicon.ico")
async def _favicon(request):
    return FileResponse(path=f"{package_path}/static/favicon.ico")

# 为 favicon.ico/ 添加专门的路由（处理末尾有斜杠的情况）
@app.route("/favicon.ico/")
async def _favicon_with_slash(request):
    return FileResponse(path=f"{package_path}/static/favicon.ico")

# 为 config.js 添加专门的路由
@app.route("/config.js")
async def _config_js(request):
    return FileResponse(path=f"{package_path}/static/config.js")

# 为 config.js/ 添加专门的路由（处理末尾有斜杠的情况）
@app.route("/config.js/")
async def _config_js_with_slash(request):
    return FileResponse(path=f"{package_path}/static/config.js")
    
# Serve static files
@app.route("/")
async def _static_root(request):
    return await server.send_static(request)

@app.route("/{basepath}/")
async def _static_root(request):
    return await server.send_static(request)

#这个对于发布后的版本刷新 /pages/...有用
@app.route("/pages/{path:path}")
async def _send_static(request):
    print("static root for /pages/...")
    return await server.send_static(request)

#支持basepath了
@app.route("/{basepath}/pages/{path:path}")
async def _send_static(request):
    print("static root for /basepath/pages/...")
    return await server.send_static(request)

@app.route("/assets/{path}")
async def _send_static_resource(request):
    return await server.send_static_resource(request)

# WebSocket 路由
@app.websocket_route('/api/stream') 
async def _websocket_endpoint(websocket):   
    await server.websocket_endpoint(websocket)

# Upload 路由
@app.route('/upload', methods=['POST'])
async def _upload_file(request: Request):
    return await server.upload_file(request)

# 资源路由
@app.route("/ss/res/{url}")
async def resource(request: Request):
    return await server.resource(request)

# API 路由
@app.route("/api/init")
async def _init_system(request):
    return await server.init_system(request)

@app.route("/api/init/{pre_clientid}")
async def _init_system2(request):
    return await server.init_system(request)

@app.route("/api/page/main/{clientid}")
async def _init_main(request):   
    return await server.init_main(request)

#将来和上面合并，用这个替代上面？还是单独吧
@app.route("/api/page/more/{pagename}/{clientid}")
async def _page_init(request):      
    return await server.page_init(request)

@app.route("/api/page/more/{sub}/{pagename}/{clientid}")
async def _page_init(request):      
    return await server.page_init(request)

# Users 路由
@app.route('/users', methods=['GET'])
async def _get_users(request):
    print("users")
    pass