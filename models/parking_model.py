from .database import DatabaseModel
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class ParkingDataModel:
    def __init__(self):
        self.db = DatabaseModel()
        
        self.table_mapping = {
            '天女小镇停车场': {
                '按省份': 'tnxz_dx_vehicle_province_rank_byday',
                '按城市': 'tnxz_dx_vehicle_city_rank_byday',
                '驻留时长分析': 'tnxz_dx_records_20250401_0820'
            },
            '欢乐湾停车场': {
                '按省份': 'hlw_vehicle_province_rank_byday',
                '按城市': 'hlw_vehicle_city_rank_byday',
                '驻留时长分析': 'hlw_records_20250401_0820'
            }
        }
    
    def get_parking_data(self, parking_lot: str, chart_type: str, 
                        start_date: str, end_date: str, limit: int = 10) -> List[Tuple]:
        table_name = self.table_mapping.get(parking_lot, {}).get(chart_type)
        
        if not table_name:
            logger.error(f"无效的参数组合: {parking_lot} - {chart_type}")
            raise ValueError(f"无效的参数组合: {parking_lot} - {chart_type}")
        
        query = f"""
            SELECT a.location, SUM(a.vehicle_count) AS vehicle_count
            FROM `{table_name}` a
            WHERE a.`出场日期` BETWEEN %s AND %s
            GROUP BY a.location
            ORDER BY vehicle_count DESC
            LIMIT %s;
        """
        
        try:
            data = self.db.execute_query(query, (start_date, end_date, limit))
            logger.info(f"停车数据查询成功: {parking_lot} - {chart_type}, {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"停车数据查询失败: {e}")
            raise
    
    def get_available_parking_lots(self) -> List[str]:
        return list(self.table_mapping.keys())
    
    def get_available_chart_types(self) -> List[str]:
        return ['按省份', '按城市', '驻留时长分析']
    
    def get_duration_distribution(self, parking_lot: str, start_date: str, end_date: str) -> List[Tuple]:
        """
        获取驻留时长分布数据
        返回格式: [(时长区间, 车辆数量, 占比), ...]
        """
        table_name = self.table_mapping.get(parking_lot, {}).get('驻留时长分析')
        
        if not table_name:
            logger.error(f"无效的停车场: {parking_lot}")
            raise ValueError(f"无效的停车场: {parking_lot}")
        
        query = f"""
            SELECT 
                CASE 
                    WHEN TIMESTAMPDIFF(HOUR, `入场时间`, `出场时间`) < 2 THEN '0-2小时'
                    WHEN TIMESTAMPDIFF(HOUR, `入场时间`, `出场时间`) < 4 THEN '2-4小时'
                    WHEN TIMESTAMPDIFF(HOUR, `入场时间`, `出场时间`) < 8 THEN '4-8小时'
                    WHEN TIMESTAMPDIFF(HOUR, `入场时间`, `出场时间`) < 24 THEN '8-24小时'
                    ELSE '24小时以上'
                END AS duration_range,
                COUNT(*) AS vehicle_count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `{table_name}` WHERE v_out_date BETWEEN %s AND %s), 2) AS percentage
            FROM `{table_name}`
            WHERE v_out_date BETWEEN %s AND %s
            GROUP BY duration_range
            ORDER BY MIN(TIMESTAMPDIFF(HOUR, `入场时间`, `出场时间`))
        """
        
        try:
            data = self.db.execute_query(query, (start_date, end_date, start_date, end_date))
            logger.info(f"驻留时长分布查询成功: {parking_lot}, {len(data)} 个区间")
            return data
        except Exception as e:
            logger.error(f"驻留时长分布查询失败: {e}")
            raise
    
    def get_duration_by_province(self, parking_lot: str, start_date: str, end_date: str, limit: int = 20) -> List[Tuple]:
        """
        获取按省份统计的平均驻留时长
        返回格式: [(省份, 车辆数量, 平均驻留小时, 最长驻留小时), ...]
        """
        table_name = self.table_mapping.get(parking_lot, {}).get('驻留时长分析')
        
        if not table_name:
            logger.error(f"无效的停车场: {parking_lot}")
            raise ValueError(f"无效的停车场: {parking_lot}")
        
        query = f"""
            SELECT 
                v_province AS province,
                COUNT(*) AS vehicle_count,
                ROUND(AVG(TIMESTAMPDIFF(MINUTE, `入场时间`, `出场时间`) / 60.0), 2) AS avg_hours,
                ROUND(MAX(TIMESTAMPDIFF(MINUTE, `入场时间`, `出场时间`) / 60.0), 2) AS max_hours
            FROM `{table_name}`
            WHERE v_out_date BETWEEN %s AND %s
              AND v_province IS NOT NULL
              AND v_province != ''
            GROUP BY v_province
            ORDER BY avg_hours DESC
            LIMIT %s
        """
        
        try:
            data = self.db.execute_query(query, (start_date, end_date, limit))
            logger.info(f"省份驻留时长查询成功: {parking_lot}, {len(data)} 个省份")
            return data
        except Exception as e:
            logger.error(f"省份驻留时长查询失败: {e}")
            raise
    
    def get_duration_trend(self, parking_lot: str, start_date: str, end_date: str) -> List[Tuple]:
        """
        获取驻留时长趋势数据
        返回格式: [(日期, 车辆数量, 平均驻留小时), ...]
        """
        table_name = self.table_mapping.get(parking_lot, {}).get('驻留时长分析')
        
        if not table_name:
            logger.error(f"无效的停车场: {parking_lot}")
            raise ValueError(f"无效的停车场: {parking_lot}")
        
        query = f"""
            SELECT 
                v_out_date AS date,
                COUNT(*) AS vehicle_count,
                ROUND(AVG(TIMESTAMPDIFF(MINUTE, `入场时间`, `出场时间`) / 60.0), 2) AS avg_hours
            FROM `{table_name}`
            WHERE v_out_date BETWEEN %s AND %s
            GROUP BY v_out_date
            ORDER BY v_out_date
        """
        
        try:
            data = self.db.execute_query(query, (start_date, end_date))
            logger.info(f"驻留时长趋势查询成功: {parking_lot}, {len(data)} 天")
            return data
        except Exception as e:
            logger.error(f"驻留时长趋势查询失败: {e}")
            raise
