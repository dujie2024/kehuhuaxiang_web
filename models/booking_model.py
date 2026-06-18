from .database import DatabaseModel
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class BookingDataModel:
    def __init__(self):
        self.db = DatabaseModel()
        
        self.table_mapping = {
            '祖山': {
                '手机号段': 'v_tel_city_zstickets_city_byday',
                '实名制（省份）': 'v_idcard_province_zstickets_byday',
                '实名制(城市)': 'v_idcard_city_zstickets_byday'
            },
            '海上游船': {
                '手机号段': 'v_tel_city_yctickets_city_byday',
                '实名制（省份）': 'v_tel_city_yctickets_city_byday',
                '实名制(城市)': 'v_tel_city_yctickets_city_byday'
            }
        }
    
    def get_booking_data(self, project: str, chart_type: str,
                        start_date: str, end_date: str, limit: int = 10) -> List[Tuple]:
        table_name = self.table_mapping.get(project, {}).get(chart_type)
        
        if not table_name:
            logger.error(f"无效的参数组合: {project} - {chart_type}")
            raise ValueError(f"无效的参数组合: {project} - {chart_type}")
        
        query = f"""
            SELECT a.`所属城市` as location, SUM(a.total_count) AS booking_count
            FROM `{table_name}` a
            WHERE a.`操作时间` BETWEEN %s AND %s
            GROUP BY location
            ORDER BY booking_count DESC
            LIMIT %s;
        """
        
        try:
            data = self.db.execute_query(query, (start_date, end_date, limit))
            logger.info(f"预订数据查询成功: {project} - {chart_type}, {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"预订数据查询失败: {e}")
            raise
    
    def get_available_projects(self) -> List[str]:
        return list(self.table_mapping.keys())
    
    def get_available_chart_types(self) -> List[str]:
        return ['手机号段', '实名制（省份）', '实名制(城市)']
