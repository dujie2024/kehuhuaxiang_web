from models.booking_model import BookingDataModel
from utils.chart_utils import ChartGenerator
import logging

logger = logging.getLogger(__name__)


class BookingController:
    def __init__(self):
        self.model = BookingDataModel()
        self.chart_generator = ChartGenerator()
    
    def analyze_booking_data(self, project: str, chart_type: str,
                            start_date: str, end_date: str) -> dict:
        try:
            data = self.model.get_booking_data(
                project, chart_type, start_date, end_date
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
                    'project': project,
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
            logger.error(f"分析预订数据时出错: {e}")
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
                metadata['project'],
                metadata['chart_type']
            )
    
    def get_projects(self):
        return self.model.get_available_projects()
    
    def get_chart_types(self):
        return self.model.get_available_chart_types()
