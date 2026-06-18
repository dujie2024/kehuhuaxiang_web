#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将项目编译为可执行程序
使用 PyInstaller 打包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装,正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安装完成")
        return True

def create_spec_file():
    """创建 PyInstaller spec 文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.ini', '.'),
        ('logs', 'logs'),
    ],
    hiddenimports=[
        'customtkinter',
        'tkcalendar',
        'matplotlib',
        'mplcursors',
        'pymysql',
        'configparser',
        'tkinter',
        'tkinter.messagebox',
        'tkinter.ttk',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'numpy',
        'PIL',
        'PIL._tkinter_finder',
        'dateutil',
        'dateutil.parser',
        'babel',
        'babel.dates',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='新朝旅游客户画像分析系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为 False 隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
    
    with open('新朝旅游客户画像分析系统.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print("✅ 创建 spec 文件完成")

def create_version_info():
    """创建版本信息文件"""
    version_info = '''# UTF-8
#
# 版本信息文件
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 2, 0, 0),
    prodvers=(1, 2, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'新朝旅游'),
            StringStruct(u'FileDescription', u'新朝旅游客户画像分析系统'),
            StringStruct(u'FileVersion', u'1.2.0'),
            StringStruct(u'InternalName', u'carpark'),
            StringStruct(u'LegalCopyright', u'Copyright (C) 2026 新朝旅游'),
            StringStruct(u'OriginalFilename', u'新朝旅游客户画像分析系统.exe'),
            StringStruct(u'ProductName', u'新朝旅游客户画像分析系统'),
            StringStruct(u'ProductVersion', u'1.2.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    print("✅ 创建版本信息文件完成")

def create_icon():
    """创建简单的图标文件"""
    # 这里可以创建一个简单的图标,或者用户可以自己提供
    if not os.path.exists('icon.ico'):
        print("⚠️  未找到 icon.ico 文件,将使用默认图标")
        print("💡 如需自定义图标,请准备一个 256x256 的 icon.ico 文件")

def build_executable():
    """构建可执行文件"""
    print("🔨 开始构建可执行文件...")
    
    # 清理之前的构建
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 执行 PyInstaller
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        '新朝旅游客户画像分析系统.spec'
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ 构建完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False

def create_portable_package():
    """创建便携版压缩包"""
    dist_dir = Path('dist')
    exe_path = dist_dir / '新朝旅游客户画像分析系统.exe'
    
    if not exe_path.exists():
        print("❌ 可执行文件不存在,无法创建便携版")
        return False
    
    print("📦 创建便携版...")
    
    # 创建便携版目录
    portable_dir = Path('dist/新朝旅游客户画像分析系统_便携版')
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制可执行文件
    shutil.copy2(exe_path, portable_dir)
    
    # 复制必要文件
    essential_files = [
        'config.ini',
        '启动程序.bat',
        'README_ARCHITECTURE.md',
        '界面优化说明.md',
        '电子围栏模块说明.md'
    ]
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, portable_dir)
    
    # 创建必要的目录
    (portable_dir / 'logs').mkdir(exist_ok=True)
    
    # 创建使用说明
    readme_content = '''# 新朝旅游客户画像分析系统 - 便携版

## 🚀 使用说明

### 1. 直接运行
双击 `新朝旅游客户画像分析系统.exe` 即可启动程序

### 2. 配置数据库
编辑 `config.ini` 文件,配置数据库连接信息:
```ini
[database.carpark]
host = 你的数据库地址
user = 用户名
password = 密码
database = carpark
port = 3306

[database.dzwl]
host = 你的数据库地址
user = 用户名
password = 密码
database = dzwl
port = 3306
```

### 3. 功能模块
- 📊 停车数据分析
- 🎫 预订数据分析  
- 🔒 电子围栏客流分析

### 4. 注意事项
- 首次运行可能较慢,请耐心等待
- 确保 MySQL 服务正常运行
- 日志文件保存在 `logs` 目录下

## 📞 技术支持
如有问题请联系技术支持

---
版本: v1.2.0
更新日期: 2026-01-23
'''
    
    with open(portable_dir / '使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 便携版创建完成!")
    return True

def main():
    """主函数"""
    print("🎯 新朝旅游客户画像分析系统 - 打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('app.py'):
        print("❌ 未找到 app.py 文件,请在项目根目录运行此脚本")
        return
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建必要文件
    create_spec_file()
    create_version_info()
    create_icon()
    
    # 构建可执行文件
    if build_executable():
        # 创建便携版
        create_portable_package()
        
        print("\n🎉 打包完成!")
        print("=" * 50)
        print("📁 输出文件:")
        print("  📦 可执行文件: dist/新朝旅游客户画像分析系统.exe")
        print("  📦 便携版目录: dist/新朝旅游客户画像分析系统_便携版/")
        print("\n💡 使用建议:")
        print("  1. 直接运行 exe 文件")
        print("  2. 或使用便携版目录分发")
        print("  3. 记得配置数据库连接信息")

if __name__ == '__main__':
    main()
