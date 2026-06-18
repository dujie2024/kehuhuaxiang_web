#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web图表生成工具
使用matplotlib生成图表并转换为base64编码的图片
"""

import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def generate_web_chart(data, start_date, end_date, title_prefix, chart_type):
    """
    生成Web图表
    
    Args:
        data: 数据列表 [(location, count), ...]
        start_date: 开始日期
        end_date: 结束日期
        title_prefix: 标题前缀（停车场名或项目名）
        chart_type: 图表类型
    
    Returns:
        base64编码的图片字符串
    """
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 提取数据
    locations = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制柱状图
    bars = ax.bar(range(len(locations)), counts, color='#1f77b4', alpha=0.8)
    
    # 设置标题和标签
    ax.set_title(f"{title_prefix} - {chart_type}车辆（游客）客源地分析\n({start_date} 至 {end_date})", 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("省份（城市）", fontsize=12, fontweight='bold')
    ax.set_ylabel("车辆(游客)数量", fontsize=12, fontweight='bold')
    
    # 设置X轴标签
    ax.set_xticks(range(len(locations)))
    ax.set_xticklabels(locations, rotation=45, ha='right')
    
    # 添加网格
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # 在柱子上方显示数值
    for i, (bar, count) in enumerate(zip(bars, counts)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 调整布局
    plt.tight_layout()
    
    # 转换为base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    
    return image_base64
