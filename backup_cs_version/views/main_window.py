import customtkinter as ctk
from tkinter import messagebox
from version import get_version_string
from .parking_view import ParkingAnalysisView
from .booking_view import BookingAnalysisView
from .dzwl_view import DzwlAnalysisView


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title(f"新朝旅游客户画像分析系统 {get_version_string()}")
        self.root.geometry("1400x850")
        
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.current_view = None
        self.setup_ui()
    
    def setup_ui(self):
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        self.create_sidebar(main_container)
        self.create_content_area(main_container)
        
        self.show_parking_view()
    
    def create_sidebar(self, parent):
        sidebar = ctk.CTkFrame(parent, width=250, corner_radius=0, fg_color="#2b2b2b")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)
        
        ctk.CTkLabel(
            logo_frame,
            text="🚗",
            font=ctk.CTkFont(size=40)
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="新朝旅游",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            logo_frame,
            text="客户画像分析系统",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        ).pack()
        
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#404040")
        separator.pack(fill="x", padx=20, pady=20)
        
        menu_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=10)
        
        self.menu_buttons = {}
        
        self.create_menu_button(
            menu_frame,
            "parking",
            "📊 停车数据分析",
            self.show_parking_view,
            is_first=True
        )
        
        self.create_menu_button(
            menu_frame,
            "booking",
            "🎫 预订数据分析",
            self.show_booking_view
        )
        
        self.create_menu_button(
            menu_frame,
            "dzwl",
            "🔒 电子围栏客流",
            self.show_dzwl_view
        )
        
        self.create_menu_button(
            menu_frame,
            "report",
            "📈 数据报表",
            lambda: self.show_coming_soon("数据报表")
        )
        
        self.create_menu_button(
            menu_frame,
            "settings",
            "⚙️ 系统设置",
            lambda: self.show_coming_soon("系统设置")
        )
        
        footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=20)
        
        ctk.CTkLabel(
            footer_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color="#606060"
        ).pack()
    
    def create_menu_button(self, parent, key, text, command, is_first=False):
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=8,
            fg_color="transparent" if not is_first else "#1f77b4",
            hover_color="#404040",
            anchor="w",
            command=lambda: self.on_menu_click(key, command)
        )
        btn.pack(fill="x", pady=5, padx=10)
        self.menu_buttons[key] = btn
    
    def on_menu_click(self, key, command):
        for btn_key, btn in self.menu_buttons.items():
            if btn_key == key:
                btn.configure(fg_color="#1f77b4")
            else:
                btn.configure(fg_color="transparent")
        
        command()
    
    def create_content_area(self, parent):
        self.content_area = ctk.CTkFrame(parent, fg_color="#f5f5f5")
        self.content_area.pack(side="right", fill="both", expand=True)
    
    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_parking_view(self):
        self.clear_content_area()
        self.current_view = ParkingAnalysisView(self.content_area)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
    
    def show_booking_view(self):
        self.clear_content_area()
        self.current_view = BookingAnalysisView(self.content_area)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
    
    def show_dzwl_view(self):
        self.clear_content_area()
        self.current_view = DzwlAnalysisView(self.content_area)
        self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
    
    def show_coming_soon(self, feature_name):
        self.clear_content_area()
        
        coming_soon_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        coming_soon_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            coming_soon_frame,
            text="🚧",
            font=ctk.CTkFont(size=80)
        ).pack(pady=(100, 20))
        
        ctk.CTkLabel(
            coming_soon_frame,
            text=f"{feature_name}功能",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            coming_soon_frame,
            text="即将上线，敬请期待...",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack()
