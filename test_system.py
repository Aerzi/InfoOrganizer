"""测试脚本 - 验证系统是否正常工作"""
import sys
import os
from pathlib import Path

# 设置UTF-8输出（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """测试所有模块是否能正常导入"""
    print("测试模块导入...")
    
    try:
        from data_io.data_loader import DataLoader
        print("✓ DataLoader 导入成功")
        
        from data_io.result_exporter import ResultExporter
        print("✓ ResultExporter 导入成功")
        
        from preprocess.cleaner import TextCleaner
        print("✓ TextCleaner 导入成功")
        
        from preprocess.tokenizer import Tokenizer
        print("✓ Tokenizer 导入成功")
        
        from preprocess.dimension_marker import DimensionMarker
        print("✓ DimensionMarker 导入成功")
        
        from analyzer.base_analyzer import BaseAnalyzer
        print("✓ BaseAnalyzer 导入成功")
        
        from analyzer.request_analyzer import RequestAnalyzer
        print("✓ RequestAnalyzer 导入成功")
        
        from analyzer.feedback_analyzer import FeedbackAnalyzer
        print("✓ FeedbackAnalyzer 导入成功")
        
        from utils.logger import logger
        print("✓ Logger 导入成功")
        
        from utils.cache import cache_manager
        print("✓ CacheManager 导入成功")
        
        print("\n所有模块导入成功！")
        return True
        
    except ImportError as e:
        print(f"\n✗ 模块导入失败: {e}")
        return False


def test_dependencies():
    """测试依赖库是否安装"""
    print("\n测试依赖库...")
    
    dependencies = [
        "pandas",
        "dask",
        "jieba",
        "snownlp",
        "matplotlib",
        "seaborn",
        "openpyxl",
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} 已安装")
        except ImportError:
            print(f"✗ {dep} 未安装")
            missing.append(dep)
    
    if missing:
        print(f"\n缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n所有依赖已安装！")
        return True


def test_config_files():
    """测试配置文件是否存在"""
    print("\n测试配置文件...")
    
    config_dir = Path(__file__).parent / "src" / "config"
    required_files = [
        "config.json",
        "ppt_business_dict.txt",
        "stopwords.txt",
        "synonym_dict.txt"
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = config_dir / filename
        if filepath.exists():
            print(f"✓ {filename} 存在")
        else:
            print(f"✗ {filename} 不存在")
            all_exist = False
    
    if all_exist:
        print("\n所有配置文件齐全！")
    else:
        print("\n部分配置文件缺失！")
    
    return all_exist


def test_basic_functionality():
    """测试基础功能"""
    print("\n测试基础功能...")
    
    try:
        from preprocess.cleaner import TextCleaner
        from preprocess.tokenizer import Tokenizer
        
        # 测试清洗
        cleaner = TextCleaner()
        text = "  测试文本！！！  "
        cleaned = cleaner.clean_text(text)
        print(f"✓ 文本清洗: '{text}' -> '{cleaned}'")
        
        # 测试分词
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("这是一个测试文本")
        print(f"✓ 分词: {tokens}")
        
        print("\n基础功能测试通过！")
        return True
        
    except Exception as e:
        print(f"\n✗ 基础功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("="*60)
    print("PPT语料分析工具 - 系统测试")
    print("="*60)
    
    results = []
    
    # 1. 测试依赖
    results.append(("依赖库检查", test_dependencies()))
    
    # 2. 测试导入
    results.append(("模块导入", test_imports()))
    
    # 3. 测试配置
    results.append(("配置文件", test_config_files()))
    
    # 4. 测试基础功能
    results.append(("基础功能", test_basic_functionality()))
    
    # 汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ 所有测试通过！系统可以正常使用。")
        print("\n快速开始:")
        print("  python src/main.py --help")
        print("  python src/gui.py")
    else:
        print("✗ 部分测试失败，请检查上述错误信息。")
    print("="*60)


if __name__ == "__main__":
    main()

