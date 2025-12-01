# 快速启动指南

## 第一次使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 测试系统

```bash
python test_system.py
```

确保所有测试通过。

### 3. 准备语料文件

创建Excel或CSV文件，至少包含`content`列。参考 `SAMPLE_DATA.md`。

### 4. 开始分析

#### 方式A：命令行

```bash
python src/main.py 你的语料文件.xlsx --dimensions "老师,教学" --type both
```

#### 方式B：图形界面

```bash
python src/gui.py
```

## 命令行参数说明

```bash
python src/main.py <文件路径> [选项]

必需参数:
  文件路径              语料文件(.xlsx 或 .csv)
  --dimensions, -d     自定义维度（逗号分隔）

可选参数:
  --type, -t          分析类型: request/feedback/both (默认: both)
  --output, -o        输出目录 (默认: output)
  --config, -c        配置文件路径 (可选)

示例:
  python src/main.py data.xlsx -d "老师,教学" -t both -o results
```

## 输出结果

分析完成后，在输出目录会生成：

```
output/
├── PPT语料分析报告_老师,教学_20251201_120000.md    # Markdown报告
├── PPT语料分析报告_老师,教学_20251201_120000.xlsx  # Excel报告
└── charts/                                        # 图表目录
    ├── 老师_教学_请求_总体词频.png
    ├── 老师_教学_请求_维度词频.png
    ├── 老师_教学_请求_情感分布.png
    ├── 老师_教学_反馈_总体词频.png
    ├── 老师_教学_反馈_维度词频.png
    └── 老师_教学_反馈_情感分布.png
```

## 常见使用场景

### 场景1：分析教学相关需求

```bash
python src/main.py ppt_requests.xlsx --dimensions "老师,教学,课堂" --type request
```

### 场景2：分析页数相关反馈

```bash
python src/main.py ppt_feedback.xlsx --dimensions "页数,页面" --type feedback
```

### 场景3：完整双场景分析

```bash
python src/main.py all_data.xlsx --dimensions "老师,教学,页数" --type both
```

## 自定义配置

编辑 `src/config/config.json` 可调整：

- 分批大小（batch_size）
- 维度权重倍数（weight_multiplier）
- Top K结果数量（top_k_results）

编辑词典文件可优化分析效果：

- `ppt_business_dict.txt` - PPT业务词典
- `synonym_dict.txt` - 同义词词典
- `stopwords.txt` - 停用词

## 获取帮助

```bash
# 查看帮助
python src/main.py --help

# 运行系统测试
python test_system.py
```

## 故障排查

### 问题1：导入错误

```bash
# 重新安装依赖
pip install -r requirements.txt --upgrade
```

### 问题2：编码错误

确保语料文件使用UTF-8或GBK编码。

### 问题3：内存不足

编辑 `config.json`，减小 `batch_size` 值。

## 下一步

- 查看 `README.md` 了解详细功能
- 查看 `BUILD.md` 了解打包方法
- 查看技术方案 `.cursor/index.mdc`

