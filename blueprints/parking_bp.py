#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
停车数据分析模块 - Blueprint
"""

from flask import Blueprint, render_template, jsonify, request
import logging
from controllers.parking_controller import ParkingController
from utils.web_chart_utils import generate_web_chart

parking_bp = Blueprint('parking', __name__, url_prefix='/parking')
logger = logging.getLogger(__name__)
controller = ParkingController()


@parking_bp.route('/')
def index():
    """停车数据分析页面"""
    return render_template('parking.html')


@parking_bp.route('/api/options', methods=['GET'])
def get_options():
    """获取停车场选项"""
    try:
        parking_lots = controller.get_parking_lots()
        chart_types = controller.get_chart_types()
        return jsonify({
            'success': True,
            'data': {
                'parking_lots': parking_lots,
                'chart_types': chart_types
            }
        })
    except Exception as e:
        logger.error(f"获取停车场选项失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'获取选项失败: {str(e)}'
        }), 500


@parking_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """分析停车数据"""
    try:
        data = request.get_json()
        parking_lot = data.get('parking_lot')
        chart_type = data.get('chart_type')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        logger.info(f"停车数据分析请求 - 停车场: {parking_lot}, 类型: {chart_type}, 日期: {start_date} ~ {end_date}")
        
        result = controller.analyze_parking_data(
            parking_lot, chart_type, start_date, end_date
        )
        
        if result['success']:
            logger.info(f"停车数据分析成功: {len(result['data'])} 条记录")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"停车数据分析失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500


@parking_bp.route('/api/chart', methods=['POST'])
def generate_chart():
    """生成停车数据图表"""
    try:
        data = request.get_json()
        chart_data = data.get('data')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        parking_lot = data.get('parking_lot')
        chart_type = data.get('chart_type')
        
        chart_base64 = generate_web_chart(
            chart_data, start_date, end_date, parking_lot, chart_type
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


@parking_bp.route('/api/duration', methods=['POST'])
def analyze_duration():
    """分析车辆驻留时长"""
    try:
        data = request.get_json()
        parking_lot = data.get('parking_lot')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        logger.info(f"驻留时长分析请求 - 停车场: {parking_lot}, 日期: {start_date} ~ {end_date}")
        
        result = controller.analyze_duration(parking_lot, start_date, end_date)
        
        if result['success']:
            logger.info(f"驻留时长分析成功")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"驻留时长分析失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500
