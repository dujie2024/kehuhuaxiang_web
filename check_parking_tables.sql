-- ============================================
-- 查询停车数据表结构
-- 用于了解字段信息，设计驻留时长分析方案
-- ============================================

USE carpark;

-- ============================================
-- 1. 查看所有停车相关的表
-- ============================================
SHOW TABLES LIKE '%vehicle%';
SHOW TABLES LIKE '%parking%';
SHOW TABLES LIKE '%tnxz%';
SHOW TABLES LIKE '%hlw%';

-- ============================================
-- 2. 查看天女小镇按省份统计表结构
-- ============================================
DESC tnxz_dx_vehicle_province_rank_byday;

-- 查看示例数据
SELECT * FROM tnxz_dx_vehicle_province_rank_byday LIMIT 5;

-- 查看所有字段
SHOW FULL COLUMNS FROM tnxz_dx_vehicle_province_rank_byday;

-- ============================================
-- 3. 查看天女小镇按城市统计表结构
-- ============================================
DESC tnxz_dx_vehicle_city_rank_byday;

SELECT * FROM tnxz_dx_vehicle_city_rank_byday LIMIT 5;

-- ============================================
-- 4. 查看欢乐湾按省份统计表结构
-- ============================================
DESC hlw_vehicle_province_rank_byday;

SELECT * FROM hlw_vehicle_province_rank_byday LIMIT 5;

-- ============================================
-- 5. 查看欢乐湾按城市统计表结构
-- ============================================
DESC hlw_vehicle_city_rank_byday;

SELECT * FROM hlw_vehicle_city_rank_byday LIMIT 5;

-- ============================================
-- 6. 查找可能的原始明细表
-- ============================================
-- 查看是否有包含时间戳的原始记录表
SHOW TABLES;

-- 查看表的创建语句（可以看到完整的字段定义）
SHOW CREATE TABLE tnxz_dx_vehicle_province_rank_byday;

-- ============================================
-- 7. 查询是否有驻留时长相关字段
-- ============================================
-- 在现有表中查找可能包含时长信息的字段
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    COLUMN_COMMENT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'carpark'
  AND TABLE_NAME LIKE '%vehicle%'
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- ============================================
-- 8. 查询是否有入场/出场时间字段
-- ============================================
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    COLUMN_COMMENT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'carpark'
  AND (
    COLUMN_NAME LIKE '%时间%' 
    OR COLUMN_NAME LIKE '%time%'
    OR COLUMN_NAME LIKE '%入场%'
    OR COLUMN_NAME LIKE '%出场%'
    OR COLUMN_NAME LIKE '%驻留%'
    OR COLUMN_NAME LIKE '%停留%'
  )
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- ============================================
-- 9. 查看数据量和日期范围
-- ============================================
-- 天女小镇省份表
SELECT 
    COUNT(*) AS total_records,
    MIN(`出场日期`) AS earliest_date,
    MAX(`出场日期`) AS latest_date
FROM tnxz_dx_vehicle_province_rank_byday;

-- 欢乐湾省份表
SELECT 
    COUNT(*) AS total_records,
    MIN(`出场日期`) AS earliest_date,
    MAX(`出场日期`) AS latest_date
FROM hlw_vehicle_province_rank_byday;

-- ============================================
-- 10. 检查是否有车牌号字段
-- ============================================
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'carpark'
  AND (
    COLUMN_NAME LIKE '%车牌%'
    OR COLUMN_NAME LIKE '%plate%'
    OR COLUMN_NAME LIKE '%license%'
  );
