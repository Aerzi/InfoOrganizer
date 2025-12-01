#!/bin/bash
echo "============================================================"
echo "PPT语料分析工具 - 依赖安装"
echo "============================================================"
echo ""

echo "正在安装Python依赖包..."
echo ""

pip install pandas==2.1.4
pip install dask==2023.12.1
pip install openpyxl==3.1.2
pip install jieba==0.42.1
pip install snownlp==0.12.3
pip install matplotlib==3.8.2
pip install seaborn==0.13.2
pip install pyinstaller==5.13.2
pip install rank_bm25==0.2.2

echo ""
echo "============================================================"
echo "安装完成！"
echo "============================================================"
echo ""
echo "运行系统测试:"
echo "  python test_system.py"
echo ""
echo "开始使用:"
echo "  python src/main.py --help"
echo "  python src/gui.py"
echo ""

