"""基础分析器"""
import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple, Any
import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from ..utils.logger import logger

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class BaseAnalyzer:
    """基础分析器（通用统计/可视化）"""
    
    def __init__(self, custom_dimensions: List[str], output_dir: str = "output"):
        """
        初始化基础分析器
        
        Args:
            custom_dimensions: 自定义维度列表
            output_dir: 输出目录
        """
        self.custom_dimensions = custom_dimensions
        self.output_dir = Path(output_dir)
        self.charts_dir = self.output_dir / "charts"
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.charts_dir.mkdir(exist_ok=True, parents=True)
        
        logger.info(f"初始化分析器，自定义维度: {custom_dimensions}")
    
    def calculate_frequency(self, df: pd.DataFrame, tokens_col: str = 'tokens') -> Dict[str, int]:
        """
        计算词频
        
        Args:
            df: 语料DataFrame
            tokens_col: tokens列名
            
        Returns:
            词频字典 {token: count}
        """
        all_tokens = []
        for tokens in df[tokens_col]:
            if isinstance(tokens, list):
                all_tokens.extend(tokens)
        
        frequency = Counter(all_tokens)
        return dict(frequency)
    
    def get_top_k_tokens(self, frequency: Dict[str, int], k: int = 10) -> List[Tuple[str, int]]:
        """
        获取Top K高频词
        
        Args:
            frequency: 词频字典
            k: 返回数量
            
        Returns:
            [(token, count), ...] 排序列表
        """
        return sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:k]
    
    def calculate_dimension_frequency(self, df: pd.DataFrame, tokens_col: str = 'tokens') -> Dict[str, int]:
        """
        计算自定义维度相关词频
        
        Args:
            df: 语料DataFrame
            tokens_col: tokens列名
            
        Returns:
            维度相关词频字典
        """
        # 只统计与维度相关的tokens
        dimension_tokens = []
        for tokens in df[tokens_col]:
            if isinstance(tokens, list):
                # 过滤出与维度相关的token（简化版：包含维度关键词的）
                for token in tokens:
                    if any(dim in token or token in dim for dim in self.custom_dimensions):
                        dimension_tokens.append(token)
        
        frequency = Counter(dimension_tokens)
        return dict(frequency)
    
    def analyze_sentiment(self, df: pd.DataFrame, content_col: str = 'content') -> pd.DataFrame:
        """
        情感分析（正面/中性/负面）
        
        Args:
            df: 语料DataFrame
            content_col: 内容列名
            
        Returns:
            添加sentiment列的DataFrame
        """
        try:
            from snownlp import SnowNLP
            
            def get_sentiment(text: str) -> str:
                """获取情感倾向"""
                try:
                    s = SnowNLP(text)
                    score = s.sentiments
                    if score >= 0.6:
                        return "正面"
                    elif score <= 0.4:
                        return "负面"
                    else:
                        return "中性"
                except:
                    return "中性"
            
            df['sentiment'] = df[content_col].apply(get_sentiment)
            logger.info("情感分析完成")
        except ImportError:
            logger.warning("SnowNLP未安装，跳过情感分析")
            df['sentiment'] = "中性"
        
        return df
    
    def calculate_sentiment_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        计算情感分布
        
        Args:
            df: 语料DataFrame（需包含sentiment列）
            
        Returns:
            情感分布字典 {sentiment: count}
        """
        if 'sentiment' not in df.columns:
            return {}
        
        sentiment_dist = df['sentiment'].value_counts().to_dict()
        return sentiment_dist
    
    def plot_frequency_bar(self, frequency: Dict[str, int], title: str, 
                          filename: str, top_k: int = 10) -> str:
        """
        绘制频次柱状图
        
        Args:
            frequency: 词频字典
            title: 图表标题
            filename: 保存文件名
            top_k: 显示Top K
            
        Returns:
            图表文件路径
        """
        top_items = self.get_top_k_tokens(frequency, k=top_k)
        
        if not top_items:
            logger.warning(f"无数据可绘制: {title}")
            return ""
        
        labels = [item[0] for item in top_items]
        values = [item[1] for item in top_items]
        
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(labels)), values, color='steelblue')
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        plt.xlabel('关键词')
        plt.ylabel('频次')
        plt.title(title)
        plt.tight_layout()
        
        filepath = self.charts_dir / filename
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        logger.info(f"保存柱状图: {filepath}")
        return str(filepath)
    
    def plot_pie_chart(self, distribution: Dict[str, int], title: str, filename: str) -> str:
        """
        绘制饼图
        
        Args:
            distribution: 分布字典
            title: 图表标题
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        if not distribution:
            logger.warning(f"无数据可绘制: {title}")
            return ""
        
        labels = list(distribution.keys())
        values = list(distribution.values())
        
        plt.figure(figsize=(10, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(title)
        plt.axis('equal')
        
        filepath = self.charts_dir / filename
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        logger.info(f"保存饼图: {filepath}")
        return str(filepath)
    
    def plot_sentiment_distribution(self, df: pd.DataFrame, title: str, filename: str) -> str:
        """
        绘制情感分布图
        
        Args:
            df: 语料DataFrame（需包含sentiment列）
            title: 图表标题
            filename: 保存文件名
            
        Returns:
            图表文件路径
        """
        sentiment_dist = self.calculate_sentiment_distribution(df)
        return self.plot_pie_chart(sentiment_dist, title, filename)
    
    def generate_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        生成汇总统计
        
        Args:
            df: 语料DataFrame
            
        Returns:
            统计字典
        """
        stats = {
            "总语料数": len(df),
            "相关语料数": df['is_relevant'].sum() if 'is_relevant' in df.columns else 0,
            "相关占比": f"{(df['is_relevant'].sum() / len(df) * 100):.2f}%" if 'is_relevant' in df.columns and len(df) > 0 else "0%",
        }
        
        # 类型分布
        if 'type' in df.columns:
            type_dist = df['type'].value_counts().to_dict()
            stats["类型分布"] = type_dist
        
        # 情感分布
        if 'sentiment' in df.columns:
            sentiment_dist = self.calculate_sentiment_distribution(df)
            stats["情感分布"] = sentiment_dist
        
        return stats

