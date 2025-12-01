@echo off
REM 设置UTF-8编码以支持中文显示
chcp 65001 >nul 2>&1

cls
echo.
echo ============================================================
echo   PPT语料分析工具 - 依赖安装程序
echo ============================================================
echo.
echo.

echo [1/9] 正在安装 pandas (数据处理库)...
pip install pandas==2.1.4 --quiet

echo [2/9] 正在安装 dask (大规模数据处理)...
pip install dask==2023.12.1 --quiet

echo [3/9] 正在安装 openpyxl (Excel支持)...
pip install openpyxl==3.1.2 --quiet

echo [4/9] 正在安装 jieba (中文分词)...
pip install jieba==0.42.1 --quiet

echo [5/9] 正在安装 snownlp (情感分析)...
pip install snownlp==0.12.3 --quiet

echo [6/9] 正在安装 matplotlib (图表生成)...
pip install matplotlib==3.8.2 --quiet

echo [7/9] 正在安装 seaborn (数据可视化)...
pip install seaborn==0.13.2 --quiet

echo [8/9] 正在安装 pyinstaller (EXE打包工具)...
pip install pyinstaller==5.13.2 --quiet

echo [9/9] 正在安装 rank_bm25 (关键词提取)...
pip install rank_bm25==0.2.2 --quiet

echo.
echo.
echo ============================================================
echo   所有依赖安装完成！
echo ============================================================
echo.
echo.
echo 下一步操作：
echo.
echo   1. 运行系统测试（验证安装是否成功）：
echo      python test_system.py
echo.
echo   2. 查看命令行使用帮助：
echo      python src/main.py --help
echo.
echo   3. 启动图形界面（推荐新手使用）：
echo      python src/gui.py
echo.
echo   4. 快速开始示例：
echo      python src/main.py data.xlsx -d "老师,教学" -t both
echo.
echo.
pause

