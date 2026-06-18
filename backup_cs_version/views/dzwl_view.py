import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from controllers.dzwl_controller import DzwlController


class DzwlAnalysisView(ctk.CTkFrame):
    """电子围栏客流分析视图"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = DzwlController()
        self.current_result = None
        self.setup_ui()
    
    def setup_ui(self):
        header = ctk.CTkLabel(
            self,
            text="🔒 电子围栏客流分析",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#9467bd"
        )
        header.pack(pady=(0, 20))
        
        content_container = ctk.CTkFrame(self)
        content_container.pack(fill="both", expand=True)
        
        left_panel = ctk.CTkFrame(content_container, width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        right_panel = ctk.CTkFrame(content_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        self.create_query_form(left_panel)
        self.create_result_area(right_panel)
    
    def create_query_form(self, parent):
        form_frame = ctk.CTkFrame(parent)
        form_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            form_frame, 
            text="查询参数设置", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0, 15))
        
        ctk.CTkLabel(
            form_frame,
            text="📌 数据说明",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#9467bd"
        ).pack(anchor="w", pady=(5, 5))
        
        info_text = "电子围栏系统记录景区\n进出人数的实时数据"
        ctk.CTkLabel(
            form_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            justify="left"
        ).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="快速日期选择:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 8))
        quick_date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        quick_date_frame.pack(fill="x", pady=(0, 10))
        
        quick_dates = [
            ("五一假期", "2025-05-01", "2025-05-05"),
            ("十一假期", "2025-10-01", "2025-10-07"),
            ("暑假", "2025-07-01", "2025-08-31")
        ]
        
        for idx, (label, start, end) in enumerate(quick_dates):
            btn = ctk.CTkButton(
                quick_date_frame,
                text=label,
                command=lambda s=start, e=end: self.set_quick_date(s, e),
                font=ctk.CTkFont(size=12),
                height=28,
                width=80,
                corner_radius=6,
                fg_color="#9467bd",
                hover_color="#7a52a0"
            )
            btn.grid(row=idx//2, column=idx%2, padx=5, pady=3, sticky="ew")
        
        quick_date_frame.grid_columnconfigure(0, weight=1)
        quick_date_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(form_frame, text="自定义日期范围:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 8))
        date_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_container.pack(fill="x", pady=(0, 20))
        
        date_left = ctk.CTkFrame(date_container, fg_color="transparent")
        date_left.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(date_left, text="开始:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.start_date = DateEntry(
            date_left,
            date_pattern="yyyy-mm-dd",
            font=("Microsoft YaHei", 11),
            background='#9467bd',
            foreground='white',
            borderwidth=2
        )
        self.start_date.pack(fill="x")
        
        date_right = ctk.CTkFrame(date_container, fg_color="transparent")
        date_right.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(date_right, text="结束:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.end_date = DateEntry(
            date_right,
            date_pattern="yyyy-mm-dd",
            font=("Microsoft YaHei", 11),
            background='#9467bd',
            foreground='white',
            borderwidth=2
        )
        self.end_date.pack(fill="x")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkButton(
            btn_frame,
            text="🔍 查询数据",
            command=self.query_data,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#9467bd",
            hover_color="#7a52a0"
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="📊 生成图表",
            command=self.show_chart,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#2ca02c",
            hover_color="#228b22"
        ).pack(fill="x")
    
    def set_quick_date(self, start_date, end_date):
        from datetime import datetime
        self.start_date.set_date(datetime.strptime(start_date, "%Y-%m-%d"))
        self.end_date.set_date(datetime.strptime(end_date, "%Y-%m-%d"))
    
    def create_result_area(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="查询结果",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.result_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.result_label.pack(side="right")
        
        self.stats_frame = ctk.CTkFrame(parent)
        self.stats_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.result_frame = ctk.CTkScrollableFrame(parent, fg_color="#f0f0f0")
        self.result_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.show_empty_state()
    
    def show_empty_state(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        empty_label = ctk.CTkLabel(
            self.result_frame,
            text="📋 暂无数据\n\n请设置查询参数后点击【查询数据】按钮",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        empty_label.pack(expand=True, pady=50)
    
    def query_data(self):
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        
        result = self.controller.analyze_passenger_flow(start_date, end_date)
        
        if result['success']:
            self.current_result = result
            self.display_statistics(result['statistics'])
            self.display_result(result)
            self.result_label.configure(text=result['message'])
        else:
            messagebox.showerror("查询失败", result['message'])
            self.show_empty_state()
    
    def display_statistics(self, stats):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats_container = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=10, pady=10)
        
        stat_items = [
            ("📅 统计天数", f"{stats['days']} 天", "#1f77b4"),
            ("📥 总进入", f"{int(stats['total_enter']):,} 人", "#2ca02c"),
            ("📤 总离开", f"{int(stats['total_exit']):,} 人", "#ff7f0e"),
            ("📊 日均进入", f"{stats['avg_enter']:,.0f} 人", "#9467bd")
        ]
        
        for idx, (label, value, color) in enumerate(stat_items):
            stat_card = ctk.CTkFrame(stats_container, fg_color="white", corner_radius=8)
            stat_card.grid(row=0, column=idx, padx=5, sticky="ew")
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(pady=(8, 2))
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(pady=(0, 8))
        
        for i in range(4):
            stats_container.grid_columnconfigure(i, weight=1)
    
    def display_result(self, result):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        data = result['data']
        
        for idx, (date, enter_count, exit_count) in enumerate(data, 1):
            row_frame = ctk.CTkFrame(self.result_frame, fg_color="white", corner_radius=8)
            row_frame.pack(fill="x", pady=5, padx=5)
            
            date_label = ctk.CTkLabel(
                row_frame,
                text=str(date),
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#9467bd",
                width=120
            )
            date_label.pack(side="left", padx=10, pady=10)
            
            enter_label = ctk.CTkLabel(
                row_frame,
                text=f"进入: {int(enter_count):,} 人",
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            enter_label.pack(side="left", fill="x", expand=True, padx=10)
            
            exit_label = ctk.CTkLabel(
                row_frame,
                text=f"离开: {int(exit_count):,} 人",
                font=ctk.CTkFont(size=13),
                text_color="#ff7f0e"
            )
            exit_label.pack(side="right", padx=15)
    
    def show_chart(self):
        if not self.current_result or not self.current_result['success']:
            messagebox.showwarning("提示", "请先查询数据")
            return
        
        self.controller.generate_flow_chart(self.current_result)
