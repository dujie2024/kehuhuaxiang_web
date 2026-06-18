# 新朝旅游客户画像分析系统 - 架构说明

## 📁 项目结构

```
carpark/
├── models/                 # 数据模型层 (Model)
│   ├── __init__.py
│   ├── database.py        # 数据库基础类
│   ├── parking_model.py   # 停车数据模型
│   └── booking_model.py   # 预订数据模型
│
├── views/                  # 视图层 (View)
│   ├── __init__.py
│   ├── main_window.py     # 主窗口 - 侧边栏导航
│   ├── parking_view.py    # 停车数据分析视图
│   └── booking_view.py    # 预订数据分析视图
│
├── controllers/            # 控制器层 (Controller)
│   ├── __init__.py
│   ├── parking_controller.py  # 停车数据控制器
│   └── booking_controller.py  # 预订数据控制器
│
├── utils/                  # 工具类
│   ├── __init__.py
│   ├── chart_utils.py     # 图表生成工具
│   └── logger_utils.py    # 日志工具
│
├── logs/                   # 日志目录
├── config.ini             # 数据库配置
├── app.py                 # 应用入口
├── requirements.txt       # 依赖列表
└── README_ARCHITECTURE.md # 本文档
```

## 🏗️ MVC 架构设计

### Model 层 (数据模型)
**职责**: 数据访问和业务数据管理

- `database.py`: 数据库连接和查询基础类
  - `DatabaseModel.execute_query()`: 执行 SQL 查询
  - `DatabaseModel.test_connection()`: 测试数据库连接

- `parking_model.py`: 停车数据模型
  - `get_parking_data()`: 查询停车数据
  - `get_available_parking_lots()`: 获取可用停车场列表
  - `get_available_chart_types()`: 获取可用图表类型

- `booking_model.py`: 预订数据模型
  - `get_booking_data()`: 查询预订数据
  - `get_available_projects()`: 获取可用项目列表
  - `get_available_chart_types()`: 获取可用图表类型

### Controller 层 (控制器)
**职责**: 业务逻辑处理,连接 Model 和 View

- `parking_controller.py`: 停车数据控制器
  - `analyze_parking_data()`: 分析停车数据,返回统一格式结果
  - `generate_chart()`: 生成图表
  - 数据验证和错误处理

- `booking_controller.py`: 预订数据控制器
  - `analyze_booking_data()`: 分析预订数据
  - `generate_chart()`: 生成图表
  - 数据验证和错误处理

### View 层 (视图)
**职责**: 用户界面展示和交互

- `main_window.py`: 主窗口
  - 侧边栏导航菜单
  - 内容区域切换
  - 菜单激活状态管理

- `parking_view.py`: 停车数据分析视图
  - 查询表单
  - 数据结果展示(卡片列表)
  - 图表生成按钮

- `booking_view.py`: 预订数据分析视图
  - 查询表单
  - 数据结果展示(卡片列表)
  - 图表生成按钮

## 🎨 界面设计 - BS 结构风格

### 侧边栏导航 (Sidebar Navigation)
```
┌─────────────────┬──────────────────────────────┐
│   🚗 新朝旅游    │                              │
│  客户画像分析系统 │                              │
│─────────────────│                              │
│ 📊 停车数据分析  │        内容区域               │
│ 🎫 预订数据分析  │    (动态切换显示)             │
│ 📈 数据报表     │                              │
│ ⚙️ 系统设置     │                              │
│                 │                              │
│      v1.0.0     │                              │
└─────────────────┴──────────────────────────────┘
```

### 内容区域布局
```
┌──────────────────────────────────────────────┐
│  📊 停车数据分析                              │
├──────────────┬───────────────────────────────┤
│  查询参数设置  │      查询结果                 │
│              │                               │
│ 停车场: [▼]  │  #1  北京市    1234 辆        │
│ 图表类型:[▼] │  #2  河北省     987 辆        │
│ 开始日期:[📅]│  #3  天津市     756 辆        │
│ 结束日期:[📅]│  ...                          │
│              │                               │
│ [🔍 查询数据] │                               │
│ [📊 生成图表] │                               │
└──────────────┴───────────────────────────────┘
```

## 🔄 数据流程

### 查询流程
```
用户操作 → View → Controller → Model → Database
                    ↓
                 验证参数
                    ↓
                 处理数据
                    ↓
View ← Controller ← 返回结果
  ↓
展示数据
```

### 具体示例 (停车数据查询)
1. **用户操作**: 在 `ParkingAnalysisView` 中点击"查询数据"
2. **View 层**: 收集表单参数,调用 `controller.analyze_parking_data()`
3. **Controller 层**: 
   - 验证参数
   - 调用 `model.get_parking_data()`
   - 处理返回结果,统一格式
4. **Model 层**: 
   - 根据参数选择表名
   - 执行 SQL 查询
   - 返回原始数据
5. **Controller 层**: 返回包含 success/message/data 的字典
6. **View 层**: 根据结果展示数据或错误信息

## 🎯 核心特性

### 1. 分离关注点
- **数据库逻辑**: 完全封装在 Model 层
- **业务逻辑**: 集中在 Controller 层
- **界面逻辑**: 独立在 View 层

### 2. 侧边栏导航
- 类似 BS 架构的左侧菜单
- 点击菜单项切换内容区域
- 菜单激活状态高亮显示

### 3. 数据展示优化
- **主界面展示**: 卡片列表形式,清晰直观
- **图表展示**: 独立窗口,支持交互
- **空状态提示**: 友好的用户引导

### 4. 统一的数据格式
Controller 返回统一格式:
```python
{
    'success': True/False,
    'message': '提示信息',
    'data': [...],
    'metadata': {...}
}
```

## 🔧 扩展指南

### 添加新功能模块

**1. 创建 Model**
```python
# models/new_model.py
from .database import DatabaseModel

class NewDataModel:
    def __init__(self):
        self.db = DatabaseModel()
    
    def get_data(self, params):
        query = "SELECT ..."
        return self.db.execute_query(query, params)
```

**2. 创建 Controller**
```python
# controllers/new_controller.py
from models.new_model import NewDataModel

class NewController:
    def __init__(self):
        self.model = NewDataModel()
    
    def analyze_data(self, params):
        data = self.model.get_data(params)
        return {
            'success': True,
            'data': data,
            'message': '查询成功'
        }
```

**3. 创建 View**
```python
# views/new_view.py
import customtkinter as ctk
from controllers.new_controller import NewController

class NewAnalysisView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.controller = NewController()
        self.setup_ui()
```

**4. 在主窗口添加菜单**
```python
# views/main_window.py
self.create_menu_button(
    menu_frame,
    "new_feature",
    "🆕 新功能",
    self.show_new_view
)

def show_new_view(self):
    self.clear_content_area()
    self.current_view = NewAnalysisView(self.content_area)
    self.current_view.pack(fill="both", expand=True, padx=20, pady=20)
```

### 修改数据库配置
编辑 `config.ini`:
```ini
[database]
host = 你的主机
user = 用户名
password = 密码
database = 数据库名
port = 3306
```

### 自定义主题颜色
在 `main_window.py` 中修改:
```python
ctk.set_default_color_theme("blue")  # blue, green, dark-blue
ctk.set_appearance_mode("light")     # light, dark, system
```

## 📊 数据展示方案

### 当前实现
- **主界面**: 排名卡片列表
  - 显示排名、位置、数量
  - 滚动查看所有结果
  - 清晰的视觉层次

- **图表窗口**: 独立 Matplotlib 窗口
  - 折线图展示趋势
  - 悬停显示数值
  - 支持缩放和保存

### 未来优化方向
1. **内嵌图表**: 在主界面右侧嵌入图表
2. **多种图表**: 柱状图、饼图、热力图
3. **数据导出**: Excel、PDF 报表
4. **实时刷新**: 定时自动更新数据

## 🚀 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行新架构程序
python app.py

# 运行旧版本(如需对比)
python main.py
```

## 📝 日志系统

日志自动保存在 `logs/` 目录:
- 文件名: `YYYYMMDD_HHMMSS.log`
- 记录级别: INFO 及以上
- 同时输出到控制台和文件

## 🎓 最佳实践

1. **保持层次分离**: 不要在 View 中直接访问 Model
2. **统一错误处理**: 在 Controller 层统一处理异常
3. **参数验证**: 在 Controller 层验证所有输入
4. **日志记录**: 关键操作都要记录日志
5. **代码复用**: 相似功能抽取为工具类

## 🔍 故障排查

### 数据库连接失败
- 检查 `config.ini` 配置
- 确认数据库服务运行
- 查看日志文件详细错误

### 界面显示异常
- 确认 CustomTkinter 版本 >= 5.2.0
- 检查系统字体支持中文
- 查看控制台错误信息

### 图表无法显示
- 确认 matplotlib 正确安装
- 检查中文字体配置
- 尝试更新 matplotlib 版本
