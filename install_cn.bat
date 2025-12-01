@echo off
REM 设置控制台代码页为UTF-8
chcp 65001 >nul 2>&1

cls
echo.
echo ============================================================
echo.
echo   PPT语料分析工具 - 依赖安装程序
echo.
echo ============================================================
echo.
echo.

echo [1/9] 正在安装 pandas...
pip install pandas==2.1.4 -q

echo [2/9] 正在安装 dask...
pip install dask==2023.12.1 -q

echo [3/9] 正在安装 openpyxl...
pip install openpyxl==3.1.2 -q

echo [4/9] 正在安装 jieba...
pip install jieba==0.42.1 -q

echo [5/9] 正在安装 snownlp...
pip install snownlp==0.12.3 -q

echo [6/9] 正在安装 matplotlib...
pip install matplotlib==3.8.2 -q

echo [7/9] 正在安装 seaborn...
pip install seaborn==0.13.2 -q

echo [8/9] 正在安装 pyinstaller...
pip install pyinstaller==5.13.2 -q

echo [9/9] 正在安装 rank_bm25...
pip install rank_bm25==0.2.2 -q

echo.
echo.
echo ============================================================
echo.
echo   安装完成！
echo.
echo ============================================================
echo.
echo.
echo 下一步操作：
echo.
echo   1. 运行系统测试：
echo      python test_system.py
echo.
echo   2. 查看使用帮助：
echo      python src/main.py --help
echo.
echo   3. 启动图形界面：
echo      python src/gui.py
echo.
echo.
pause

