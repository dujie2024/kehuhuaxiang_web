import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import pymysql
from tkcalendar import DateEntry
import configparser
from chart_generator import generate_chart
import logging
import os

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
DB_CONFIG = {
    'host': config.get('database.carpark', 'host'),
    'user': config.get('database.carpark', 'user'),
    'password': config.get('database.carpark', 'password'),
    'database': config.get('database.carpark', 'database'),
    'port': config.getint('database.carpark', 'port')
}

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VehicleQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("新朝旅游客户画像分析系统")
        self.root.geometry("1200x800")
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
    
    def setup_ui(self):
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_container,
            text="🚗 新朝旅游客户画像分析系统",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True)
        
        left_panel = ctk.CTkFrame(content_frame, width=400)
        left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.create_parking_analysis_section(left_panel)
        self.create_booking_analysis_section(right_panel)
        
        self.create_help_section(main_container)
    
    def create_parking_analysis_section(self, parent):
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = ctk.CTkLabel(
            section_frame,
            text="📊 停车数据分析",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1f77b4"
        )
        header.pack(pady=(10, 20))
        
        form_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=15)
        
        ctk.CTkLabel(form_frame, text="停车场选择:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.parking_lot = ctk.CTkComboBox(
            form_frame,
            values=["天女小镇停车场", "欢乐湾停车场"],
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.parking_lot.set("天女小镇停车场")
        self.parking_lot.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="图表类型:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.chart_type = ctk.CTkComboBox(
            form_frame,
            values=["按省份", "按城市"],
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.chart_type.set("按省份")
        self.chart_type.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="开始日期:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.start_date_entry = DateEntry(
            form_frame,
            date_pattern="yyyy-mm-dd",
            font=("Microsoft YaHei", 12),
            background='#1f77b4',
            foreground='white',
            borderwidth=2
        )
        self.start_date_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="结束日期:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.end_date_entry = DateEntry(
            form_frame,
            date_pattern="yyyy-mm-dd",
            font=("Microsoft YaHei", 12),
            background='#1f77b4',
            foreground='white',
            borderwidth=2
        )
        self.end_date_entry.pack(fill="x", pady=(0, 20))
        
        query_btn = ctk.CTkButton(
            form_frame,
            text="🔍 开始分析",
            command=self.query_data,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10
        )
        query_btn.pack(fill="x", pady=(10, 10))
    
    def create_booking_analysis_section(self, parent):
        section_frame = ctk.CTkFrame(parent)
        section_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        header = ctk.CTkLabel(
            section_frame,
            text="🎫 预订数据分析",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff7f0e"
        )
        header.pack(pady=(10, 20))
        
        form_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=15)
        
        ctk.CTkLabel(form_frame, text="项目选择:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.project = ctk.CTkComboBox(
            form_frame,
            values=["祖山", "海上游船"],
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.project.set("祖山")
        self.project.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="图表类型:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.chart_type2 = ctk.CTkComboBox(
            form_frame,
            values=["手机号段", "实名制（省份）", "实名制(城市)"],
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.chart_type2.set("手机号段")
        self.chart_type2.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="开始日期:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.booking_start_date = DateEntry(
            form_frame,
            date_pattern='yyyy-mm-dd',
            font=("Microsoft YaHei", 12),
            background='#ff7f0e',
            foreground='white',
            borderwidth=2
        )
        self.booking_start_date.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="结束日期:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(5, 2))
        self.booking_end_date = DateEntry(
            form_frame,
            date_pattern='yyyy-mm-dd',
            font=("Microsoft YaHei", 12),
            background='#ff7f0e',
            foreground='white',
            borderwidth=2
        )
        self.booking_end_date.pack(fill="x", pady=(0, 20))
        
        query_btn = ctk.CTkButton(
            form_frame,
            text="🔍 开始分析",
            command=self.query_booking_data,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#ff7f0e",
            hover_color="#e06d00"
        )
        query_btn.pack(fill="x", pady=(10, 10))
    
    def create_help_section(self, parent):
        help_frame = ctk.CTkFrame(parent)
        help_frame.pack(fill="x", pady=(10, 0))
        
        help_text = """📌 数据说明：
• 停车数据：天女小镇东西停车场及欢乐湾一二层停车场2025年数据 (20250101-20251010)
• 订票数据：票务系统客人预订手机号及实名制信息 (20250101-20250820)

💡 操作说明：
1. 选择分析维度：停车数据或预订数据
2. 配置查询参数：停车场/项目、图表类型、日期范围
3. 点击"开始分析"按钮生成可视化图表
4. 支持多次查询和对比分析"""
        
        help_label = ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        help_label.pack(padx=15, pady=10, anchor="w")

    def query_data(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        parking_lot = self.parking_lot.get()
        chart_type = self.chart_type.get()
        
        if parking_lot == "天女小镇停车场":
            table_name = "tnxz_dx_vehicle_province_rank_byday" if chart_type == "按省份" else "tnxz_dx_vehicle_city_rank_byday"
        else:
            table_name = "hlw_vehicle_province_rank_byday" if chart_type == "按省份" else "hlw_vehicle_city_rank_byday"
        
        conn = None
        cursor = None
        try:
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            query = f"""
                SELECT a.location, SUM(a.vehicle_count) AS vehicle_count
                FROM `{table_name}` a
                WHERE a.`出场日期` BETWEEN %s AND %s
                GROUP BY a.location
                ORDER BY vehicle_count DESC
                LIMIT 10;
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
            
            if not data:
                messagebox.showinfo("提示", "未找到指定日期范围内的数据")
                return
            
            generate_chart(data, start_date, end_date, parking_lot, chart_type)
            logger.info(f"停车数据查询成功: {parking_lot} - {chart_type}")
            
        except ValueError:
            messagebox.showerror("错误", "日期格式应为 YYYY-MM-DD")
        except pymysql.Error as err:
            messagebox.showerror("数据库错误", f"错误: {err}")
            logger.error(f"数据库查询错误: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def query_booking_data(self):
        start_date = self.booking_start_date.get()
        end_date = self.booking_end_date.get()
        project = self.project.get()
        chart_type = self.chart_type2.get()
        
        conn = None
        cursor = None
        try:
            conn = pymysql.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            if project == "祖山":
                if chart_type == "手机号段":
                    table_name = "v_tel_city_zstickets_city_byday"
                elif chart_type == "实名制（省份）":
                    table_name = "v_idcard_province_zstickets_byday"
                else:
                    table_name = "v_idcard_city_zstickets_byday"
            else:
                table_name = "v_tel_city_yctickets_city_byday"
            
            query = f"""
                SELECT a.`所属城市` as location, SUM(a.total_count) AS booking_count
                FROM `{table_name}` a
                WHERE a.`操作时间` BETWEEN %s AND %s
                GROUP BY location
                ORDER BY booking_count DESC
                LIMIT 10;
            """
            cursor.execute(query, (start_date, end_date))
            data = cursor.fetchall()
            
            if not data:
                messagebox.showinfo("提示", "未找到指定日期范围内的数据")
                return
            
            generate_chart(data, start_date, end_date, project, chart_type)
            logger.info(f"预订数据查询成功: {project} - {chart_type}")
            
        except ValueError:
            messagebox.showerror("错误", "日期格式应为 YYYY-MM-DD")
        except pymysql.Error as err:
            messagebox.showerror("数据库错误", f"错误: {err}")
            logger.error(f"数据库查询错误: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


if __name__ == "__main__":
    try:
        root = ctk.CTk()
        app = VehicleQueryApp(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"程序运行时发生异常: {e}", exc_info=True)
        messagebox.showerror("错误", f"程序发生错误: {e}")