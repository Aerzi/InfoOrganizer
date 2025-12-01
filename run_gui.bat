@echo off
REM 设置UTF-8编码以支持中文显示
chcp 65001 >nul 2>&1

echo.
echo ============================================================
echo   PPT语料分析工具 - 图形界面启动
echo ============================================================
echo.
echo   正在启动图形界面，请稍候...
echo.

python src/gui.py

if errorlevel 1 (
    echo.
    echo   启动失败！请检查：
    echo   1. 是否已安装Python 3.10+
    echo   2. 是否已运行 install_deps.bat 安装依赖
    echo   3. 是否在项目根目录运行此脚本
    echo.
    pause
)


