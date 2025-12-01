"""自定义维度标记模块"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Set
from ..utils.logger import logger


class DimensionMarker:
    """自定义维度标记器（通用化，支持任意维度）"""
    
    def __init__(self, synonym_dict_path: str = None, weight_multiplier: float = 3.0):
        """
        初始化维度标记器
        
        Args:
            synonym_dict_path: 同义词词典路径
            weight_multiplier: 权重提升倍数
        """
        self.synonym_dict_path = synonym_dict_path
        self.weight_multiplier = weight_multiplier
        self.synonym_dict: Dict[str, Set[str]] = {}
        
        # 加载同义词词典
        if synonym_dict_path:
            self._load_synonym_dict(synonym_dict_path)
    
    def _load_synonym_dict(self, dict_path: str) -> None:
        """
        加载同义词词典
        
        格式：主词=同义词1,同义词2,同义词3
        
        Args:
            dict_path: 词典文件路径
        """
        dict_file = Path(dict_path)
        if dict_file.exists():
            try:
                with open(dict_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        # 跳过空行和注释
                        if not line or line.startswith('#'):
                            continue
                        
                        # 解析格式：主词=同义词1,同义词2
                        if '=' in line:
                            main_word, synonyms = line.split('=', 1)
                            main_word = main_word.strip()
                            synonym_list = [s.strip() for s in synonyms.split(',') if s.strip()]
                            
                            # 存储同义词关系（主词也包含在集合中）
                            self.synonym_dict[main_word] = set([main_word] + synonym_list)
                
                logger.info(f"成功加载同义词词典: {dict_path}，共 {len(self.synonym_dict)} 组同义词")
            except Exception as e:
                logger.warning(f"加载同义词词典失败: {str(e)}")
        else:
            logger.warning(f"同义词词典文件不存在: {dict_path}")
    
    def expand_dimensions(self, custom_dimensions: List[str]) -> Set[str]:
        """
        扩展自定义维度（加入同义词）
        
        Args:
            custom_dimensions: 用户输入的自定义维度列表
            
        Returns:
            扩展后的维度集合（包含同义词）
        """
        expanded = set()
        
        for dim in custom_dimensions:
            dim = dim.strip()
            if not dim:
                continue
            
            # 添加原始维度
            expanded.add(dim)
            
            # 添加同义词
            if dim in self.synonym_dict:
                expanded.update(self.synonym_dict[dim])
        
        logger.info(f"维度扩展: {custom_dimensions} -> {len(expanded)} 个关键词")
        return expanded
    
    def mark_dimension_weight(self, tokens: List[str], custom_dimensions: List[str]) -> Dict[str, float]:
        """
        通用化自定义维度权重标记
        
        Args:
            tokens: 分词后的tokens
            custom_dimensions: 用户输入的自定义维度/关键词列表（如["老师", "教学"]）
            
        Returns:
            带权重的token字典 {token: weight}
        """
        # 扩展维度（包含同义词）
        expanded_dimensions = self.expand_dimensions(custom_dimensions)
        
        weight_dict = {}
        for token in tokens:
            # 匹配自定义维度或其同义词（通用逻辑，无硬编码）
            if token in expanded_dimensions:
                weight_dict[token] = self.weight_multiplier  # 目标维度权重提升
            else:
                weight_dict[token] = 1.0  # 普通词基础权重
        
        return weight_dict
    
    def check_dimension_relevance(self, tokens: List[str], custom_dimensions: List[str]) -> bool:
        """
        检查语料是否与自定义维度相关
        
        Args:
            tokens: 分词后的tokens
            custom_dimensions: 自定义维度列表
            
        Returns:
            是否相关
        """
        # 扩展维度
        expanded_dimensions = self.expand_dimensions(custom_dimensions)
        
        # 检查是否有任何token匹配维度
        return any(token in expanded_dimensions for token in tokens)
    
    def mark_corpus_dimension(self, df: pd.DataFrame, custom_dimensions: List[str], 
                             tokens_col: str = 'tokens') -> pd.DataFrame:
        """
        批量标记语料的维度权重
        
        Args:
            df: 语料DataFrame（需包含tokens列）
            custom_dimensions: 自定义维度列表
            tokens_col: tokens列名
            
        Returns:
            添加dimension_weights和is_relevant列的DataFrame
        """
        logger.info(f"开始标记自定义维度: {custom_dimensions}")
        
        # 标记权重
        df['dimension_weights'] = df[tokens_col].apply(
            lambda tokens: self.mark_dimension_weight(tokens, custom_dimensions)
        )
        
        # 标记是否相关
        df['is_relevant'] = df[tokens_col].apply(
            lambda tokens: self.check_dimension_relevance(tokens, custom_dimensions)
        )
        
        relevant_count = df['is_relevant'].sum()
        logger.info(f"维度标记完成，{len(df)} 条语料中有 {relevant_count} 条与自定义维度相关")
        
        return df
    
    def filter_relevant_corpus(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        过滤出与自定义维度相关的语料
        
        Args:
            df: 语料DataFrame（需包含is_relevant列）
            
        Returns:
            过滤后的DataFrame
        """
        if 'is_relevant' not in df.columns:
            logger.warning("DataFrame缺少is_relevant列，无法过滤")
            return df
        
        original_count = len(df)
        df_relevant = df[df['is_relevant'] == True].copy()
        filtered_count = original_count - len(df_relevant)
        
        logger.info(f"过滤出与维度相关的语料: {len(df_relevant)} 条（过滤掉 {filtered_count} 条不相关）")
        
        return df_relevant

