# 新朝旅游客户画像分析系统 - BS架构说明

## 📋 项目概述

本项目已从CS（Client-Server）桌面应用架构成功转换为BS（Browser-Server）Web应用架构，支持通过Google Chrome等现代浏览器访问，并可在局域网内多用户同时使用。

## 🏗️ 架构变更

### 原CS架构
- **客户端**: CustomTkinter桌面应用
- **数据访问**: 客户端直接连接MySQL数据库
- **图表展示**: Matplotlib弹窗显示
- **部署方式**: 需在每台电脑安装客户端程序

### 新BS架构
- **服务端**: Flask Web服务器
- **客户端**: HTML5 + CSS3 + JavaScript (纯浏览器)
- **数据访问**: 浏览器 → Flask API → MySQL数据库
- **图表展示**: 服务端生成图表，Base64编码传输到浏览器
- **部署方式**: 服务器端运行一次，局域网内所有设备通过浏览器访问

## 📁 新增文件结构

```
kehuhuaxiang_web/
├── web_app.py                 # Flask Web服务器主程序
├── templates/                 # HTML模板目录
│   └── index.html            # 主页面
├── static/                    # 静态资源目录
│   ├── css/
│   │   └── style.css         # 样式表
│   └── js/
│       └── app.js            # 前端JavaScript逻辑
├── utils/
│   └── web_chart_utils.py    # Web图表生成工具
├── requirements_web.txt       # Web版依赖包
├── 启动Web服务器.bat          # Windows启动脚本
└── README_WEB.md             # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装Web版依赖
pip install -r requirements_web.txt
```

### 2. 启动服务器

**方式一：使用批处理文件（推荐）**
```bash
双击运行: 启动Web服务器.bat
```

**方式二：命令行启动**
```bash
python web_app.py
```

### 3. 访问系统

启动后，控制台会显示访问地址：

- **本机访问**: http://localhost:5000
- **局域网访问**: http://192.168.x.x:5000 (实际IP会在启动时显示)

## 🌐 局域网访问配置

### 服务器端配置

1. **确保防火墙允许端口5000**
   - Windows防火墙: 控制面板 → 系统和安全 → Windows Defender防火墙 → 高级设置 → 入站规则 → 新建规则
   - 选择"端口" → TCP → 特定本地端口: 5000 → 允许连接

2. **获取服务器IP地址**
   - 启动服务器时会自动显示
   - 或使用命令: `ipconfig` (Windows) / `ifconfig` (Linux/Mac)

### 客户端访问

1. 确保客户端设备与服务器在同一局域网
2. 打开Google Chrome浏览器
3. 输入地址: `http://服务器IP:5000`
4. 开始使用系统

## 🎨 功能特性

### 1. 停车数据分析
- 选择停车场（天女小镇/欢乐湾）
- 选择分析维度（按省份/按城市）
- 设置日期范围
- 查看TOP10排名数据
- 生成可视化图表

### 2. 预订数据分析
- 选择项目（祖山/海上游船）
- 选择分析类型（手机号段/实名制省份/实名制城市）
- 设置日期范围
- 查看TOP10排名数据
- 生成可视化图表

### 3. 现代化界面
- 响应式设计，支持不同屏幕尺寸
- 侧边栏导航，类似后台管理系统
- 卡片式数据展示
- 平滑动画效果
- 加载状态提示

## 🔧 技术栈

### 后端
- **Flask 2.3+**: Web框架
- **Flask-CORS**: 跨域资源共享
- **PyMySQL**: MySQL数据库连接
- **Matplotlib**: 图表生成

### 前端
- **HTML5**: 页面结构
- **CSS3**: 样式和动画
- **JavaScript (ES6+)**: 交互逻辑
- **Fetch API**: 异步数据请求

## 📡 API接口说明

### 停车数据相关

**获取停车场选项**
```
GET /api/parking/options
返回: { success: true, data: { parking_lots: [...], chart_types: [...] } }
```

**分析停车数据**
```
POST /api/parking/analyze
请求体: { parking_lot, chart_type, start_date, end_date }
返回: { success: true, data: [[location, count], ...] }
```

**生成停车数据图表**
```
POST /api/parking/chart
请求体: { data, parking_lot, chart_type, start_date, end_date }
返回: { success: true, chart: "base64_encoded_image" }
```

### 预订数据相关

**获取预订选项**
```
GET /api/booking/options
返回: { success: true, data: { projects: [...], chart_types: [...] } }
```

**分析预订数据**
```
POST /api/booking/analyze
请求体: { project, chart_type, start_date, end_date }
返回: { success: true, data: [[location, count], ...] }
```

**生成预订数据图表**
```
POST /api/booking/chart
请求体: { data, project, chart_type, start_date, end_date }
返回: { success: true, chart: "base64_encoded_image" }
```

### 健康检查
```
GET /api/health
返回: { success: true, message: "Service is running", version: "..." }
```

## 🔒 安全建议

1. **生产环境部署**
   - 修改Flask配置: `app.run(debug=False)`
   - 使用WSGI服务器（如Gunicorn、uWSGI）
   - 配置Nginx反向代理

2. **数据库安全**
   - 使用专用数据库账户，限制权限
   - 不要在公网暴露数据库端口
   - 定期备份数据

3. **访问控制**
   - 仅在内网使用，不要暴露到公网
   - 如需公网访问，添加身份验证
   - 使用HTTPS加密传输

## 🐛 故障排查

### 无法访问Web页面

1. **检查服务器是否启动**
   - 查看控制台是否有错误信息
   - 确认显示"Running on http://0.0.0.0:5000"

2. **检查防火墙**
   - 临时关闭防火墙测试
   - 添加端口5000的入站规则

3. **检查网络连接**
   - 确保客户端和服务器在同一局域网
   - 使用ping命令测试连通性

### 数据查询失败

1. **检查数据库连接**
   - 确认config.ini配置正确
   - 测试数据库服务是否运行
   - 检查数据库用户权限

2. **查看日志**
   - 检查logs目录下的日志文件
   - 查看控制台错误信息

### 图表无法显示

1. **检查matplotlib**
   - 确认matplotlib正确安装
   - 确认使用Agg后端（非GUI）

2. **检查字体**
   - 确认系统安装了中文字体
   - 可能需要安装Microsoft YaHei字体

## 📊 性能优化建议

1. **数据库查询优化**
   - 为常用查询字段添加索引
   - 使用连接池管理数据库连接

2. **缓存策略**
   - 对静态数据使用缓存
   - 使用Redis缓存查询结果

3. **并发处理**
   - 使用Gunicorn多进程部署
   - 配置适当的worker数量

## 🔄 版本对比

| 特性 | CS架构 | BS架构 |
|------|--------|--------|
| 部署方式 | 每台电脑安装 | 服务器运行一次 |
| 访问方式 | 桌面应用 | 浏览器访问 |
| 多用户 | 需多次安装 | 支持多用户同时访问 |
| 更新维护 | 需逐台更新 | 服务器端更新即可 |
| 跨平台 | Windows限定 | 任何支持浏览器的设备 |
| 数据安全 | 客户端直连数据库 | 通过API访问，更安全 |

## 📝 后续开发建议

1. **用户认证**: 添加登录功能，区分不同用户权限
2. **数据导出**: 支持导出Excel、PDF报表
3. **实时刷新**: WebSocket实时数据推送
4. **移动适配**: 优化移动端显示效果
5. **数据缓存**: 减少数据库查询压力
6. **日志审计**: 记录用户操作日志

## 📞 技术支持

如遇到问题，请检查：
1. logs目录下的日志文件
2. 浏览器控制台的错误信息
3. 服务器控制台的输出信息

---

**注意**: 原CS架构的文件（main.py、app.py等）仍然保留，可以继续使用桌面版本。Web版本是新增功能，两者可以并存。
