#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询原始停车记录表结构
"""

import pymysql
import configparser

def get_db_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return {
        'host': config.get('database.carpark', 'host'),
        'user': config.get('database.carpark', 'user'),
        'password': config.get('database.carpark', 'password'),
        'database': config.get('database.carpark', 'database'),
        'port': config.getint('database.carpark', 'port'),
        'charset': 'utf8mb4'
    }

def execute_query(query):
    config = get_db_config()
    conn = pymysql.connect(**config)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()

print("=" * 100)
print("查询原始停车记录表结构")
print("=" * 100)

# 查询天女小镇原始记录表结构
print("\n1. 天女小镇原始记录表 (tnxz_dx_records_20250401_0820) 字段:")
print("-" * 100)

columns = execute_query("""
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        COLUMN_TYPE,
        IS_NULLABLE,
        COLUMN_KEY,
        COLUMN_COMMENT
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = 'carpark'
      AND TABLE_NAME = 'tnxz_dx_records_20250401_0820'
    ORDER BY ORDINAL_POSITION
""")

print(f"{'序号':<6} {'字段名':<30} {'数据类型':<20} {'可空':<8} {'键':<8} {'注释':<30}")
print("-" * 100)
for i, col in enumerate(columns, 1):
    print(f"{i:<6} {col[0]:<30} {col[1]:<20} {col[3]:<8} {col[4]:<8} {col[5] or '':<30}")

# 查看示例数据
print("\n2. 天女小镇原始记录表 - 示例数据 (前5条):")
print("-" * 100)

sample_data = execute_query("""
    SELECT * FROM tnxz_dx_records_20250401_0820 LIMIT 5
""")

if sample_data and len(sample_data) > 0:
    col_names = [col[0] for col in columns]
    print(" | ".join(col_names))
    print("-" * 100)
    for row in sample_data:
        print(" | ".join(str(val) if val is not None else 'NULL' for val in row))

# 统计信息
print("\n3. 数据统计:")
print("-" * 100)

stats = execute_query("""
    SELECT 
        COUNT(*) AS total_records,
        COUNT(DISTINCT `车牌号`) AS unique_plates
    FROM tnxz_dx_records_20250401_0820
""")

if stats:
    print(f"总记录数: {stats[0][0]:,}")
    print(f"唯一车牌数: {stats[0][1]:,}")

# 查询欢乐湾原始记录表结构
print("\n" + "=" * 100)
print("4. 欢乐湾原始记录表 (hlw_records_20250401_0820) 字段:")
print("-" * 100)

hlw_columns = execute_query("""
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        COLUMN_TYPE,
        COLUMN_COMMENT
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = 'carpark'
      AND TABLE_NAME = 'hlw_records_20250401_0820'
    ORDER BY ORDINAL_POSITION
""")

print(f"{'序号':<6} {'字段名':<30} {'数据类型':<20} {'注释':<30}")
print("-" * 100)
for i, col in enumerate(hlw_columns, 1):
    print(f"{i:<6} {col[0]:<30} {col[1]:<20} {col[3] or '':<30}")

# 欢乐湾示例数据
print("\n5. 欢乐湾原始记录表 - 示例数据 (前3条):")
print("-" * 100)

hlw_sample = execute_query("""
    SELECT * FROM hlw_records_20250401_0820 LIMIT 3
""")

if hlw_sample and len(hlw_sample) > 0:
    hlw_col_names = [col[0] for col in hlw_columns]
    print(" | ".join(hlw_col_names))
    print("-" * 100)
    for row in hlw_sample:
        print(" | ".join(str(val) if val is not None else 'NULL' for val in row))

print("\n" + "=" * 100)
print("查询完成！")
print("=" * 100)
