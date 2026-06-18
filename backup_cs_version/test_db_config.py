#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试数据库配置"""

from models.database import DatabaseModel

print("=== 测试数据库配置 ===\n")

print("1. Carpark 数据库配置:")
db1 = DatabaseModel(db_name='carpark')
print(f"   用户: {db1.db_config['user']}")
print(f"   主机: {db1.db_config['host']}")
print(f"   数据库: {db1.db_config['database']}")
print(f"   端口: {db1.db_config['port']}")

print("\n2. DZWL 数据库配置:")
db2 = DatabaseModel(db_name='dzwl')
print(f"   用户: {db2.db_config['user']}")
print(f"   主机: {db2.db_config['host']}")
print(f"   数据库: {db2.db_config['database']}")
print(f"   端口: {db2.db_config['port']}")

print("\n=== 配置验证完成 ===")
