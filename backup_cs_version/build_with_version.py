#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带版本信息的打包脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# 导入版本信息
from version import __version__, __app_name__, __build_date__

def create_version_info():
    """创建版本信息文件"""
    build_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    version_parts = __version__.replace('.', ', ')
    
    version_info_content = f'''# UTF-8
#
# 版本信息文件 - 自动生成
# 生成时间: {build_time}

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_parts}, 0),
    prodvers=({version_parts}, 0),
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
            StringStruct(u'FileDescription', u'{__app_name__}'),
            StringStruct(u'FileVersion', u'{__version__}'),
            StringStruct(u'InternalName', u'carpark'),
            StringStruct(u'LegalCopyright', u'Copyright (C) 2026 新朝旅游'),
            StringStruct(u'OriginalFilename', u'{__app_name__}.exe'),
            StringStruct(u'ProductName', u'{__app_name__}'),
            StringStruct(u'ProductVersion', u'{__version__}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info_content)
    print(f"[OK] 版本信息已更新 ({__version__})")

def create_spec_with_version():
    """创建带版本信息的 spec 文件"""
    icon_line = "icon='icon.ico' if os.path.exists('icon.ico') else None,"
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
# 自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 版本: {__version__}

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.ini', '.'),
        ('logs', 'logs'),
        ('version.py', '.'),
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
    hooksconfig={{}},
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
    name='{__app_name__}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {icon_line}
    version='version_info.txt',
)
"""
    
    spec_filename = f'{__app_name__}_v{__version__}.spec'
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print(f"[OK] Spec 文件已创建: {spec_filename}")
    return spec_filename

def clean_build_artifacts():
    """清理构建产物"""
    print("[CLEAN] 清理构建产物...")
    
    artifacts = ['build', '*.spec']
    
    for artifact in artifacts:
        if '*' in artifact:
            import glob
            for file_path in glob.glob(artifact):
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"  删除: {file_path}")
        else:
            if os.path.exists(artifact):
                if os.path.isdir(artifact):
                    shutil.rmtree(artifact)
                else:
                    os.remove(artifact)
                print(f"  删除: {artifact}")

def build_executable(spec_filename):
    """构建可执行文件"""
    print("[BUILD] 构建可执行文件...")
    
    # 查找 PyInstaller 路径
    pyinstaller_path = shutil.which('pyinstaller')
    if not pyinstaller_path:
        # 尝试虚拟环境路径
        venv_pyinstaller = os.path.join(os.path.dirname(sys.executable), 'pyinstaller.exe')
        if os.path.exists(venv_pyinstaller):
            pyinstaller_path = venv_pyinstaller
        else:
            print("[ERROR] 未找到 PyInstaller，请先安装: pip install pyinstaller")
            return False
    
    # 执行 PyInstaller
    cmd = [
        pyinstaller_path,
        '--clean',
        '--noconfirm',
        spec_filename
    ]
    
    try:
        subprocess.check_call(cmd)
        print("[OK] 构建完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 构建失败: {e}")
        return False

def create_version_portable():
    """创建版本化便携包"""
    print("[PACKAGE] 创建版本化便携包...")
    
    dist_dir = Path('dist')
    exe_path = dist_dir / f'{__app_name__}.exe'
    
    if not exe_path.exists():
        print("[ERROR] 可执行文件不存在")
        return False
    
    # 创建便携版目录
    portable_dir = dist_dir / f'{__app_name__}_v{__version__}_便携版'
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制可执行文件
    shutil.copy2(exe_path, portable_dir)
    print(f"  复制: {exe_path.name}")
    
    # 复制必要文件
    essential_files = [
        'config.ini',
        '启动程序.bat',
        'README_ARCHITECTURE.md',
        '界面优化说明.md',
        '电子围栏模块说明.md',
        'database_user_setup.sql',
        '数据库权限配置说明.md',
        'version.py'
    ]
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, portable_dir)
            print(f"  复制: {file_name}")
    
    # 创建必要的目录
    (portable_dir / 'logs').mkdir(exist_ok=True)
    
    # 创建版本化使用说明
    readme_content = f'''# {__app_name__} v{__version__} - 便携版

## 🎉 版本信息

**版本**: v{__version__}  
**构建日期**: {__build_date__}  
**应用名称**: {__app_name__}  
**作者**: 新朝旅游

### v{__version__} 新特性
- ✅ **数据库安全改进**: 不再使用 root 账户
- ✅ **专用应用账户**: carpark_app 只读权限
- ✅ **权限最小化**: 只授予查询权限
- ✅ **安全配置**: 包含完整的数据库权限配置
- ✅ **版本管理**: 添加程序版本信息显示

## 🚀 使用说明

### 1. 直接运行
双击 `{__app_name__}.exe` 即可启动程序

### 2. 配置数据库
编辑 `config.ini` 文件，配置数据库连接信息:

```ini
[database.carpark]
host = 你的数据库地址
user = carpark_app          # 使用应用专用账户
password = carpark_app_2026
database = carpark
port = 3306

[database.dzwl]
host = 你的数据库地址
user = carpark_app          # 使用应用专用账户
password = carpark_app_2026
database = dzwl
port = 3306
```

### 3. 数据库用户设置
首次使用前，需要在数据库中创建应用用户：

```bash
# 使用 root 账户执行
mysql -u root -p < database_user_setup.sql
```

详细说明请参考 `数据库权限配置说明.md`

## 📊 功能模块

- 📊 **停车数据分析**: 分析停车场使用情况
- 🎫 **预订数据分析**: 分析票务预订数据  
- 🔒 **电子围栏客流**: 分析景区进出客流

## 🛡️ 安全特性

### 数据库安全
- ✅ **专用账户**: 使用 carpark_app 账户
- ✅ **最小权限**: 只授予 SELECT 权限
- ✅ **权限隔离**: 应用和管理分离
- ✅ **访问控制**: 建议限制访问IP

### 安全建议
- 🔑 修改默认密码 `carpark_app_2026`
- 🚫 不要使用 root 账户
- 📝 定期审计数据库权限
- 🔒 限制数据库访问IP

## 📚 文档说明

包含完整的技术文档:
- `README_ARCHITECTURE.md`: 系统架构说明
- `界面优化说明.md`: 界面功能介绍
- `电子围栏模块说明.md`: 电子围栏模块使用
- `database_user_setup.sql`: 数据库用户创建脚本
- `数据库权限配置说明.md`: 详细权限配置指南

## 🛠️ 故障排除

### 常见问题

**Q: 程序无法启动**
A: 检查系统是否为 64位 Windows，关闭杀毒软件重试

**Q: 数据库连接失败**
A: 
- 检查 MySQL 服务是否启动
- 验证 config.ini 配置是否正确
- 确认数据库用户 `carpark_app` 已创建
- 检查用户密码是否正确

**Q: 权限不足错误**
A: 
- 确认数据库用户已正确创建
- 执行 `GRANT SELECT ON database.* TO 'carpark_app'@'%';`
- 检查用户权限: `SHOW GRANTS FOR 'carpark_app'@'%';`

### 日志查看
日志文件位置: `logs/` 目录下
- `app.log`: 主程序日志
- `models.database.log`: 数据库日志

## 📞 技术支持

如有问题请联系技术支持，并提供以下信息:
- 系统版本
- 错误信息
- 日志文件内容
- 数据库权限配置

---
**版本**: v{__version__}  
**构建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**更新内容**: 数据库安全改进 + 版本管理
'''
    
    with open(portable_dir / '使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("[OK] 版本化便携包创建完成!")
    return True

def create_distribution_archive():
    """创建分发压缩包"""
    print("[PACKAGE] 创建分发压缩包...")
    
    portable_dir = Path(f'dist/{__app_name__}_v{__version__}_便携版')
    if not portable_dir.exists():
        print("[ERROR] 便携版目录不存在")
        return False
    
    # 创建 ZIP 压缩包
    import zipfile
    
    zip_filename = f'dist/{__app_name__}_v{__version__}_便携版.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in portable_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(portable_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"[OK] 压缩包已创建: {zip_filename}")
    return True

def main():
    """主函数"""
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(f"[BUILD] {__app_name__} v{__version__} - 带版本信息打包")
    print("=" * 60)
    
    # 检查当前目录
    if not os.path.exists('app.py'):
        print("[ERROR] 未找到 app.py 文件，请在项目根目录运行此脚本")
        return
    
    # 步骤 0: 清理旧的构建产物
    clean_build_artifacts()
    print()
    
    # 步骤 1: 创建版本信息
    create_version_info()
    
    # 步骤 2: 创建 spec 文件
    spec_filename = create_spec_with_version()
    
    # 步骤 3: 构建可执行文件
    if not build_executable(spec_filename):
        print("[ERROR] 构建失败，停止执行")
        return
    
    print()
    
    # 步骤 4: 创建版本化便携包
    if not create_version_portable():
        print("[ERROR] 便携包创建失败")
        return
    
    print()
    
    # 步骤 5: 创建分发压缩包
    create_distribution_archive()
    
    print()
    print("[SUCCESS] 带版本信息的分发文件创建完成!")
    print("=" * 60)
    print("[OUTPUT] 输出文件:")
    print(f"  - 可执行文件: dist/{__app_name__}.exe")
    print(f"  - 便携版目录: dist/{__app_name__}_v{__version__}_便携版/")
    print(f"  - 压缩包: dist/{__app_name__}_v{__version__}_便携版.zip")
    print()
    print("[INFO] 分发建议:")
    print("  1. 使用便携版 ZIP 包进行分发")
    print("  2. 提醒用户配置数据库专用用户")
    print("  3. 包含完整的安全配置文档")
    print("  4. 确保目标机器有 MySQL 服务")

if __name__ == '__main__':
    main()
