#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询停车数据表结构
用于了解字段信息，设计驻留时长分析方案
"""

import pymysql
import configparser
from typing import List, Dict

def get_db_config():
    """读取数据库配置"""
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

def execute_query(query: str) -> List:
    """执行查询"""
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

def print_separator(title: str):
    """打印分隔线"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def main():
    print("开始查询停车数据表结构...\n")
    
    # 1. 查看所有停车相关的表
    print_separator("1. 所有停车相关的表")
    tables = execute_query("SHOW TABLES LIKE '%vehicle%'")
    print(f"找到 {len(tables)} 个包含'vehicle'的表:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # 2. 查看天女小镇省份表结构
    print_separator("2. 天女小镇省份表 (tnxz_dx_vehicle_province_rank_byday) 结构")
    columns = execute_query("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_KEY,
            COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'carpark'
          AND TABLE_NAME = 'tnxz_dx_vehicle_province_rank_byday'
        ORDER BY ORDINAL_POSITION
    """)
    
    print(f"\n字段列表 (共 {len(columns)} 个字段):")
    print(f"{'字段名':<30} {'类型':<15} {'可空':<8} {'键':<8} {'注释':<20}")
    print("-" * 90)
    for col in columns:
        print(f"{col[0]:<30} {col[1]:<15} {col[2]:<8} {col[3]:<8} {col[4] or '':<20}")
    
    # 3. 查看示例数据
    print_separator("3. 天女小镇省份表 - 示例数据 (前3条)")
    sample_data = execute_query("""
        SELECT * FROM tnxz_dx_vehicle_province_rank_byday LIMIT 3
    """)
    
    if sample_data:
        # 获取列名
        col_names = [col[0] for col in columns]
        print("\n列名:", " | ".join(col_names))
        print("-" * 120)
        for row in sample_data:
            print(" | ".join(str(val) for val in row))
    
    # 4. 查看天女小镇城市表结构
    print_separator("4. 天女小镇城市表 (tnxz_dx_vehicle_city_rank_byday) 结构")
    city_columns = execute_query("""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'carpark'
          AND TABLE_NAME = 'tnxz_dx_vehicle_city_rank_byday'
        ORDER BY ORDINAL_POSITION
    """)
    
    print(f"\n字段列表 (共 {len(city_columns)} 个字段):")
    for col in city_columns:
        print(f"  - {col[0]:<30} ({col[1]:<15}) {col[2] or ''}")
    
    # 5. 查找所有包含时间相关的字段
    print_separator("5. 查找所有时间相关字段")
    time_fields = execute_query("""
        SELECT 
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'carpark'
          AND TABLE_NAME LIKE '%vehicle%'
          AND (
            COLUMN_NAME LIKE '%时间%' 
            OR COLUMN_NAME LIKE '%time%'
            OR COLUMN_NAME LIKE '%日期%'
            OR COLUMN_NAME LIKE '%date%'
            OR COLUMN_NAME LIKE '%入场%'
            OR COLUMN_NAME LIKE '%出场%'
            OR COLUMN_NAME LIKE '%驻留%'
            OR COLUMN_NAME LIKE '%停留%'
            OR COLUMN_NAME LIKE '%duration%'
          )
        ORDER BY TABLE_NAME, COLUMN_NAME
    """)
    
    if time_fields:
        print(f"\n找到 {len(time_fields)} 个时间相关字段:")
        print(f"{'表名':<40} {'字段名':<25} {'类型':<15} {'注释':<20}")
        print("-" * 100)
        for field in time_fields:
            print(f"{field[0]:<40} {field[1]:<25} {field[2]:<15} {field[3] or '':<20}")
    else:
        print("\n[提示] 未找到时间相关字段")
    
    # 6. 查找是否有车牌号字段
    print_separator("6. 查找车牌号相关字段")
    plate_fields = execute_query("""
        SELECT 
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'carpark'
          AND (
            COLUMN_NAME LIKE '%车牌%'
            OR COLUMN_NAME LIKE '%plate%'
            OR COLUMN_NAME LIKE '%license%'
            OR COLUMN_NAME LIKE '%vehicle_id%'
          )
    """)
    
    if plate_fields:
        print(f"\n找到 {len(plate_fields)} 个车牌相关字段:")
        for field in plate_fields:
            print(f"  - {field[0]}.{field[1]} ({field[2]})")
    else:
        print("\n[提示] 未找到车牌号字段")
    
    # 7. 查看所有表
    print_separator("7. carpark数据库中的所有表")
    all_tables = execute_query("SHOW TABLES")
    print(f"\n共 {len(all_tables)} 个表:")
    for i, table in enumerate(all_tables, 1):
        print(f"  {i:2d}. {table[0]}")
    
    # 8. 数据量统计
    print_separator("8. 数据量和日期范围")
    
    tables_to_check = [
        'tnxz_dx_vehicle_province_rank_byday',
        'tnxz_dx_vehicle_city_rank_byday',
        'hlw_vehicle_province_rank_byday',
        'hlw_vehicle_city_rank_byday'
    ]
    
    for table in tables_to_check:
        try:
            stats = execute_query(f"""
                SELECT 
                    COUNT(*) AS total_records,
                    MIN(`出场日期`) AS earliest_date,
                    MAX(`出场日期`) AS latest_date
                FROM {table}
            """)
            if stats:
                print(f"\n[统计] {table}:")
                print(f"   总记录数: {stats[0][0]:,}")
                print(f"   日期范围: {stats[0][1]} ~ {stats[0][2]}")
        except Exception as e:
            print(f"\n[错误] {table}: 查询失败 - {e}")
    
    print("\n" + "=" * 80)
    print("[完成] 查询完成！")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
