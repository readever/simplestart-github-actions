'''
因为cython的缘故，server.py拆成了 server.py 和 app.py. server.py 可以cython, app.py不用，直接编译

那么又因为uvicorn的调用问题，调用自己的话，会有重复的问题。所以又加了这个launch.py
unicorn.run 直接用app, 不能用reload. 用字符串,例如 run("server:app", realod=True) 才能加reload
'''

#这里只要分析命令行参数就行

'''
在setup.py中entrypoint, 
    entry_points={
        "console_scripts": ["ss = launch:start"]
    }
'''

import uvicorn
import argparse
import os
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def start():
    # 创建解析器对象
    parser = argparse.ArgumentParser(description='SimpleStart - Stream Synchronization Framework')

    # userscript 是必需的位置参数
    parser.add_argument('userscript', type=str, help='the user script to run')

    # command 是可选的位置参数
    parser.add_argument('command', nargs='?', default='', help='run mode: dev or empty')

    # 添加端口参数
    parser.add_argument('--port', type=int, default=8000, help='port number to use')
    parser.add_argument('-V', '--version', action='version', version='SimpleStart 0.50')
    parser.add_argument('--basepath', type=str, default='', help='application base path relative to host')
    parser.add_argument('--allow-origins', type=str, nargs='*', default=['http://localhost:3000', 'http://localhost:8080', 'http://localhost'], help='allowed origins for CORS (e.g., "http://localhost:3000" "https://frontend.example.com"). Default includes localhost variants for development. Use empty list to disable all cross-origin. Use "*" to allow all origins (not recommended for production)')

    # 解析参数
    args = parser.parse_args()

    # Print startup information
    ##print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    ##print(f"{Colors.BOLD}{Colors.OKBLUE}SimpleStart Launch Configuration{Colors.ENDC}")
    ##print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    ##print(f"{Colors.OKGREEN}User Script: {Colors.ENDC}{args.userscript}")
    ##print(f"{Colors.OKGREEN}Port Number: {Colors.ENDC}{args.port}")
    ##print(f"{Colors.OKGREEN}Run Mode: {Colors.ENDC}{args.command or 'default'}")
    
    # Get absolute path before changing working directory
    userscript_abs_path = os.path.abspath(args.userscript)
    userscript_dir = os.path.dirname(userscript_abs_path)
    ##print(f"{Colors.OKGREEN}Script Absolute Path: {Colors.ENDC}{userscript_abs_path}")
    ##print(f"{Colors.OKGREEN}Script Directory: {Colors.ENDC}{userscript_dir}")
    
    # Check if user script exists
    if not os.path.exists(userscript_abs_path):
        # Ask user if they want to create the script
        answer = input(f"{Colors.WARNING}Script '{args.userscript}' does not exist. Would you like to create it? (y/n): {Colors.ENDC}")
        if answer.lower() == 'y':
            # Create default script content
            default_content = '''
import simplestart as ss

# Your web app starts here
ss.write("Hello, world")
ss.text("SimpleStart initialized successfully.", tag="b")
ss.divider()

ss.write("""
Next steps:
  1. Open the generated file in your editor
  2. Start coding in Python
""")
ss.space("mb-4")
ss.text("Learn more: ")
ss.link("http://www.simplestart.cc", href="http://www.simplestart.cc", target="_blank")
'''
            # Ensure directory exists
            os.makedirs(userscript_dir, exist_ok=True)
            # Create file
            with open(userscript_abs_path, 'w', encoding='utf-8') as f:
                f.write(default_content.strip())
            print(f"{Colors.OKGREEN}Created script '{args.userscript}' with default content.{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Operation cancelled. Exiting.{Colors.ENDC}")
            sys.exit(0)
    
    # Change working directory to user script directory
    os.chdir(userscript_dir)
    ##print(f"{Colors.OKGREEN}Working Directory: {Colors.ENDC}{os.getcwd()}")

    # Execute different operations based on 'command' parameter
    '''
    if args.command == 'dev':
        print(f"{Colors.OKBLUE}Starting in dev mode: script={args.userscript}, port={args.port}, basepath={args.basepath}{Colors.ENDC}")
    else:
        print(f"{Colors.OKBLUE}Starting in normal mode: script={args.userscript}, port={args.port}, basepath={args.basepath}{Colors.ENDC}")
    '''
    
    host = '0.0.0.0'
    port = args.port

    # Print welcome message
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}Welcome to SimpleStart{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Official Website: {Colors.ENDC}http://www.simplestart.cc")
    print(f"{Colors.OKBLUE}Access Address: {Colors.ENDC}http://localhost:{port}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print()

    # 设置环境变量（必须在 import server 之前）
    os.environ["userscript_abs_path"] = userscript_abs_path
    os.environ["userscript_dir"] = os.path.dirname(userscript_abs_path)
    
    # 提取脚本名称（不含路径和扩展名）作为 user_script_path
    user_script_name = os.path.splitext(os.path.basename(userscript_abs_path))[0]
    os.environ["userscript"] = user_script_name
    
    os.environ["runmode"] = args.command
    os.environ['basepath'] = args.basepath

    # 设置 CORS 配置到环境变量
    if args.allow_origins:
        os.environ['allow_origins'] = ' '.join(args.allow_origins)
    else:
        os.environ['allow_origins'] = ''

    # 确保 src 目录在 Python 路径中
    src_dir = Path(__file__).parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    # 导入 server 模块
    import server
    
    # 设置端口号到 config，以便 convertTxt2Url 函数能够使用正确的端口号
    server.ss.config.port = port

    #路由已经合并到server.py中，直接使用server:app
    uvicorn.run("server:app", host=host, port=port, reload=False, log_level="warning")

#python3 -m src.launch testme.py --port 8001 # 启动服务器，端口为 8001 for hbuilder
if __name__ == "__main__":
    start()
