#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预订数据分析模块 - Blueprint
"""

from flask import Blueprint, render_template, jsonify, request
import logging
from controllers.booking_controller import BookingController
from utils.web_chart_utils import generate_web_chart

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')
logger = logging.getLogger(__name__)
controller = BookingController()


@booking_bp.route('/')
def index():
    """预订数据分析页面"""
    return render_template('booking.html')


@booking_bp.route('/api/options', methods=['GET'])
def get_options():
    """获取预订选项"""
    try:
        projects = controller.get_projects()
        chart_types = controller.get_chart_types()
        return jsonify({
            'success': True,
            'data': {
                'projects': projects,
                'chart_types': chart_types
            }
        })
    except Exception as e:
        logger.error(f"获取预订选项失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'获取选项失败: {str(e)}'
        }), 500


@booking_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """分析预订数据"""
    try:
        data = request.get_json()
        project = data.get('project')
        chart_type = data.get('chart_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        logger.info(f"预订数据分析请求 - 项目: {project}, 类型: {chart_type}, 日期: {start_date} ~ {end_date}")
        
        result = controller.analyze_booking_data(
            project, chart_type, start_date, end_date
        )
        
        if result['success']:
            logger.info(f"预订数据分析成功: {len(result['data'])} 条记录")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"预订数据分析失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500


@booking_bp.route('/api/chart', methods=['POST'])
def generate_chart():
    """生成预订数据图表"""
    try:
        data = request.get_json()
        chart_data = data.get('data')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        project = data.get('project')
        chart_type = data.get('chart_type')
        
        chart_base64 = generate_web_chart(
            chart_data, start_date, end_date, project, chart_type
        )
        
        return jsonify({
            'success': True,
            'chart': chart_base64
        })
    except Exception as e:
        logger.error(f"生成图表失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'生成图表失败: {str(e)}'
        }), 500
