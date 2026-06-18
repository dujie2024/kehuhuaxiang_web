#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子围栏客流分析模块 - Blueprint
"""

from flask import Blueprint, render_template, jsonify, request
import logging
from controllers.dzwl_controller import DzwlController
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

dzwl_bp = Blueprint('dzwl', __name__, url_prefix='/dzwl')
logger = logging.getLogger(__name__)
controller = DzwlController()


@dzwl_bp.route('/')
def index():
    """电子围栏客流分析页面"""
    return render_template('dzwl.html')


@dzwl_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """分析电子围栏客流数据"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        logger.info(f"电子围栏客流分析请求 - 日期: {start_date} ~ {end_date}")
        
        result = controller.analyze_passenger_flow(start_date, end_date)
        
        if result['success']:
            logger.info(f"电子围栏客流分析成功: {len(result['data'])} 条记录")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"电子围栏客流分析失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500


@dzwl_bp.route('/api/chart', methods=['POST'])
def generate_chart():
    """生成电子围栏客流图表"""
    try:
        data = request.get_json()
        chart_data = data.get('data')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 提取数据
        dates = [str(row[0]) for row in chart_data]
        enter_counts = [row[1] for row in chart_data]
        exit_counts = [row[2] for row in chart_data]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 7))
        
        ax.plot(dates, enter_counts, marker='o', linestyle='-', 
                color='#2ca02c', linewidth=2.5, markersize=8, label='进入人数')
        ax.plot(dates, exit_counts, marker='s', linestyle='-', 
                color='#ff7f0e', linewidth=2.5, markersize=8, label='离开人数')
        
        ax.set_title(f"电子围栏客流趋势分析 ({start_date} 至 {end_date})", 
                    fontsize=18, fontweight='bold', pad=20)
        ax.set_xlabel("日期", fontsize=14, fontweight='bold')
        ax.set_ylabel("人数", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=13, loc='best')
        
        # 在数据点上显示数值
        for i, (date, enter, exit) in enumerate(zip(dates, enter_counts, exit_counts)):
            if i % max(1, len(dates) // 10) == 0:  # 避免标签过密
                ax.text(i, enter, f'{int(enter)}', ha='center', va='bottom', fontsize=9)
                ax.text(i, exit, f'{int(exit)}', ha='center', va='top', fontsize=9)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # 转换为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close(fig)
        
        return jsonify({
            'success': True,
            'chart': image_base64
        })
    except Exception as e:
        logger.error(f"生成图表失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'生成图表失败: {str(e)}'
        }), 500
