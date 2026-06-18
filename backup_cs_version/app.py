#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新朝旅游客户画像分析系统
主程序入口
"""

import sys
import os
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from version import get_version_string, get_version_info
from views.main_window import MainWindow
import customtkinter as ctk
from tkinter import messagebox
from utils.logger_utils import setup_logger

logger = setup_logger('CarParkApp')


def main():
    try:
        print(get_version_string())
        root = ctk.CTk()
        app = MainWindow(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"程序运行时发生异常: {e}", exc_info=True)
        messagebox.showerror("错误", f"程序发生错误: {e}")


if __name__ == "__main__":
    main()
