-- ========================================
-- 数据库用户权限配置脚本
-- 创建只读应用账户，用于应用程序访问数据库
-- ========================================

-- 1. 创建应用专用用户
-- 用户名: carpark_app
-- 密码: carpark_app_2026 (请根据实际情况修改)
-- 主机: % (允许任何主机连接，可以改为具体IP如 '192.168.0.%')

-- 为 carpark 数据库创建用户
CREATE USER IF NOT EXISTS 'carpark_app'@'%' IDENTIFIED BY 'carpark_app_2026';

-- 为 dzwl 数据库创建用户（如果使用相同用户）
-- 或者可以创建单独的用户
-- CREATE USER IF NOT EXISTS 'dzwl_app'@'%' IDENTIFIED BY 'dzwl_app_2026';


-- ========================================
-- 2. 授予 carpark 数据库的查询权限
-- ========================================

-- 授予 SELECT 权限（查询表和视图）
GRANT SELECT ON carpark.* TO 'carpark_app'@'%';

-- 如果需要查询特定表，可以使用以下方式（更细粒度控制）
-- GRANT SELECT ON carpark.joy_carpark_tab TO 'carpark_app'@'%';
-- GRANT SELECT ON carpark.joy_booking_tab TO 'carpark_app'@'%';


-- ========================================
-- 3. 授予 dzwl 数据库的查询权限
-- ========================================

-- 授予 SELECT 权限（查询表和视图）
GRANT SELECT ON dzwl.* TO 'carpark_app'@'%';

-- 如果需要查询特定表或视图
-- GRANT SELECT ON dzwl.joy_dzwl_tab_q2 TO 'carpark_app'@'%';


-- ========================================
-- 4. 刷新权限
-- ========================================
FLUSH PRIVILEGES;


-- ========================================
-- 5. 验证用户权限
-- ========================================

-- 查看用户权限
SHOW GRANTS FOR 'carpark_app'@'%';

-- 查看所有用户
-- SELECT User, Host FROM mysql.user WHERE User = 'carpark_app';


-- ========================================
-- 可选：创建单独的用户用于不同数据库
-- ========================================

/*
-- 如果希望为每个数据库创建独立用户：

-- carpark 数据库用户
CREATE USER IF NOT EXISTS 'carpark_app'@'%' IDENTIFIED BY 'carpark_app_2026';
GRANT SELECT ON carpark.* TO 'carpark_app'@'%';

-- dzwl 数据库用户
CREATE USER IF NOT EXISTS 'dzwl_app'@'%' IDENTIFIED BY 'dzwl_app_2026';
GRANT SELECT ON dzwl.* TO 'dzwl_app'@'%';

FLUSH PRIVILEGES;
*/


-- ========================================
-- 可选：限制特定IP访问
-- ========================================

/*
-- 如果只允许特定IP段访问（推荐）：

-- 删除通配符用户
DROP USER IF EXISTS 'carpark_app'@'%';

-- 创建限制IP的用户
CREATE USER IF NOT EXISTS 'carpark_app'@'192.168.0.%' IDENTIFIED BY 'carpark_app_2026';
GRANT SELECT ON carpark.* TO 'carpark_app'@'192.168.0.%';
GRANT SELECT ON dzwl.* TO 'carpark_app'@'192.168.0.%';
FLUSH PRIVILEGES;
*/


-- ========================================
-- 可选：删除用户（如需回滚）
-- ========================================

/*
-- 删除创建的用户
DROP USER IF EXISTS 'carpark_app'@'%';
DROP USER IF EXISTS 'dzwl_app'@'%';
FLUSH PRIVILEGES;
*/


-- ========================================
-- 安全建议
-- ========================================

/*
1. 修改默认密码
   - 将 'carpark_app_2026' 改为强密码
   - 密码建议包含大小写字母、数字、特殊字符
   - 长度至少12位

2. 限制访问IP
   - 将 '%' 改为具体的IP地址或IP段
   - 例如: '192.168.0.%' 或 '192.168.0.100'

3. 定期审计
   - 定期检查用户权限
   - 监控数据库访问日志
   - 及时删除不使用的账户

4. 最小权限原则
   - 只授予必要的权限
   - 如果只需要查询特定表，使用表级权限
   - 避免使用 root 账户

5. 密码管理
   - 定期更换密码
   - 不要在代码中硬编码密码
   - 使用配置文件管理密码
*/
