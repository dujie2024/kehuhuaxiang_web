#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试车辆驻留时长分析功能
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:80"

def test_duration_analysis():
    """测试驻留时长分析API"""
    
    print("=" * 80)
    print("测试车辆驻留时长分析功能")
    print("=" * 80)
    
    # 测试场景1：五一假期
    test_cases = [
        {
            "name": "五一假期 - 天女小镇停车场",
            "parking_lot": "天女小镇停车场",
            "start_date": "2025-05-01",
            "end_date": "2025-05-05"
        },
        {
            "name": "五一假期 - 欢乐湾停车场",
            "parking_lot": "欢乐湾停车场",
            "start_date": "2025-05-01",
            "end_date": "2025-05-05"
        },
        {
            "name": "8月数据 - 天女小镇停车场",
            "parking_lot": "天女小镇停车场",
            "start_date": "2025-08-01",
            "end_date": "2025-08-20"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"测试场景 {i}: {test_case['name']}")
        print(f"{'=' * 80}")
        print(f"停车场: {test_case['parking_lot']}")
        print(f"日期范围: {test_case['start_date']} ~ {test_case['end_date']}")
        
        # 发送请求
        url = f"{BASE_URL}/parking/api/duration"
        payload = {
            "parking_lot": test_case['parking_lot'],
            "start_date": test_case['start_date'],
            "end_date": test_case['end_date']
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            if result['success']:
                print(f"\n✅ 查询成功！")
                
                # 1. 驻留时长分布
                print(f"\n📊 驻留时长分布:")
                print(f"{'时长区间':<15} {'车辆数量':<12} {'占比':<10}")
                print("-" * 40)
                for item in result['distribution']:
                    range_name = item[0]
                    count = item[1]
                    percentage = item[2]
                    print(f"{range_name:<15} {count:<12} {percentage}%")
                
                # 2. 省份驻留时长对比
                if result['province_comparison']:
                    print(f"\n🗺️ 各省份平均驻留时长 (Top 10):")
                    print(f"{'排名':<6} {'省份':<12} {'车辆数':<10} {'平均时长':<12} {'最长时长':<12}")
                    print("-" * 60)
                    for idx, item in enumerate(result['province_comparison'], 1):
                        province = item[0]
                        count = item[1]
                        avg_hours = item[2]
                        max_hours = item[3]
                        print(f"#{idx:<5} {province:<12} {count:<10} {avg_hours} 小时{'':<5} {max_hours} 小时")
                
                # 3. 驻留时长趋势
                if result['trend']:
                    print(f"\n📈 驻留时长趋势 (前5天):")
                    print(f"{'日期':<15} {'车辆数':<10} {'平均时长':<12}")
                    print("-" * 40)
                    for item in result['trend'][:5]:
                        date = item[0]
                        count = item[1]
                        avg_hours = item[2]
                        print(f"{date:<15} {count:<10} {avg_hours} 小时")
                    
                    if len(result['trend']) > 5:
                        print(f"... 共 {len(result['trend'])} 天数据")
                
                # 统计摘要
                total_vehicles = sum(item[1] for item in result['distribution'])
                print(f"\n📊 统计摘要:")
                print(f"   总车辆数: {total_vehicles:,} 辆")
                print(f"   分析天数: {len(result['trend'])} 天")
                print(f"   涉及省份: {len(result['province_comparison'])} 个")
                
            else:
                print(f"\n❌ 查询失败: {result['message']}")
                
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 网络请求失败: {e}")
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
    
    print(f"\n{'=' * 80}")
    print("测试完成！")
    print(f"{'=' * 80}")

def test_options_api():
    """测试选项API，验证驻留时长分析是否在列表中"""
    print("\n" + "=" * 80)
    print("测试选项API - 验证驻留时长分析选项")
    print("=" * 80)
    
    url = f"{BASE_URL}/parking/api/options"
    
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result['success']:
            print("\n✅ 选项API正常")
            print(f"\n停车场选项: {result['data']['parking_lots']}")
            print(f"图表类型: {result['data']['chart_types']}")
            
            if '驻留时长分析' in result['data']['chart_types']:
                print("\n✅ '驻留时长分析' 选项已成功添加！")
            else:
                print("\n❌ 未找到'驻留时长分析'选项")
        else:
            print(f"\n❌ 选项API失败: {result['message']}")
            
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    # 测试选项API
    test_options_api()
    
    # 测试驻留时长分析
    test_duration_analysis()
