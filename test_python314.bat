@echo off
REM 设置UTF-8编码以支持中文显示
chcp 65001 >nul 2>&1

cls
echo.
echo ============================================================
echo   Python 3.14 兼容性测试
echo ============================================================
echo.

echo [步骤 1] 检查Python版本...
python --version
echo.

echo [步骤 2] 检查pip版本...
pip --version
echo.

echo [步骤 3] 尝试安装核心依赖（可能需要几分钟）...
echo.

echo 正在安装 pandas...
pip install "pandas>=2.0.0" --quiet
if errorlevel 1 (
    echo   × pandas 安装失败
    goto :error
) else (
    echo   ✓ pandas 安装成功
)

echo 正在安装 jieba...
pip install "jieba>=0.42.0" --quiet
if errorlevel 1 (
    echo   × jieba 安装失败
    goto :error
) else (
    echo   ✓ jieba 安装成功
)

echo 正在安装 matplotlib...
pip install "matplotlib>=3.7.0" --quiet
if errorlevel 1 (
    echo   × matplotlib 安装失败
    goto :error
) else (
    echo   ✓ matplotlib 安装成功
)

echo 正在安装 openpyxl...
pip install "openpyxl>=3.0.0" --quiet
if errorlevel 1 (
    echo   × openpyxl 安装失败
    goto :error
) else (
    echo   ✓ openpyxl 安装成功
)

echo.
echo [步骤 4] 运行系统测试...
echo.
python test_system.py

echo.
echo ============================================================
echo   Python 3.14 兼容性测试完成！
echo ============================================================
echo.
echo 如果测试全部通过，说明完全兼容 Python 3.14
echo 如果部分失败，请查看上面的错误信息
echo.
pause
goto :end

:error
echo.
echo ============================================================
echo   检测到兼容性问题
echo ============================================================
echo.
echo 可能的原因：
echo   1. 某些依赖库尚未支持 Python 3.14
echo   2. Python 3.14 是测试版本，依赖库还在适配中
echo.
echo 建议：
echo   1. 等待依赖库更新
echo   2. 或使用 Python 3.12（最新稳定版）
echo   3. 查看具体错误信息，尝试手动解决
echo.
pause

:end


