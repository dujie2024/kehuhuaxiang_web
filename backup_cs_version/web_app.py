#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新朝旅游客户画像分析系统 - Web服务器
BS架构主程序
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
import os
import json
import base64
from io import BytesIO

from controllers.parking_controller import ParkingController
from controllers.booking_controller import BookingController
from controllers.dzwl_controller import DzwlController
from utils.logger_utils import setup_logger
from utils.web_chart_utils import generate_web_chart
from version import get_version_string

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

logger = setup_logger('WebApp')

parking_controller = ParkingController()
booking_controller = BookingController()
dzwl_controller = DzwlController()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html', version=get_version_string())


@app.route('/api/parking/options', methods=['GET'])
def get_parking_options():
    """获取停车场选项"""
    try:
        parking_lots = ["天女小镇停车场", "欢乐湾停车场"]
        chart_types = ["按省份", "按城市"]
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


@app.route('/api/parking/analyze', methods=['POST'])
def analyze_parking():
    """分析停车数据"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        parking_lot = data.get('parking_lot')
        chart_type = data.get('chart_type')
        
        logger.info(f"收到停车数据分析请求 - 停车场: {parking_lot}, 图表类型: {chart_type}, 日期: {start_date} 至 {end_date}")
        
        result = parking_controller.analyze_parking_data(
            parking_lot, chart_type, start_date, end_date
        )
        
        if result['success']:
            logger.info(f"停车数据分析成功: {parking_lot} - {chart_type}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"停车数据分析失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500


@app.route('/api/parking/chart', methods=['POST'])
def generate_parking_chart():
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


@app.route('/api/booking/options', methods=['GET'])
def get_booking_options():
    """获取预订选项"""
    try:
        projects = ["祖山", "海上游船"]
        chart_types = ["手机号段", "实名制（省份）", "实名制(城市)"]
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


@app.route('/api/booking/analyze', methods=['POST'])
def analyze_booking():
    """分析预订数据"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        project = data.get('project')
        chart_type = data.get('chart_type')
        
        result = booking_controller.analyze_booking_data(
            project, chart_type, start_date, end_date
        )
        
        if result['success']:
            logger.info(f"预订数据分析成功: {project} - {chart_type}")
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"预订数据分析失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500


@app.route('/api/booking/chart', methods=['POST'])
def generate_booking_chart():
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


@app.route('/api/dzwl/options', methods=['GET'])
def get_dzwl_options():
    """获取电子围栏选项"""
    try:
        fence_types = ["围栏1", "围栏2", "围栏3"]
        return jsonify({
            'success': True,
            'data': {
                'fence_types': fence_types
            }
        })
    except Exception as e:
        logger.error(f"获取电子围栏选项失败: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'获取选项失败: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'message': 'Service is running',
        'version': get_version_string()
    })


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info(get_version_string())
    logger.info("启动Web服务器 - BS架构")
    logger.info("=" * 60)
    
    # 获取本机IP地址
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    port = 5000
    logger.info(f"本地访问地址: http://localhost:{port}")
    logger.info(f"局域网访问地址: http://{local_ip}:{port}")
    logger.info("按 Ctrl+C 停止服务器")
    
    # 启动服务器，监听所有网络接口以支持局域网访问
    app.run(host='0.0.0.0', port=port, debug=False)
