@echo off
chcp 65001
cls
setlocal enabledelayedexpansion


:: 检查管理员权限
openfiles >nul 2>&1
if %errorlevel%==0 (
    set ADMIN=true
) else (
    set ADMIN=false
)

:: 设置脚本路径
set SCRIPT_PATH=%~dp0
cd /d "%SCRIPT_PATH%"

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 未检测到Python环境，请先安装Python 3.x
    pause
    exit /b 1
)

:: 安装ntplib（如果尚未安装）
pip list | find "ntplib" >nul || pip install ntplib

:: 运行主程序
python start_sync.py

pause