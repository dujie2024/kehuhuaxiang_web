import matplotlib.pyplot as plt
import mplcursors

def generate_chart(data, start_date, end_date, parking_lot, chart_type):
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    dates = [row[0] for row in data]
    vehicle_counts = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, vehicle_counts, marker='o', linestyle='-', color='b')
    plt.title(f"{parking_lot} - {chart_type}车辆（游客）客源地分析 ({start_date} 至 {end_date})")
    plt.xlabel("省份（城市）")
    plt.ylabel("车辆(游客)数量")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 添加悬停提示
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"{int(sel.target[1])}"))
    
    plt.show()