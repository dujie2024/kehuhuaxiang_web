from models.parking_model import ParkingDataModel
from utils.chart_utils import ChartGenerator
import logging

logger = logging.getLogger(__name__)


class ParkingController:
    def __init__(self):
        self.model = ParkingDataModel()
        self.chart_generator = ChartGenerator()
    
    def analyze_parking_data(self, parking_lot: str, chart_type: str,
                            start_date: str, end_date: str) -> dict:
        try:
            data = self.model.get_parking_data(
                parking_lot, chart_type, start_date, end_date
            )
            
            if not data:
                return {
                    'success': False,
                    'message': '未找到指定日期范围内的数据',
                    'data': []
                }
            
            return {
                'success': True,
                'message': f'成功获取 {len(data)} 条记录',
                'data': data,
                'metadata': {
                    'parking_lot': parking_lot,
                    'chart_type': chart_type,
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
        except ValueError as e:
            logger.error(f"参数错误: {e}")
            return {
                'success': False,
                'message': str(e),
                'data': []
            }
        except Exception as e:
            logger.error(f"分析停车数据时出错: {e}")
            return {
                'success': False,
                'message': f'数据查询失败: {str(e)}',
                'data': []
            }
    
    def generate_chart(self, result: dict):
        if result['success'] and result['data']:
            metadata = result['metadata']
            self.chart_generator.generate_chart(
                result['data'],
                metadata['start_date'],
                metadata['end_date'],
                metadata['parking_lot'],
                metadata['chart_type']
            )
    
    def get_parking_lots(self):
        return self.model.get_available_parking_lots()
    
    def get_chart_types(self):
        return self.model.get_available_chart_types()
    
    def analyze_duration(self, parking_lot: str, start_date: str, end_date: str) -> dict:
        """
        分析车辆驻留时长
        返回：时长分布、省份对比、趋势数据
        """
        try:
            # 获取时长分布数据
            distribution = self.model.get_duration_distribution(parking_lot, start_date, end_date)
            
            # 获取省份驻留时长对比
            province_data = self.model.get_duration_by_province(parking_lot, start_date, end_date, limit=20)
            
            # 获取趋势数据
            trend_data = self.model.get_duration_trend(parking_lot, start_date, end_date)
            
            if not distribution and not province_data:
                return {
                    'success': False,
                    'message': '未找到指定日期范围内的数据',
                    'distribution': [],
                    'province_comparison': [],
                    'trend': []
                }
            
            return {
                'success': True,
                'message': f'成功获取驻留时长分析数据',
                'distribution': distribution,
                'province_comparison': province_data,
                'trend': trend_data,
                'metadata': {
                    'parking_lot': parking_lot,
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
        except ValueError as e:
            logger.error(f"参数错误: {e}")
            return {
                'success': False,
                'message': str(e),
                'distribution': [],
                'province_comparison': [],
                'trend': []
            }
        except Exception as e:
            logger.error(f"分析驻留时长时出错: {e}")
            return {
                'success': False,
                'message': f'数据查询失败: {str(e)}',
                'distribution': [],
                'province_comparison': [],
                'trend': []
            }
