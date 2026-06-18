from .database import DatabaseModel
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class DzwlDataModel:
    """电子围栏客流数据模型"""
    
    def __init__(self):
        self.db = DatabaseModel(db_name='dzwl')
    
    def get_passenger_flow_data(self, start_date: str, end_date: str) -> List[Tuple]:
        """
        获取电子围栏客流数据
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
        
        Returns:
            List[Tuple]: [(日期, 进入累计, 离开累计), ...]
        """
        query = """
            SELECT 
                STR_TO_DATE(`joy_dzwl_tab_q2`.`日期`, '%%Y-%%m-%%d') AS `stat_date`,
                SUM(`joy_dzwl_tab_q2`.`进入累计`) AS `daily_enter_count`,
                SUM(`joy_dzwl_tab_q2`.`离开累计`) AS `daily_exit_count`
            FROM `joy_dzwl_tab_q2`
            WHERE STR_TO_DATE(`joy_dzwl_tab_q2`.`日期`, '%%Y-%%m-%%d') BETWEEN %s AND %s
            GROUP BY STR_TO_DATE(`joy_dzwl_tab_q2`.`日期`, '%%Y-%%m-%%d')
            ORDER BY `stat_date`
        """
        
        try:
            data = self.db.execute_query(query, (start_date, end_date))
            logger.info(f"电子围栏客流数据查询成功: {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"电子围栏客流数据查询失败: {e}")
            raise
    
    def get_total_statistics(self, start_date: str, end_date: str) -> dict:
        """
        获取时间段内的总体统计数据
        
        Returns:
            dict: {
                'total_enter': 总进入人数,
                'total_exit': 总离开人数,
                'avg_enter': 日均进入人数,
                'avg_exit': 日均离开人数,
                'days': 天数
            }
        """
        data = self.get_passenger_flow_data(start_date, end_date)
        
        if not data:
            return {
                'total_enter': 0,
                'total_exit': 0,
                'avg_enter': 0,
                'avg_exit': 0,
                'days': 0
            }
        
        total_enter = sum(row[1] for row in data)
        total_exit = sum(row[2] for row in data)
        days = len(data)
        
        return {
            'total_enter': total_enter,
            'total_exit': total_exit,
            'avg_enter': round(total_enter / days, 2) if days > 0 else 0,
            'avg_exit': round(total_exit / days, 2) if days > 0 else 0,
            'days': days
        }
