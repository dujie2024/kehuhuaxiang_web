#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接池优化模块
使用DBUtils实现连接池，提升并发查询性能
"""

import pymysql
from dbutils.pooled_db import PooledDB
import configparser
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DatabasePool:
    """数据库连接池管理类"""
    
    _pools = {}  # 存储不同数据库的连接池
    
    @classmethod
    def get_pool(cls, db_name: str = 'carpark') -> PooledDB:
        """
        获取数据库连接池
        
        Args:
            db_name: 数据库配置名称 (carpark 或 dzwl)
        
        Returns:
            PooledDB: 连接池对象
        """
        if db_name not in cls._pools:
            cls._pools[db_name] = cls._create_pool(db_name)
        return cls._pools[db_name]
    
    @classmethod
    def _create_pool(cls, db_name: str) -> PooledDB:
        """
        创建数据库连接池
        
        Args:
            db_name: 数据库配置名称
        
        Returns:
            PooledDB: 连接池对象
        """
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8')
        
        section = f'database.{db_name}'
        
        pool = PooledDB(
            creator=pymysql,
            maxconnections=20,          # 连接池最大连接数
            mincached=2,                # 初始化时至少创建的空闲连接
            maxcached=10,               # 连接池最大空闲连接数
            maxshared=0,                # 最大共享连接数（0表示不共享）
            blocking=True,              # 连接池满时是否阻塞等待
            maxusage=None,              # 单个连接最大复用次数（None表示无限制）
            setsession=[],              # 连接前执行的SQL命令列表
            ping=1,                     # ping MySQL服务器检查连接是否可用
            host=config.get(section, 'host'),
            user=config.get(section, 'user'),
            password=config.get(section, 'password'),
            database=config.get(section, 'database'),
            port=config.getint(section, 'port'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.Cursor
        )
        
        logger.info(f"数据库连接池创建成功: {db_name} (max={20}, cached={10})")
        return pool
    
    @classmethod
    def get_connection(cls, db_name: str = 'carpark'):
        """
        从连接池获取数据库连接
        
        Args:
            db_name: 数据库配置名称
        
        Returns:
            connection: 数据库连接对象
        """
        pool = cls.get_pool(db_name)
        return pool.connection()
    
    @classmethod
    def close_all_pools(cls):
        """关闭所有连接池"""
        for db_name, pool in cls._pools.items():
            try:
                pool.close()
                logger.info(f"连接池已关闭: {db_name}")
            except Exception as e:
                logger.error(f"关闭连接池失败 {db_name}: {e}")
        cls._pools.clear()


class DatabaseModelWithPool:
    """使用连接池的数据库模型基类"""
    
    def __init__(self, db_name: str = 'carpark'):
        """
        初始化数据库模型
        
        Args:
            db_name: 数据库配置名称
        """
        self.db_name = db_name
        self.pool = DatabasePool.get_pool(db_name)
    
    def execute_query(self, query: str, params: tuple = None) -> list:
        """
        执行查询语句
        
        Args:
            query: SQL查询语句
            params: 查询参数
        
        Returns:
            list: 查询结果列表
        """
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f"数据库查询失败: {e}")
            logger.error(f"SQL: {query}")
            logger.error(f"参数: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()  # 归还连接到连接池
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        执行更新语句
        
        Args:
            query: SQL更新语句
            params: 更新参数
        
        Returns:
            int: 影响的行数
        """
        conn = None
        cursor = None
        try:
            conn = self.pool.connection()
            cursor = conn.cursor()
            affected_rows = cursor.execute(query, params)
            conn.commit()
            return affected_rows
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"数据库更新失败: {e}")
            logger.error(f"SQL: {query}")
            logger.error(f"参数: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


# 使用示例
if __name__ == "__main__":
    # 测试连接池
    logging.basicConfig(level=logging.INFO)
    
    # 获取连接
    db = DatabaseModelWithPool('carpark')
    
    # 执行查询
    query = "SELECT COUNT(*) FROM tnxz_dx_vehicle_province_rank_byday"
    result = db.execute_query(query)
    print(f"查询结果: {result}")
    
    # 关闭连接池
    DatabasePool.close_all_pools()
