import pymysql
import configparser
import logging
from typing import Optional, Tuple, Any

logger = logging.getLogger(__name__)


class DatabaseModel:
    def __init__(self, config_file='config.ini', db_name='carpark'):
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        
        section_name = f'database.{db_name}'
        
        if not config.has_section(section_name):
            raise ValueError(f"配置文件中未找到 [{section_name}] section，请检查 {config_file}")
        
        self.db_config = {
            'host': config.get(section_name, 'host'),
            'user': config.get(section_name, 'user'),
            'password': config.get(section_name, 'password'),
            'database': config.get(section_name, 'database'),
            'port': config.getint(section_name, 'port')
        }
        self.db_name = db_name
        
        logger.info(f"数据库配置加载成功: {section_name} -> {self.db_config['user']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}")
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> list:
        conn = None
        cursor = None
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            data = cursor.fetchall()
            logger.info(f"查询成功,返回 {len(data)} 条记录")
            return data
        except pymysql.Error as err:
            logger.error(f"数据库查询错误: {err}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        try:
            conn = pymysql.connect(**self.db_config)
            conn.close()
            logger.info("数据库连接测试成功")
            return True
        except pymysql.Error as err:
            logger.error(f"数据库连接失败: {err}")
            return False
