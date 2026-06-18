import matplotlib.pyplot as plt
import mplcursors
from typing import List, Tuple


class ChartGenerator:
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_chart(self, data: List[Tuple], start_date: str, end_date: str,
                      location: str, chart_type: str):
        if not data:
            return
        
        locations = [row[0] for row in data]
        counts = [row[1] for row in data]
        
        plt.figure(figsize=(12, 6))
        plt.plot(locations, counts, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
        plt.title(f"{location} - {chart_type}车辆（游客）客源地分析 ({start_date} 至 {end_date})", 
                 fontsize=16, fontweight='bold')
        plt.xlabel("省份（城市）", fontsize=12)
        plt.ylabel("车辆(游客)数量", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{int(sel.target[1])}"))
        
        plt.show()
    
    def generate_bar_chart(self, data: List[Tuple], title: str):
        if not data:
            return
        
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(labels, values, color='steelblue', alpha=0.8)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel("位置", fontsize=12)
        plt.ylabel("数量", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()
