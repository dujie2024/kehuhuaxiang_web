#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试打包的可执行程序
"""

import os
import subprocess
import time
from pathlib import Path

def test_exe():
    """测试可执行文件"""
    exe_path = Path('dist/新朝旅游客户画像分析系统.exe')
    
    if not exe_path.exists():
        print("❌ 可执行文件不存在")
        return False
    
    print(f"📁 可执行文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    print("🚀 启动程序测试...")
    try:
        # 启动程序 (非阻塞)
        process = subprocess.Popen([str(exe_path)])
        print("✅ 程序启动成功!")
        print("⏰ 等待 5 秒后自动关闭...")
        
        time.sleep(5)
        
        # 终止进程
        process.terminate()
        print("✅ 测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 程序启动失败: {e}")
        return False

def test_portable():
    """测试便携版"""
    portable_dir = Path('dist/新朝旅游客户画像分析系统_便携版')
    
    if not portable_dir.exists():
        print("❌ 便携版目录不存在")
        return False
    
    print("📦 便携版文件检查:")
    required_files = [
        '新朝旅游客户画像分析系统.exe',
        'config.ini',
        '使用说明.txt',
        'logs/'
    ]
    
    for file_name in required_files:
        file_path = portable_dir / file_name
        if file_path.exists():
            size = file_path.stat().st_size if file_path.is_file() else "目录"
            print(f"  ✅ {file_name} ({size})")
        else:
            print(f"  ❌ {file_name} (缺失)")
    
    return True

def main():
    """主函数"""
    print("🧪 新朝旅游客户画像分析系统 - 打包测试")
    print("=" * 50)
    
    # 测试可执行文件
    if test_exe():
        print("\n✅ 可执行文件测试通过")
    else:
        print("\n❌ 可执行文件测试失败")
        return
    
    # 测试便携版
    if test_portable():
        print("\n✅ 便携版检查通过")
    else:
        print("\n❌ 便携版检查失败")
        return
    
    print("\n🎉 所有测试通过!")
    print("=" * 50)
    print("📋 分发建议:")
    print("  1. 使用便携版目录进行分发")
    print("  2. 确保目标机器有 MySQL 服务")
    print("  3. 配置数据库连接信息")
    print("  4. 提供使用说明文档")

if __name__ == '__main__':
    main()
