#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序版本信息
"""

__version__ = "2.0.0"
__app_name__ = "新朝旅游客户画像分析系统"
__author__ = "新朝旅游"
__build_date__ = "2026-02-28"
__description__ = "新朝旅游客户画像分析系统 - 模块化BS架构，包含停车数据分析、预订数据分析和电子围栏客流分析功能，支持快速日期选择"

def get_version_info():
    """获取版本信息"""
    return {
        "version": __version__,
        "app_name": __app_name__,
        "author": __author__,
        "build_date": __build_date__,
        "description": __description__
    }

def get_version_string():
    """获取版本字符串"""
    return f"{__app_name__} v{__version__} (构建于 {__build_date__})"

if __name__ == "__main__":
    print(get_version_string())
    print(f"描述: {__description__}")
    print(f"作者: {__author__}")
