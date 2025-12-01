"""请求语料分析器"""
import pandas as pd
from typing import Dict, List, Any
from .base_analyzer import BaseAnalyzer
from ..utils.logger import logger


class RequestAnalyzer(BaseAnalyzer):
    """请求语料分析器（聚焦需求分析，适配自定义维度）"""
    
    def __init__(self, custom_dimensions: List[str], output_dir: str = "output"):
        """
        初始化请求语料分析器
        
        Args:
            custom_dimensions: 自定义维度列表
            output_dir: 输出目录
        """
        super().__init__(custom_dimensions, output_dir)
        logger.info("初始化请求语料分析器")
    
    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        综合分析请求语料
        
        Args:
            df: 请求语料DataFrame
            
        Returns:
            分析结果字典
        """
        logger.info(f"开始分析请求语料，共 {len(df)} 条")
        
        results = {
            "维度": self.custom_dimensions,
            "分析类型": "请求语料（需求分析）"
        }
        
        # 1. 基础统计
        results["基础统计"] = self.generate_summary_stats(df)
        
        # 2. 频次分析
        logger.info("进行频次分析...")
        frequency = self.calculate_frequency(df)
        results["总体词频Top10"] = self.get_top_k_tokens(frequency, k=10)
        
        # 维度相关词频
        dim_frequency = self.calculate_dimension_frequency(df)
        results["维度相关词频Top10"] = self.get_top_k_tokens(dim_frequency, k=10)
        
        # 3. 情感分析
        logger.info("进行情感分析...")
        df = self.analyze_sentiment(df)
        sentiment_dist = self.calculate_sentiment_distribution(df)
        results["情感分布"] = sentiment_dist
        
        # 4. 需求分类分析（基于高频词推断）
        logger.info("进行需求分类分析...")
        demand_categories = self._classify_demands(df)
        results["需求分类"] = demand_categories
        
        # 5. 关联特征分析
        logger.info("进行关联特征分析...")
        associations = self._analyze_associations(df)
        results["关联特征"] = associations
        
        # 6. 场景分析
        logger.info("进行场景分析...")
        scenes = self._analyze_scenes(df)
        results["场景分布"] = scenes
        
        # 7. 生成可视化图表
        logger.info("生成可视化图表...")
        self._generate_charts(df, frequency, dim_frequency, sentiment_dist)
        
        logger.info("请求语料分析完成")
        return results
    
    def _classify_demands(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        需求分类（基于关键词规则）
        
        Args:
            df: 语料DataFrame
            
        Returns:
            需求分类统计
        """
        # 定义需求关键词
        demand_keywords = {
            "模板定制": ["模板", "定制", "样式", "风格", "主题"],
            "内容模块": ["内容", "模块", "功能", "添加", "新增"],
            "格式适配": ["格式", "适配", "兼容", "导出", "排版"],
            "页数相关": ["页数", "页面", "幻灯片", "多少页"],
            "操作简化": ["简单", "容易", "方便", "快速", "操作"]
        }
        
        demand_counts = {category: 0 for category in demand_keywords.keys()}
        
        for _, row in df.iterrows():
            content = str(row.get('content', ''))
            tokens = row.get('tokens', [])
            
            # 检查每个需求类别
            for category, keywords in demand_keywords.items():
                if any(kw in content or kw in tokens for kw in keywords):
                    demand_counts[category] += 1
        
        return demand_counts
    
    def _analyze_associations(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        分析自定义维度的关联特征
        
        Args:
            df: 语料DataFrame
            
        Returns:
            关联特征字典
        """
        associations = {}
        
        for dim in self.custom_dimensions:
            # 找出包含该维度的语料
            dim_related = df[df['tokens'].apply(
                lambda tokens: any(dim in token or token == dim for token in tokens)
            )]
            
            if len(dim_related) == 0:
                associations[dim] = []
                continue
            
            # 统计与该维度共现的高频词
            all_tokens = []
            for tokens in dim_related['tokens']:
                all_tokens.extend([t for t in tokens if t != dim])
            
            from collections import Counter
            top_associated = Counter(all_tokens).most_common(5)
            associations[dim] = [word for word, count in top_associated]
        
        return associations
    
    def _analyze_scenes(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        分析PPT使用场景
        
        Args:
            df: 语料DataFrame
            
        Returns:
            场景分布统计
        """
        # 定义场景关键词
        scene_keywords = {
            "课堂演示": ["课堂", "上课", "教学", "讲课", "学生"],
            "工作汇报": ["工作", "汇报", "总结", "报告", "会议"],
            "项目展示": ["项目", "展示", "演示", "介绍", "方案"],
            "培训材料": ["培训", "学习", "教程", "指导"],
            "其他": []
        }
        
        scene_counts = {scene: 0 for scene in scene_keywords.keys()}
        
        for _, row in df.iterrows():
            content = str(row.get('content', ''))
            tokens = row.get('tokens', [])
            
            matched = False
            # 检查每个场景
            for scene, keywords in scene_keywords.items():
                if scene == "其他":
                    continue
                if any(kw in content or kw in tokens for kw in keywords):
                    scene_counts[scene] += 1
                    matched = True
                    break
            
            if not matched:
                scene_counts["其他"] += 1
        
        return scene_counts
    
    def _generate_charts(self, df: pd.DataFrame, frequency: Dict[str, int], 
                        dim_frequency: Dict[str, int], sentiment_dist: Dict[str, int]) -> None:
        """
        生成所有图表
        
        Args:
            df: 语料DataFrame
            frequency: 总体词频
            dim_frequency: 维度相关词频
            sentiment_dist: 情感分布
        """
        dim_str = "_".join(self.custom_dimensions[:2])  # 使用前2个维度作为文件名
        
        # 1. 总体词频柱状图
        self.plot_frequency_bar(
            frequency, 
            f"请求语料-总体高频词Top10",
            f"{dim_str}_请求_总体词频.png"
        )
        
        # 2. 维度相关词频柱状图
        self.plot_frequency_bar(
            dim_frequency,
            f"请求语料-{','.join(self.custom_dimensions)}相关高频词Top10",
            f"{dim_str}_请求_维度词频.png"
        )
        
        # 3. 情感分布饼图
        self.plot_sentiment_distribution(
            df,
            f"请求语料-情感分布",
            f"{dim_str}_请求_情感分布.png"
        )

