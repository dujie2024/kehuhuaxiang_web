# CS架构代码备份说明

本目录包含原CS（Client-Server）架构的代码文件，已被新的模块化BS架构替代。

## 📅 备份时间
2026-02-28

## 📦 备份文件清单

### CS桌面应用主程序
- `main.py` - 原CS架构的主程序（CustomTkinter桌面应用）
- `app.py` - 原CS架构的入口文件
- `main_modern.py` - 现代化UI版本的CS主程序
- `chart_generator.py` - 原CS架构的图表生成器（使用plt.show()）

### 视图层（Views）
- `views/` - 原CS架构的视图目录
  - `main_window.py` - 主窗口
  - `parking_view.py` - 停车数据分析视图
  - `booking_view.py` - 预订数据分析视图
  - `dzwl_view.py` - 电子围栏客流分析视图
  - `report_view.py` - 报表视图
  - `settings_view.py` - 设置视图

### 旧版BS架构（单页面版本）
- `web_app.py` - 旧版单页面BS架构主程序
- `index.html` - 旧版单页面HTML
- `app.js` - 旧版单页面JavaScript
- `style.css` - 旧版单页面CSS

### 构建和打包相关（exe打包）
- `build.py` - PyInstaller打包脚本
- `build_with_version.py` - 带版本信息的打包脚本
- `requirements_build.txt` - 打包所需依赖
- `新朝旅游客户画像分析系统_v1.3.0.spec` - PyInstaller配置文件
- `python-3.11.9.exe` - Python安装程序（26MB）

### 测试文件
- `test_exe.py` - exe测试文件
- `test_db_config.py` - 数据库配置测试

### 配置文件备份
- `config.py` - 旧版配置文件
- `config.ini.backup` - 配置备份
- `version_info.txt` - 版本信息文本

### 依赖和启动脚本
- `requirements.txt` - CS架构的依赖文件
- `启动程序.bat` - CS桌面应用启动脚本
- `启动Web服务器.bat` - 旧版BS架构启动脚本

### 文档（CS/桌面应用相关）
- `README_ARCHITECTURE.md` - 原CS架构说明文档
- `README_UI.md` - UI界面说明文档
- `界面优化说明.md` - 界面优化文档
- `打包说明.md` - exe打包说明
- `分发指南.md` - 软件分发指南

## 🆕 新架构文件（保留在主目录）

### 模块化BS架构
- `app_modular.py` - 新的模块化主应用
- `blueprints/` - Blueprint模块目录
  - `parking_bp.py` - 停车数据模块
  - `booking_bp.py` - 预订数据模块
  - `dzwl_bp.py` - 电子围栏模块
- `templates/` - 模块化HTML页面
  - `index_modular.html` - 主导航页面
  - `parking.html` - 停车数据页面
  - `booking.html` - 预订数据页面
  - `dzwl.html` - 电子围栏页面
- `static/css/module.css` - 模块通用样式
- `static/js/` - 模块化JavaScript
  - `parking.js`
  - `booking.js`
  - `dzwl.js`

### 共享组件（继续使用）
- `controllers/` - 控制器层（复用）
- `models/` - 数据模型层（复用）
- `utils/` - 工具类（复用）
- `config.ini` - 配置文件（复用）
- `version.py` - 版本信息（已更新为v2.0.0）

### 新文档
- `README_模块化架构.md` - 模块化架构说明文档
- `README_WEB.md` - Web版本说明文档
- `快速开始指南.md` - 快速开始指南

### 启动脚本
- `启动模块化Web服务器.bat` - 新的启动脚本

## ⚠️ 注意事项

1. **不要删除 `controllers/` 和 `models/` 目录**
   - 这些是业务逻辑层和数据访问层
   - 新BS架构继续使用这些组件

2. **不要删除 `utils/` 目录**
   - 包含日志、数据库、图表等工具类
   - 新BS架构依赖这些工具

3. **不要删除 `config.ini`**
   - 数据库配置文件
   - 所有版本共用

4. **可以安全删除的内容**
   - 本备份目录下的所有文件
   - 这些文件已不再使用

## 🔄 版本演进

1. **v1.0 - CS架构**（已备份）
   - CustomTkinter桌面应用
   - 直接访问数据库
   - 本地运行

2. **v1.3 - 单页面BS架构**（已备份）
   - Flask单文件Web应用
   - 单页面HTML
   - 支持局域网访问

3. **v2.0 - 模块化BS架构**（当前版本）✨
   - Flask Blueprint模块化
   - 多页面独立HTML
   - 快速日期选择
   - 易扩展、易维护

## 📞 恢复说明

如需恢复CS架构或旧版BS架构：

1. 从本备份目录复制相应文件到主目录
2. 安装对应的依赖：
   - CS架构：`pip install -r requirements.txt`
   - 旧BS架构：`pip install -r requirements_web.txt`
3. 运行对应的启动脚本

---

**建议：保留此备份目录一段时间，确认新架构稳定后再删除。**
