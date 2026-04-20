@echo off
chcp 65001 >nul
echo 正在以管理员身份安装数维数据管家系统依赖...
echo ============================================================

:: 安装核心依赖
pip install fastapi uvicorn sqlalchemy pymysql pydantic passlib bcrypt --user

:: 安装其他依赖
pip install simpleeval python-multipart PyJWT --user

echo ============================================================
echo 依赖安装完成！
echo 请按任意键继续...
pause
