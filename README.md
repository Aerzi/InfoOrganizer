# PPT主题生成场景语料分析工具

## 项目概述

这是一个**纯本地化、无服务端依赖**的通用语料分析工具，专注于PPT主题生成场景的用户语料分析。核心能力是对语料进行**自定义维度/关键词的多维度分析**，支持大规模数据处理（20万+行），并在PPT场景下的分析效果优于通用大模型。

### 核心特性

- ✅ **纯本地化运行**：无需联网，无数据泄露风险
- ✅ **大规模数据支持**：支持20万+行语料分批处理
- ✅ **自定义维度分析**：支持任意关键词（如"老师/教学/权限/页数"等）
- ✅ **双场景分析**：区分"请求语料"（需求分析）和"反馈语料"（效果反馈）
- ✅ **多维度输出**：文字报告 + Excel表格 + 可视化图表
- ✅ **可打包为EXE**：支持Windows平台独立运行

## 快速开始

### 环境要求

- **Python 3.10+**（推荐 3.10、3.11、3.12，更高版本通常也兼容）
- Windows/Linux/MacOS
- 至少 2GB 可用内存

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基础使用

#### 1. 命令行模式

```bash
# 分析语料（指定自定义维度）
python src/main.py data.xlsx --dimensions "老师,教学" --type both --output output

# 参数说明：
# data.xlsx: 语料文件（支持.xlsx/.csv）
# --dimensions: 自定义维度（多个用逗号分隔）
# --type: 分析类型（request=请求, feedback=反馈, both=双场景）
# --output: 输出目录
```

#### 2. GUI模式

```bash
python src/gui.py
```

启动图形界面，通过可视化界面选择文件和配置参数。

### 语料文件格式

语料文件（Excel或CSV）需包含以下字段：

| 字段名 | 说明 | 是否必需 |
|--------|------|----------|
| content | 语料内容 | ✅ 必需 |
| type | 语料类型（"请求"或"反馈"） | 可选 |
| time | 时间戳 | 可选 |

示例：

| content | type |
|---------|------|
| 希望PPT模板适合老师上课使用，简洁一点 | 请求 |
| 老师反馈说操作太复杂，不适合课堂演示 | 反馈 |

## 核心功能

### 1. 多维度分析

支持对任意自定义维度进行分析，包括：

- **频次分布**：统计维度相关内容的出现频次和占比
- **关联特征**：分析维度与其他诉求的关联关系
- **情感倾向**：识别用户态度（正面/中性/负面）
- **场景关联**：分析维度对应的PPT使用场景
- **需求/问题分类**：归类具体需求和反馈问题

### 2. 双场景分析

- **请求语料分析**（需求分析）
  - 需求分类统计
  - 场景分布分析
  - 关联特征挖掘
  
- **反馈语料分析**（效果反馈）
  - 问题分类统计
  - 情感倾向分析
  - 优化建议生成

### 3. 可视化输出

自动生成多种图表：

- 高频词柱状图
- 情感分布饼图
- 维度关联热力图
- 场景分布图

### 4. 结果输出

- **Markdown报告**：结构化文本报告
- **Excel报告**：多Sheet详细数据
- **PNG图表**：所有可视化图表

## 项目结构

```
InfoOrganizer/
├── src/
│   ├── main.py                # 命令行主入口
│   ├── gui.py                 # GUI界面
│   ├── data_io/               # 数据输入输出模块
│   │   ├── data_loader.py     # 大规模数据加载
│   │   └── result_exporter.py # 结果导出
│   ├── preprocess/            # 预处理模块
│   │   ├── cleaner.py         # 文本清洗
│   │   ├── tokenizer.py       # 分词
│   │   └── dimension_marker.py # 维度标记
│   ├── analyzer/              # 分析引擎
│   │   ├── base_analyzer.py   # 基础分析器
│   │   ├── request_analyzer.py # 请求分析器
│   │   └── feedback_analyzer.py # 反馈分析器
│   ├── config/                # 配置文件
│   │   ├── config.json        # 主配置
│   │   ├── ppt_business_dict.txt # PPT业务词典
│   │   ├── stopwords.txt      # 停用词
│   │   └── synonym_dict.txt   # 同义词词典
│   └── utils/                 # 工具函数
│       ├── logger.py          # 日志工具
│       └── cache.py           # 缓存工具
├── requirements.txt           # 依赖清单
├── build.spec                 # 打包配置
└── README.md                  # 本文件
```

## 打包为EXE

### Windows平台

```bash
# 安装打包工具
pip install pyinstaller

# 打包为EXE（文件夹模式）
pyinstaller build.spec

# 打包结果在 dist/PPT语料分析工具/ 目录下
```

### 使用打包后的EXE

1. 进入 `dist/PPT语料分析工具/` 目录
2. 双击运行 `PPT语料分析工具.exe`
3. 按照命令行提示操作

## 配置说明

### 主配置文件（src/config/config.json）

```json
{
  "data_loader": {
    "batch_size": 10000,           // 分批大小
    "min_content_length": 2        // 最小内容长度
  },
  "preprocess": {
    "custom_dimension_weight_multiplier": 3.0  // 维度权重倍数
  },
  "analyzer": {
    "top_k_results": 10            // Top K结果数量
  }
}
```

### 自定义词典

#### 1. PPT业务词典（ppt_business_dict.txt）

添加PPT场景专属术语，一行一个：

```
PPT主题
演示文稿
课堂演示
```

#### 2. 同义词词典（synonym_dict.txt）

定义同义词关系，格式：主词=同义词1,同义词2

```
老师=教师,教员,讲师
教学=授课,讲课,上课
```

#### 3. 停用词（stopwords.txt）

定义需要过滤的无意义词：

```
的
了
在
```

## 性能指标

针对20万行语料的性能表现：

| 指标 | 数值 |
|------|------|
| 数据加载时间 | ≤60秒 |
| 预处理时间 | ≤120秒 |
| 分析时间 | ≤180秒 |
| 报告生成时间 | ≤30秒 |
| 内存占用 | ≤2GB |
| 总耗时 | ≤6分钟 |

## 技术栈

- **核心语言**：Python 3.10+
- **数据处理**：Pandas + Dask
- **NLP分析**：jieba + SnowNLP + BM25
- **可视化**：Matplotlib + Seaborn
- **打包工具**：PyInstaller
- **GUI框架**：Tkinter

## 常见问题

### Q1: 如何处理大规模数据？

工具自动支持大规模数据分批处理。对于超过5万行的数据，会自动使用Dask进行分批加载，避免内存溢出。

### Q2: 自定义维度如何选择？

根据分析需求选择，例如：
- 用户角色：老师、学生、职员
- 功能维度：页数、风格、模板
- 场景维度：教学、汇报、演示

### Q3: 支持哪些文件格式？

目前支持：
- Excel文件（.xlsx）
- CSV文件（.csv）

自动识别UTF-8、GBK等多种编码。

### Q4: 如何提高分析精度？

1. 完善PPT业务词典（添加领域术语）
2. 扩充同义词词典（统一相似表达）
3. 调整维度权重倍数（config.json）

## 开发与贡献

### 开发环境设置

```bash
# 克隆项目
git clone <repository-url>

# 安装依赖
pip install -r requirements.txt

# 运行测试
python src/main.py test_data.xlsx --dimensions "测试" --output test_output
```

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请联系项目维护者。

---

**版本**：v1.0.0  
**最后更新**：2025-12-01
