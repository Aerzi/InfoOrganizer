"""反馈语料分析器"""
import pandas as pd
from typing import Dict, List, Any
from .base_analyzer import BaseAnalyzer
from ..utils.logger import logger


class FeedbackAnalyzer(BaseAnalyzer):
    """反馈语料分析器（聚焦效果反馈，适配自定义维度）"""
    
    def __init__(self, custom_dimensions: List[str], output_dir: str = "output"):
        """
        初始化反馈语料分析器
        
        Args:
            custom_dimensions: 自定义维度列表
            output_dir: 输出目录
        """
        super().__init__(custom_dimensions, output_dir)
        logger.info("初始化反馈语料分析器")
    
    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        综合分析反馈语料
        
        Args:
            df: 反馈语料DataFrame
            
        Returns:
            分析结果字典
        """
        logger.info(f"开始分析反馈语料，共 {len(df)} 条")
        
        results = {
            "维度": self.custom_dimensions,
            "分析类型": "反馈语料（效果反馈）"
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
        
        # 4. 问题分类分析
        logger.info("进行问题分类分析...")
        problem_categories = self._classify_problems(df)
        results["问题分类"] = problem_categories
        
        # 5. 关联特征分析
        logger.info("进行关联特征分析...")
        associations = self._analyze_associations(df)
        results["关联特征"] = associations
        
        # 6. 场景分析
        logger.info("进行场景分析...")
        scenes = self._analyze_scenes(df)
        results["场景分布"] = scenes
        
        # 7. 优化建议生成
        logger.info("生成优化建议...")
        suggestions = self._generate_suggestions(df, problem_categories, sentiment_dist)
        results["优化建议"] = suggestions
        
        # 8. 生成可视化图表
        logger.info("生成可视化图表...")
        self._generate_charts(df, frequency, dim_frequency, sentiment_dist)
        
        logger.info("反馈语料分析完成")
        return results
    
    def _classify_problems(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        问题分类（基于关键词规则）
        
        Args:
            df: 语料DataFrame
            
        Returns:
            问题分类统计
        """
        # 定义问题关键词
        problem_keywords = {
            "操作体验": ["操作", "复杂", "困难", "不会用", "难用", "麻烦"],
            "内容适配": ["内容", "不合适", "不适配", "不符合", "缺少"],
            "格式问题": ["格式", "排版", "错乱", "变形", "显示"],
            "功能缺失": ["功能", "缺少", "没有", "不支持", "无法"],
            "性能问题": ["慢", "卡", "加载", "延迟", "响应"],
            "效果满意": ["好", "满意", "不错", "很棒", "喜欢", "适合"]
        }
        
        problem_counts = {category: 0 for category in problem_keywords.keys()}
        
        for _, row in df.iterrows():
            content = str(row.get('content', ''))
            tokens = row.get('tokens', [])
            
            # 检查每个问题类别
            for category, keywords in problem_keywords.items():
                if any(kw in content or kw in tokens for kw in keywords):
                    problem_counts[category] += 1
        
        return problem_counts
    
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
            "课堂教学": ["课堂", "上课", "教学", "讲课", "学生", "老师"],
            "工作会议": ["工作", "会议", "汇报", "报告", "总结"],
            "项目演示": ["项目", "展示", "演示", "介绍", "方案"],
            "培训学习": ["培训", "学习", "教程", "指导"],
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
    
    def _generate_suggestions(self, df: pd.DataFrame, problem_categories: Dict[str, int], 
                             sentiment_dist: Dict[str, int]) -> List[str]:
        """
        基于反馈生成优化建议
        
        Args:
            df: 语料DataFrame
            problem_categories: 问题分类统计
            sentiment_dist: 情感分布
            
        Returns:
            优化建议列表
        """
        suggestions = []
        
        # 根据负面情感比例
        total = sum(sentiment_dist.values())
        negative_ratio = sentiment_dist.get("负面", 0) / total if total > 0 else 0
        
        if negative_ratio > 0.3:
            suggestions.append(f"负面反馈占比较高({negative_ratio*100:.1f}%)，需要重点关注用户满意度问题")
        
        # 根据主要问题类别
        if problem_categories:
            top_problem = max(problem_categories.items(), key=lambda x: x[1])
            if top_problem[1] > 0:
                suggestions.append(f"主要问题集中在「{top_problem[0]}」({top_problem[1]}条)，建议优先优化")
        
        # 针对自定义维度的建议
        for dim in self.custom_dimensions:
            dim_related = df[df['tokens'].apply(
                lambda tokens: any(dim in token or token == dim for token in tokens)
            )]
            
            if len(dim_related) > 0:
                # 分析该维度的情感倾向
                if 'sentiment' in dim_related.columns:
                    dim_negative = (dim_related['sentiment'] == '负面').sum()
                    dim_negative_ratio = dim_negative / len(dim_related)
                    
                    if dim_negative_ratio > 0.4:
                        suggestions.append(
                            f"针对「{dim}」维度的反馈中负面占比{dim_negative_ratio*100:.1f}%，"
                            f"建议深入分析该维度相关的PPT功能/场景优化方向"
                        )
        
        # 通用建议
        if not suggestions:
            suggestions.append("整体反馈较为积极，建议继续保持并收集更多用户意见")
        
        return suggestions
    
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
            f"反馈语料-总体高频词Top10",
            f"{dim_str}_反馈_总体词频.png"
        )
        
        # 2. 维度相关词频柱状图
        self.plot_frequency_bar(
            dim_frequency,
            f"反馈语料-{','.join(self.custom_dimensions)}相关高频词Top10",
            f"{dim_str}_反馈_维度词频.png"
        )
        
        # 3. 情感分布饼图
        self.plot_sentiment_distribution(
            df,
            f"反馈语料-情感分布",
            f"{dim_str}_反馈_情感分布.png"
        )

