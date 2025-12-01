"""
PPT主题生成场景语料分析工具 - 主入口
支持大规模语料分析，自定义维度分析，双场景分析（请求/反馈）
"""
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from data_io.data_loader import DataLoader
from data_io.result_exporter import ResultExporter
from preprocess.cleaner import TextCleaner
from preprocess.tokenizer import Tokenizer
from preprocess.dimension_marker import DimensionMarker
from analyzer.request_analyzer import RequestAnalyzer
from analyzer.feedback_analyzer import FeedbackAnalyzer
from utils.logger import logger


class CorpusAnalyzer:
    """语料分析主控制器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化分析器
        
        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 初始化各模块
        self.data_loader = DataLoader(
            batch_size=self.config["data_loader"]["batch_size"],
            min_content_length=self.config["data_loader"]["min_content_length"]
        )
        
        self.cleaner = TextCleaner()
        
        # 获取配置文件所在目录
        if config_path:
            config_dir = Path(config_path).parent
        else:
            config_dir = Path(__file__).parent / "config"
        
        self.tokenizer = Tokenizer(
            business_dict_path=str(config_dir / "ppt_business_dict.txt"),
            stopwords_path=str(config_dir / "stopwords.txt")
        )
        
        self.dimension_marker = DimensionMarker(
            synonym_dict_path=str(config_dir / "synonym_dict.txt"),
            weight_multiplier=self.config["preprocess"]["custom_dimension_weight_multiplier"]
        )
        
        logger.info("语料分析器初始化完成")
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "config.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logger.info(f"配置文件加载成功: {config_path}")
        return config
    
    def analyze(self, file_path: str, custom_dimensions: List[str], 
               analysis_type: str = "both", output_dir: str = "output") -> Dict[str, Any]:
        """
        执行语料分析
        
        Args:
            file_path: 语料文件路径
            custom_dimensions: 自定义维度列表（如 ["老师", "教学"]）
            analysis_type: 分析类型（"request"=请求, "feedback"=反馈, "both"=双场景）
            output_dir: 输出目录
            
        Returns:
            分析结果字典
        """
        logger.info("="*60)
        logger.info("开始语料分析")
        logger.info(f"文件: {file_path}")
        logger.info(f"自定义维度: {custom_dimensions}")
        logger.info(f"分析类型: {analysis_type}")
        logger.info("="*60)
        
        # 1. 加载数据
        logger.info("\n[步骤 1/5] 加载数据...")
        df_all = self._load_data(file_path)
        
        if df_all is None or len(df_all) == 0:
            logger.error("数据加载失败或数据为空")
            return {}
        
        logger.info(f"数据加载完成，共 {len(df_all)} 条语料")
        
        # 2. 预处理
        logger.info("\n[步骤 2/5] 预处理数据...")
        df_processed = self._preprocess(df_all, custom_dimensions)
        
        if df_processed is None or len(df_processed) == 0:
            logger.error("预处理后数据为空")
            return {}
        
        logger.info(f"预处理完成，剩余 {len(df_processed)} 条有效语料")
        
        # 3. 分析
        logger.info("\n[步骤 3/5] 执行分析...")
        results = self._run_analysis(df_processed, custom_dimensions, analysis_type, output_dir)
        
        # 4. 导出结果
        logger.info("\n[步骤 4/5] 导出结果...")
        self._export_results(results, analysis_type, output_dir)
        
        logger.info("\n[步骤 5/5] 分析完成！")
        logger.info("="*60)
        
        return results
    
    def _load_data(self, file_path: str) -> pd.DataFrame:
        """加载数据"""
        try:
            # 使用小规模加载（适配常规场景）
            df = self.data_loader.load_small_corpus(file_path)
            return df
        except Exception as e:
            logger.error(f"数据加载失败: {str(e)}")
            return None
    
    def _preprocess(self, df: pd.DataFrame, custom_dimensions: List[str]) -> pd.DataFrame:
        """预处理数据"""
        try:
            # 1. 文本清洗
            logger.info("1/3 清洗文本...")
            df = self.cleaner.clean_corpus(df)
            
            # 2. 分词
            logger.info("2/3 分词...")
            df = self.tokenizer.tokenize_corpus(df)
            
            # 3. 维度标记
            logger.info("3/3 标记自定义维度...")
            df = self.dimension_marker.mark_corpus_dimension(df, custom_dimensions)
            
            # 过滤出相关语料
            df_relevant = self.dimension_marker.filter_relevant_corpus(df)
            
            return df_relevant
            
        except Exception as e:
            logger.error(f"预处理失败: {str(e)}")
            return None
    
    def _run_analysis(self, df: pd.DataFrame, custom_dimensions: List[str], 
                     analysis_type: str, output_dir: str) -> Dict[str, Any]:
        """执行分析"""
        results = {
            "维度": custom_dimensions
        }
        
        try:
            # 分割请求和反馈语料
            df_request = df[df['type'].str.contains('请求|request', case=False, na=False)] if 'type' in df.columns else df
            df_feedback = df[df['type'].str.contains('反馈|feedback', case=False, na=False)] if 'type' in df.columns else pd.DataFrame()
            
            # 如果没有type字段或无法区分，则全部视为请求语料
            if len(df_request) == 0 and len(df_feedback) == 0:
                logger.warning("无type字段或无法区分请求/反馈，全部视为请求语料")
                df_request = df
            
            logger.info(f"请求语料: {len(df_request)} 条, 反馈语料: {len(df_feedback)} 条")
            
            # 分析请求语料
            if analysis_type in ["request", "both"] and len(df_request) > 0:
                logger.info("分析请求语料...")
                request_analyzer = RequestAnalyzer(custom_dimensions, output_dir)
                results["请求分析"] = request_analyzer.analyze(df_request)
            
            # 分析反馈语料
            if analysis_type in ["feedback", "both"] and len(df_feedback) > 0:
                logger.info("分析反馈语料...")
                feedback_analyzer = FeedbackAnalyzer(custom_dimensions, output_dir)
                results["反馈分析"] = feedback_analyzer.analyze(df_feedback)
            
            # 整体统计
            results["基础统计"] = {
                "总语料数": len(df),
                "相关语料数": len(df),
                "相关占比": "100%",
                "类型分布": {
                    "请求语料": len(df_request),
                    "反馈语料": len(df_feedback)
                }
            }
            
            return results
            
        except Exception as e:
            logger.error(f"分析失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return results
    
    def _export_results(self, results: Dict[str, Any], analysis_type: str, output_dir: str) -> None:
        """导出结果"""
        try:
            exporter = ResultExporter(output_dir)
            filepaths = exporter.export_all(results, analysis_type)
            
            logger.info("导出完成:")
            for format_type, filepath in filepaths.items():
                logger.info(f"  - {format_type}: {filepath}")
                
        except Exception as e:
            logger.error(f"导出失败: {str(e)}")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PPT语料分析工具")
    parser.add_argument("file", help="语料文件路径 (.xlsx 或 .csv)")
    parser.add_argument("--dimensions", "-d", required=True, 
                       help="自定义维度（多个用逗号分隔，如：老师,教学）")
    parser.add_argument("--type", "-t", choices=["request", "feedback", "both"], 
                       default="both", help="分析类型（默认：both）")
    parser.add_argument("--output", "-o", default="output", 
                       help="输出目录（默认：output）")
    parser.add_argument("--config", "-c", default=None, 
                       help="配置文件路径（可选）")
    
    args = parser.parse_args()
    
    # 解析自定义维度
    dimensions = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    
    if not dimensions:
        logger.error("请至少指定一个自定义维度")
        sys.exit(1)
    
    # 创建分析器并执行
    analyzer = CorpusAnalyzer(config_path=args.config)
    results = analyzer.analyze(
        file_path=args.file,
        custom_dimensions=dimensions,
        analysis_type=args.type,
        output_dir=args.output
    )
    
    if results:
        logger.info("\n分析成功完成！")
        logger.info(f"结果已保存到: {args.output}")
    else:
        logger.error("\n分析失败")
        sys.exit(1)


if __name__ == "__main__":
    main()

