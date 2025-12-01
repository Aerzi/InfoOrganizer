# 兼容性说明

## Python版本兼容性

### ✅ 完全支持（已测试）
- **Python 3.10.x** - 推荐版本，稳定可靠
- **Python 3.11.x** - 性能更好（约快10-15%）
- **Python 3.12.x** - 最新稳定版，性能最佳

### 🟡 可能支持（未深度测试）
- **Python 3.13.x** - 最新稳定版，通常兼容
- **Python 3.14.x** - 测试版本，理论兼容（依赖库支持情况待确认）
- **Python 3.9.x** - 可能工作，但部分特性需注意

### ❌ 不支持
- **Python 3.8 及以下** - 不兼容，请升级

## 依赖库版本兼容性

### 核心依赖最低版本

| 库名 | 最低版本 | 推荐版本 | 说明 |
|------|---------|---------|------|
| pandas | 2.0.0 | 2.1.4+ | 数据处理核心 |
| dask | 2023.0.0 | 2023.12.1+ | 大规模数据支持 |
| jieba | 0.42.0 | 0.42.1+ | 中文分词 |
| snownlp | 0.12.0 | 0.12.3+ | 情感分析 |
| matplotlib | 3.7.0 | 3.8.2+ | 图表生成 |
| seaborn | 0.12.0 | 0.13.2+ | 数据可视化 |
| openpyxl | 3.0.0 | 3.1.2+ | Excel支持 |
| pyinstaller | 5.0.0 | 5.13.2+ | EXE打包 |

### 自动依赖
这些库会被自动安装，无需手动指定：
- numpy（pandas依赖）
- pillow（matplotlib依赖）
- python-dateutil（pandas依赖）

## 操作系统兼容性

### ✅ Windows
- **Windows 10** - 完全支持
- **Windows 11** - 完全支持
- **Windows Server 2019/2022** - 支持

### ✅ Linux
- **Ubuntu 20.04+** - 支持
- **Debian 11+** - 支持
- **CentOS 8+** - 支持
- **其他发行版** - 通常兼容

### ✅ macOS
- **macOS 11 (Big Sur)+** - 支持
- **macOS 10.15 (Catalina)** - 可能需要额外配置

## 特定平台注意事项

### Windows
- ✅ 完全支持中文路径和文件名
- ✅ 支持打包为EXE独立运行
- ⚠️ 需要安装Visual C++ Redistributable（matplotlib依赖）

### Linux
- ✅ 无额外依赖
- ⚠️ GUI模式需要X11（SSH需要X转发）
- ⚠️ 某些发行版需要安装tkinter：`sudo apt install python3-tk`

### macOS
- ✅ 原生支持
- ⚠️ M1/M2芯片需确保使用ARM版Python或Rosetta
- ⚠️ 首次运行matplotlib可能需要安装XQuartz

## 中文支持

### 字体支持
- **Windows**: 自动使用SimHei（黑体）
- **Linux**: 需安装中文字体
  ```bash
  sudo apt install fonts-wqy-zenhei fonts-wqy-microhei
  ```
- **macOS**: 自动使用系统中文字体

### 编码支持
- ✅ UTF-8（推荐）
- ✅ GBK/GB2312（自动识别）
- ✅ UTF-8-BOM

## 数据规模限制

| 场景 | 推荐配置 | 支持规模 |
|------|---------|---------|
| 小规模分析 | 2GB内存 | < 1万行 |
| 中规模分析 | 4GB内存 | 1-10万行 |
| 大规模分析 | 8GB内存 | 10-50万行 |
| 超大规模 | 16GB内存 | 50万行+ |

## 已知问题和解决方案

### 1. SnowNLP在Python 3.12可能有警告
**问题**: 运行时出现DeprecationWarning
**解决**: 不影响功能，可以忽略，或等待snownlp更新

### 2. Matplotlib中文显示问题
**问题**: 图表中文显示为方框
**解决**: 
```python
# 在 src/analyzer/base_analyzer.py 中已自动处理
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
```

### 3. Dask在Windows下的路径问题
**问题**: 路径包含中文或空格时可能出错
**解决**: 使用英文路径，或在代码中进行路径转义（已处理）

## 版本升级指南

### 从Python 3.10升级到3.11
```bash
# 1. 升级Python
# 下载并安装Python 3.11

# 2. 重新安装依赖
pip install -r requirements.txt --upgrade

# 3. 测试
python test_system.py
```

### 从Python 3.11升级到3.12
```bash
# 同上，无需额外配置
pip install -r requirements.txt --upgrade
```

## 性能对比

| Python版本 | 相对性能 | 内存占用 | 推荐场景 |
|-----------|---------|---------|---------|
| 3.10 | 1.0x | 基准 | 稳定性优先 |
| 3.11 | 1.15x | -5% | 性能与稳定兼顾 |
| 3.12 | 1.25x | -10% | 追求极致性能 |

注：性能数据基于官方benchmark，实际效果因场景而异。

## 测试矩阵

我们在以下环境测试过本工具：

| Python | OS | 状态 |
|--------|-------|------|
| 3.10.12 | Windows 11 | ✅ |
| 3.11.5 | Windows 11 | ✅ |
| 3.12.0 | Windows 11 | ✅ |
| 3.10.12 | Ubuntu 22.04 | ✅ |
| 3.11.5 | macOS 13 | ✅ |

## 获取支持

如遇到兼容性问题：
1. 查看本文档的"已知问题"部分
2. 运行 `python test_system.py` 诊断
3. 查看日志文件：`logs/analysis_*.log`
4. 提交问题时请附上Python版本和错误信息

---

**最后更新**: 2025-12-01  
**适用版本**: v1.0.0

