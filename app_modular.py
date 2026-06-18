#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新朝旅游客户画像分析系统 - 模块化Web服务器
BS架构 - 使用Blueprint模块化设计
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import logging
import socket
from datetime import datetime
import os

from blueprints.parking_bp import parking_bp
from blueprints.booking_bp import booking_bp
from blueprints.dzwl_bp import dzwl_bp
from utils.logger_utils import setup_logger
from version import get_version_string

# 创建Flask应用
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

# 配置日志
logger = setup_logger('WebApp')

# 注册Blueprint模块
app.register_blueprint(parking_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(dzwl_bp)


@app.route('/')
def index():
    """主页 - 导航页面"""
    return render_template('index_modular.html', version=get_version_string())


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'message': 'Service is running',
        'version': get_version_string(),
        'modules': ['parking', 'booking', 'dzwl']
    })


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'message': '请求的资源不存在'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"服务器内部错误: {error}", exc_info=True)
    return jsonify({
        'success': False,
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info(get_version_string())
    logger.info("启动模块化Web服务器 - BS架构")
    logger.info("=" * 60)
    logger.info("已加载模块:")
    logger.info("  - 停车数据分析 (/parking)")
    logger.info("  - 预订数据分析 (/booking)")
    logger.info("  - 电子围栏客流 (/dzwl)")
    logger.info("=" * 60)
    
    # 获取本机IP地址
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    port = 80
    logger.info(f"本地访问地址: http://localhost:{port}")
    logger.info(f"局域网访问地址: http://{local_ip}:{port}")
    logger.info("=" * 60)
    logger.info("模块访问地址:")
    logger.info(f"  停车数据: http://localhost:{port}/parking")
    logger.info(f"  预订数据: http://localhost:{port}/booking")
    logger.info(f"  电子围栏: http://localhost:{port}/dzwl")
    logger.info("=" * 60)
    logger.info("按 Ctrl+C 停止服务器")
    
    # 启动服务器，监听所有网络接口以支持局域网访问
    app.run(host='0.0.0.0', port=port, debug=False)
