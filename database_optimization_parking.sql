-- ============================================
-- 停车数据查询优化 - 数据库索引脚本
-- 创建时间: 2026-02-28
-- 目的: 优化停车数据分析查询性能
-- ============================================

USE carpark;

-- ============================================
-- 1. 天女小镇停车场 - 按省份统计表
-- ============================================
-- 检查是否存在索引
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'carpark'
  AND TABLE_NAME = 'tnxz_dx_vehicle_province_rank_byday'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;

-- 创建复合索引：出场日期 + location
-- 这个索引可以同时优化WHERE条件和GROUP BY
CREATE INDEX idx_tnxz_province_date_location 
ON tnxz_dx_vehicle_province_rank_byday(`出场日期`, location);

-- 如果需要单独的日期索引（用于日期范围查询）
CREATE INDEX idx_tnxz_province_date 
ON tnxz_dx_vehicle_province_rank_byday(`出场日期`);

-- ============================================
-- 2. 天女小镇停车场 - 按城市统计表
-- ============================================
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'carpark'
  AND TABLE_NAME = 'tnxz_dx_vehicle_city_rank_byday'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;

-- 创建复合索引
CREATE INDEX idx_tnxz_city_date_location 
ON tnxz_dx_vehicle_city_rank_byday(`出场日期`, location);

CREATE INDEX idx_tnxz_city_date 
ON tnxz_dx_vehicle_city_rank_byday(`出场日期`);

-- ============================================
-- 3. 欢乐湾停车场 - 按省份统计表
-- ============================================
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'carpark'
  AND TABLE_NAME = 'hlw_vehicle_province_rank_byday'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;

-- 创建复合索引
CREATE INDEX idx_hlw_province_date_location 
ON hlw_vehicle_province_rank_byday(`出场日期`, location);

CREATE INDEX idx_hlw_province_date 
ON hlw_vehicle_province_rank_byday(`出场日期`);

-- ============================================
-- 4. 欢乐湾停车场 - 按城市统计表
-- ============================================
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'carpark'
  AND TABLE_NAME = 'hlw_vehicle_city_rank_byday'
ORDER BY INDEX_NAME, SEQ_IN_INDEX;

-- 创建复合索引
CREATE INDEX idx_hlw_city_date_location 
ON hlw_vehicle_city_rank_byday(`出场日期`, location);

CREATE INDEX idx_hlw_city_date 
ON hlw_vehicle_city_rank_byday(`出场日期`);

-- ============================================
-- 5. 验证索引创建结果
-- ============================================
-- 查看所有停车数据表的索引
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    INDEX_TYPE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = 'carpark'
  AND TABLE_NAME IN (
    'tnxz_dx_vehicle_province_rank_byday',
    'tnxz_dx_vehicle_city_rank_byday',
    'hlw_vehicle_province_rank_byday',
    'hlw_vehicle_city_rank_byday'
  )
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- ============================================
-- 6. 查询性能测试
-- ============================================
-- 测试查询（五一假期）
EXPLAIN SELECT 
    a.location, 
    SUM(a.vehicle_count) AS vehicle_count
FROM tnxz_dx_vehicle_province_rank_byday a
WHERE a.`出场日期` BETWEEN '2025-05-01' AND '2025-05-05'
GROUP BY a.location
ORDER BY vehicle_count DESC
LIMIT 10;

-- 查看查询执行计划
-- 优化后应该看到：
-- - type: range (使用索引范围扫描)
-- - key: idx_tnxz_province_date 或 idx_tnxz_province_date_location
-- - rows: 显著减少

-- ============================================
-- 7. 索引维护建议
-- ============================================
-- 定期分析表，更新索引统计信息
ANALYZE TABLE tnxz_dx_vehicle_province_rank_byday;
ANALYZE TABLE tnxz_dx_vehicle_city_rank_byday;
ANALYZE TABLE hlw_vehicle_province_rank_byday;
ANALYZE TABLE hlw_vehicle_city_rank_byday;

-- ============================================
-- 8. 如果索引已存在，先删除再创建
-- ============================================
-- 取消注释以下语句来删除旧索引（如果需要）
/*
DROP INDEX idx_tnxz_province_date_location ON tnxz_dx_vehicle_province_rank_byday;
DROP INDEX idx_tnxz_province_date ON tnxz_dx_vehicle_province_rank_byday;
DROP INDEX idx_tnxz_city_date_location ON tnxz_dx_vehicle_city_rank_byday;
DROP INDEX idx_tnxz_city_date ON tnxz_dx_vehicle_city_rank_byday;
DROP INDEX idx_hlw_province_date_location ON hlw_vehicle_province_rank_byday;
DROP INDEX idx_hlw_province_date ON hlw_vehicle_province_rank_byday;
DROP INDEX idx_hlw_city_date_location ON hlw_vehicle_city_rank_byday;
DROP INDEX idx_hlw_city_date ON hlw_vehicle_city_rank_byday;
*/

-- ============================================
-- 预期性能提升
-- ============================================
-- 优化前：全表扫描，查询时间 2-5秒（取决于数据量）
-- 优化后：索引扫描，查询时间 0.1-0.5秒
-- 提升倍数：5-50倍（数据量越大，提升越明显）
