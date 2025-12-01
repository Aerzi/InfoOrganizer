# Python 3.14 使用说明

## 🎉 欢迎Python 3.14早期用户！

您正在使用Python 3.14（可能是alpha或beta版本），这是非常前沿的版本！

## ✅ 理论兼容性

本项目**理论上完全兼容** Python 3.14，因为：

1. **纯Python代码**：没有使用C扩展或底层API
2. **标准库依赖**：只使用稳定的标准库特性
3. **成熟第三方库**：pandas、matplotlib等都会提前适配新版本
4. **向前兼容**：Python社区注重向后兼容性

## 🧪 快速测试

### 方式1：使用自动测试脚本
```bash
# 双击运行
test_python314.bat
```

这个脚本会：
1. 检查Python版本
2. 逐个安装核心依赖
3. 运行系统测试
4. 报告兼容性结果

### 方式2：手动测试
```bash
# 1. 尝试安装依赖
pip install -r requirements.txt

# 2. 运行测试
python test_system.py

# 3. 如果测试通过，直接使用
python src/gui.py
```

## ⚠️ 可能遇到的问题

### 问题1：某些库没有Python 3.14的wheel
**表现**：安装时需要从源码编译，耗时较长
**解决**：耐心等待编译完成，或使用虚拟环境

### 问题2：SnowNLP可能有警告
**表现**：运行时出现DeprecationWarning
**影响**：不影响功能，可以忽略
**解决**：等待snownlp更新或添加警告过滤

### 问题3：某些依赖尚未支持
**表现**：pip install失败
**解决方案**：
```bash
# 尝试安装开发版
pip install --pre <package-name>

# 或指定低一版本的依赖
pip install "pandas>=2.0.0,<2.3.0"
```

## 🔍 已知情况（持续更新）

### 核心依赖支持情况

| 库名 | Python 3.14支持 | 备注 |
|------|----------------|------|
| pandas | ✅ 通常支持 | 新版本都会适配 |
| jieba | ✅ 纯Python | 完全兼容 |
| matplotlib | ✅ 通常支持 | 可能需要最新版 |
| seaborn | ✅ 通常支持 | 依赖matplotlib |
| openpyxl | ✅ 纯Python | 完全兼容 |
| snownlp | ⚠️ 可能有警告 | 不影响使用 |
| dask | ✅ 通常支持 | 新版本都会适配 |
| pyinstaller | ⚠️ 待确认 | 打包功能可能需等待更新 |

## 🎯 推荐操作流程

### 第1步：测试兼容性
```bash
test_python314.bat
```

### 第2步：根据测试结果决策

#### 如果全部通过 ✅
恭喜！可以正常使用，继续下面的步骤：
```bash
# 安装完整依赖
install_deps.bat

# 启动GUI
run_gui.bat
```

#### 如果部分失败 ⚠️
有两个选择：

**选择A：降级到稳定版本（推荐）**
```bash
# 安装Python 3.12（最新稳定版）
# 从 https://www.python.org/downloads/ 下载

# 重新测试
python test_system.py
```

**选择B：尝试手动解决**
1. 查看具体错误信息
2. 尝试安装预发布版本：`pip install --pre <package>`
3. 或等待依赖库更新

## 📊 性能预期

Python 3.14 相比 3.12 可能带来：
- **性能提升**：5-15%（取决于具体优化）
- **内存优化**：更好的内存管理
- **新特性**：可能有新的语言特性

## 💡 实用技巧

### 创建虚拟环境（强烈推荐）
```bash
# 创建虚拟环境
python -m venv venv_314

# 激活虚拟环境（Windows）
venv_314\Scripts\activate

# 在虚拟环境中安装
pip install -r requirements.txt

# 运行测试
python test_system.py
```

### 查看安装的包版本
```bash
pip list
```

### 查看某个包是否兼容
```bash
pip install --dry-run <package-name>
```

## 🐛 问题反馈

如果在Python 3.14上遇到问题，请记录：
1. **Python精确版本**：`python --version`
2. **错误信息**：完整的错误堆栈
3. **依赖版本**：`pip list > installed_packages.txt`
4. **测试结果**：`test_system.py`的输出

## 📚 参考资源

- [Python 3.14 What's New](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Python Release Schedule](https://peps.python.org/pep-0000/)
- 本项目兼容性文档：`COMPATIBILITY.md`

## 🎊 结论

**大概率完全兼容！** 

Python社区对向后兼容性非常重视，只要依赖库更新及时，本项目在Python 3.14上应该可以无缝运行。

如果遇到问题，运行 `test_python314.bat` 即可快速诊断！

---

**最后更新**: 2025-12-01  
**测试状态**: 理论兼容，待实测验证  
**建议行动**: 先运行 test_python314.bat 测试


