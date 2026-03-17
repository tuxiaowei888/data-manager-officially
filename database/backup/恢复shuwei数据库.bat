@echo off
echo ========================================
echo   数维数据管家 - MySQL数据库恢复脚本
echo ========================================
echo.

echo 正在检查数据库文件...
if not exist "shuwei_data_manager_backup.sql" (
    echo.
    echo ✗ 错误：未找到 shuwei_data_manager_backup.sql 文件！
    pause
    exit /b 1
)

echo 正在创建数据库（如果不存在）...
docker exec -i my-mysql mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS shuwei_data_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ✗ 创建数据库失败！请检查 Docker 容器是否运行
    pause
    exit /b 1
)

echo 正在导入数据...
docker cp shuwei_data_manager_backup.sql my-mysql:/tmp/shuwei_data_manager_backup.sql
docker exec -i my-mysql mysql -u root -p123456 shuwei_data_manager -e "source /tmp/shuwei_data_manager_backup.sql"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ 数据库恢复成功！
    echo   现在可以启动系统了
) else (
    echo.
    echo ✗ 恢复失败！请检查数据库配置
)
pause
