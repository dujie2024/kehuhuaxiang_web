import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from controllers.booking_controller import BookingController


class BookingAnalysisView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = BookingController()
        self.current_result = None
        self.setup_ui()
    
    def setup_ui(self):
        header = ctk.CTkLabel(
            self,
            text="🎫 预订数据分析",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ff7f0e"
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
        
        ctk.CTkLabel(form_frame, text="项目选择:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(5, 8))
        self.project_var = ctk.StringVar(value=self.controller.get_projects()[0])
        project_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        project_frame.pack(fill="x", pady=(0, 15))
        for proj in self.controller.get_projects():
            ctk.CTkRadioButton(
                project_frame,
                text=proj,
                variable=self.project_var,
                value=proj,
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", pady=3)
        
        ctk.CTkLabel(form_frame, text="图表类型:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(10, 8))
        self.chart_type_var = ctk.StringVar(value=self.controller.get_chart_types()[0])
        chart_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        chart_frame.pack(fill="x", pady=(0, 15))
        for chart in self.controller.get_chart_types():
            ctk.CTkRadioButton(
                chart_frame,
                text=chart,
                variable=self.chart_type_var,
                value=chart,
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", pady=3)
        
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
                fg_color="#ff7f0e",
                hover_color="#e06d00"
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
            background='#ff7f0e',
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
            background='#ff7f0e',
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
            fg_color="#ff7f0e",
            hover_color="#e06d00"
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
        
        self.result_frame = ctk.CTkScrollableFrame(parent, fg_color="#f0f0f0")
        self.result_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.show_empty_state()
    
    def show_empty_state(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        empty_label = ctk.CTkLabel(
            self.result_frame,
            text="📋 暂无数据\n\n请设置查询参数后点击【查询数据】按钮",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        empty_label.pack(expand=True, pady=50)
    
    def query_data(self):
        project = self.project_var.get()
        chart_type = self.chart_type_var.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        
        result = self.controller.analyze_booking_data(
            project, chart_type, start_date, end_date
        )
        
        if result['success']:
            self.current_result = result
            self.display_result(result)
            self.result_label.configure(text=result['message'])
        else:
            messagebox.showerror("查询失败", result['message'])
            self.show_empty_state()
    
    def display_result(self, result):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        data = result['data']
        
        for idx, (location, count) in enumerate(data, 1):
            row_frame = ctk.CTkFrame(self.result_frame, fg_color="white", corner_radius=8)
            row_frame.pack(fill="x", pady=5, padx=5)
            
            rank_label = ctk.CTkLabel(
                row_frame,
                text=f"#{idx}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#ff7f0e",
                width=50
            )
            rank_label.pack(side="left", padx=10, pady=10)
            
            location_label = ctk.CTkLabel(
                row_frame,
                text=location,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            location_label.pack(side="left", fill="x", expand=True, padx=10)
            
            count_label = ctk.CTkLabel(
                row_frame,
                text=f"{int(count)} 人",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2ca02c"
            )
            count_label.pack(side="right", padx=15)
    
    def show_chart(self):
        if not self.current_result or not self.current_result['success']:
            messagebox.showwarning("提示", "请先查询数据")
            return
        
        self.controller.generate_chart(self.current_result)
