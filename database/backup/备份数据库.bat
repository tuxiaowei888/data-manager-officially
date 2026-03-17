@echo off
echo ========================================
echo   数维数据管家 - MySQL数据库备份脚本
echo ========================================
echo.

echo 正在导出数据库...
docker exec -i shuwei-mysql mysqldump -u root -proot shuwei_data_manager > database_backup.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ 数据库导出成功！
    echo   文件保存在: %CD%\database_backup.sql
    echo.
    echo 请将此文件拷贝到新电脑，然后在新电脑上运行"恢复数据库.bat"
) else (
    echo.
    echo ✗ 导出失败！请检查：
    echo   1. Docker 容器是否正在运行
    echo   2. MySQL 用户名密码是否正确
)
pause
