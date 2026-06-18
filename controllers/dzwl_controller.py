from models.dzwl_model import DzwlDataModel
from utils.chart_utils import ChartGenerator
import logging

logger = logging.getLogger(__name__)


class DzwlController:
    """电子围栏客流控制器"""
    
    def __init__(self):
        self.model = DzwlDataModel()
        self.chart_generator = ChartGenerator()
    
    def analyze_passenger_flow(self, start_date: str, end_date: str) -> dict:
        """
        分析电子围栏客流数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            dict: {
                'success': bool,
                'message': str,
                'data': list,
                'statistics': dict,
                'metadata': dict
            }
        """
        try:
            data = self.model.get_passenger_flow_data(start_date, end_date)
            
            if not data:
                return {
                    'success': False,
                    'message': '未找到指定日期范围内的数据',
                    'data': [],
                    'statistics': {}
                }
            
            statistics = self.model.get_total_statistics(start_date, end_date)
            
            return {
                'success': True,
                'message': f'成功获取 {len(data)} 条记录',
                'data': data,
                'statistics': statistics,
                'metadata': {
                    'start_date': start_date,
                    'end_date': end_date
                }
            }
        except ValueError as e:
            logger.error(f"参数错误: {e}")
            return {
                'success': False,
                'message': str(e),
                'data': [],
                'statistics': {}
            }
        except Exception as e:
            logger.error(f"分析电子围栏客流数据时出错: {e}")
            return {
                'success': False,
                'message': f'数据查询失败: {str(e)}',
                'data': [],
                'statistics': {}
            }
    
    def generate_flow_chart(self, result: dict):
        """生成客流趋势图表"""
        if not result['success'] or not result['data']:
            return
        
        import matplotlib.pyplot as plt
        import mplcursors
        
        data = result['data']
        dates = [str(row[0]) for row in data]
        enter_counts = [row[1] for row in data]
        exit_counts = [row[2] for row in data]
        
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        ax.plot(dates, enter_counts, marker='o', linestyle='-', 
                color='#1f77b4', linewidth=2, markersize=6, label='进入人数')
        ax.plot(dates, exit_counts, marker='s', linestyle='-', 
                color='#ff7f0e', linewidth=2, markersize=6, label='离开人数')
        
        metadata = result['metadata']
        ax.set_title(f"电子围栏客流趋势分析 ({metadata['start_date']} 至 {metadata['end_date']})", 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel("日期", fontsize=12)
        ax.set_ylabel("人数", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{int(sel.target[1])}人"))
        
        plt.show()
