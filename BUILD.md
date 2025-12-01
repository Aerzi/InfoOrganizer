# 打包说明

## 打包为Windows EXE

### 前提条件

1. 已安装Python 3.10+
2. 已安装所有依赖：`pip install -r requirements.txt`
3. 已安装PyInstaller：`pip install pyinstaller`

### 打包步骤

#### 方式1：使用spec配置文件（推荐）

```bash
# 在项目根目录执行
pyinstaller build.spec
```

#### 方式2：手动打包命令

```bash
# 文件夹模式（推荐，体积约120MB）
pyinstaller --onedir ^
--windowed ^
--add-data "src/config;config" ^
--exclude-module tkinter.test ^
--optimize=2 ^
--name "PPT语料分析工具" ^
src/main.py

# 单文件模式（可选，体积约80MB，启动较慢）
pyinstaller --onefile ^
--windowed ^
--add-data "src/config;config" ^
--exclude-module tkinter.test ^
--optimize=2 ^
--name "PPT语料分析工具" ^
src/main.py
```

### 打包结果

打包完成后，结果在 `dist/PPT语料分析工具/` 目录：

```
dist/
└── PPT语料分析工具/
    ├── PPT语料分析工具.exe  # 主程序
    ├── config/               # 配置文件
    ├── _internal/            # 依赖库
    └── ...
```

### 使用打包后的程序

#### 命令行模式

```bash
cd dist/PPT语料分析工具
PPT语料分析工具.exe data.xlsx --dimensions "老师,教学" --type both
```

#### GUI模式（需单独打包GUI）

```bash
# 打包GUI版本
pyinstaller --onedir ^
--windowed ^
--add-data "src/config;config" ^
--exclude-module tkinter.test ^
--optimize=2 ^
--name "PPT语料分析工具-GUI" ^
src/gui.py
```

### 打包优化建议

#### 减小体积

1. **排除不必要的模块**：
```bash
--exclude-module test
--exclude-module unittest
--exclude-module email
```

2. **压缩可执行文件**：
```bash
--upx-dir=<upx路径>  # 需要下载UPX工具
```

3. **移除调试信息**：
```bash
--strip  # Linux/Mac
--optimize=2  # Python字节码优化
```

#### 提升启动速度

- 使用 `--onedir` 模式（文件夹模式）
- 避免打包过多不必要的依赖

### 常见问题

#### Q1: 打包后运行出错

**解决方案**：
1. 检查是否包含所有必要的数据文件（config目录）
2. 确保使用 `--add-data` 参数添加配置文件
3. 查看日志文件（logs/目录）了解详细错误

#### Q2: 打包体积过大

**解决方案**：
1. 检查是否包含了不必要的依赖（如torch、tensorflow）
2. 使用虚拟环境打包，只安装必需的包
3. 使用UPX压缩

#### Q3: 杀毒软件误报

**解决方案**：
1. 使用 `--clean` 参数重新打包
2. 向杀毒软件厂商提交误报申诉
3. 在打包时添加代码签名（需要代码签名证书）

### 分发建议

#### 打包成压缩包

```bash
# 进入dist目录
cd dist

# 压缩为zip
# Windows: 使用7-Zip或WinRAR
7z a PPT语料分析工具_v1.0.0.zip "PPT语料分析工具"
```

#### 创建安装包（可选）

使用NSIS或Inno Setup创建Windows安装程序：

1. 下载Inno Setup
2. 使用提供的脚本模板
3. 编译生成Setup.exe

### 测试清单

打包完成后，测试以下功能：

- [ ] 程序能正常启动
- [ ] 能加载配置文件
- [ ] 能读取测试语料文件
- [ ] 能执行完整分析流程
- [ ] 能正常生成报告
- [ ] 能保存输出文件
- [ ] 图表能正常生成

## Linux/Mac打包

### Linux

```bash
pyinstaller --onedir \
--add-data "src/config:config" \
--exclude-module tkinter.test \
--optimize=2 \
--name "PPT语料分析工具" \
src/main.py
```

### Mac

```bash
pyinstaller --onedir \
--add-data "src/config:config" \
--exclude-module tkinter.test \
--optimize=2 \
--name "PPT语料分析工具" \
src/main.py
```

注意：Mac平台需要额外处理代码签名和公证。

---

**建议**：首次打包请在干净的虚拟环境中进行，避免包含不必要的依赖。

