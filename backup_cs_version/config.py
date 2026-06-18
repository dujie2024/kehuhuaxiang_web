# MySQL 数据库配置
DB_CONFIG = {
    #"host": "120.48.90.104",
    "host": "127.0.0.1",
    "port": 3306,  # 端口号，整数类型
    "user": "root", 
    "password": "root",
    #"password": "Root123456_",
    "database": "carpark",
    "charset": "utf8mb4",  # 字符集配置
    "autocommit": True,  # 自动提交配置
    "connect_timeout": 10  # 连接超时配置，整数类型
}