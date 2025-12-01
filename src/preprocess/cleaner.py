"""文本清洗模块"""
import re
import pandas as pd
from typing import List
from ..utils.logger import logger


class TextCleaner:
    """文本清洗器（通用化，无维度绑定）"""
    
    def __init__(self):
        """初始化清洗器"""
        # 特殊符号清理规则
        self.special_chars_pattern = re.compile(r'[^\w\s\u4e00-\u9fa5.,!?;:，。！？；：、]')
        # 多余空格清理规则
        self.whitespace_pattern = re.compile(r'\s+')
        # 数字转换规则
        self.number_mapping = {
            '0': '零', '1': '一', '2': '二', '3': '三', '4': '四',
            '5': '五', '6': '六', '7': '七', '8': '八', '9': '九',
            '10': '十'
        }
    
    def clean_special_chars(self, text: str) -> str:
        """
        清理特殊符号
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        # 保留中文、英文、数字和基础标点
        return self.special_chars_pattern.sub(' ', text)
    
    def normalize_whitespace(self, text: str) -> str:
        """
        标准化空格
        
        Args:
            text: 原始文本
            
        Returns:
            标准化后的文本
        """
        # 合并多个空格为一个
        text = self.whitespace_pattern.sub(' ', text)
        return text.strip()
    
    def normalize_numbers(self, text: str, convert_chinese: bool = False) -> str:
        """
        标准化数字
        
        Args:
            text: 原始文本
            convert_chinese: 是否将数字转为中文（可选）
            
        Returns:
            标准化后的文本
        """
        if convert_chinese:
            # 将常见数字转为中文（可选功能，默认不开启）
            for num, chinese in self.number_mapping.items():
                text = text.replace(num, chinese)
        return text
    
    def remove_duplicates(self, texts: List[str]) -> List[str]:
        """
        去除重复文本
        
        Args:
            texts: 文本列表
            
        Returns:
            去重后的文本列表
        """
        seen = set()
        unique_texts = []
        for text in texts:
            text_normalized = text.strip().lower()
            if text_normalized and text_normalized not in seen:
                seen.add(text_normalized)
                unique_texts.append(text)
        return unique_texts
    
    def clean_text(self, text: str, remove_chars: bool = True, 
                   normalize_space: bool = True, convert_numbers: bool = False) -> str:
        """
        综合清洗文本
        
        Args:
            text: 原始文本
            remove_chars: 是否清理特殊符号
            normalize_space: 是否标准化空格
            convert_numbers: 是否转换数字为中文
            
        Returns:
            清洗后的文本
        """
        if not text or not isinstance(text, str):
            return ""
        
        # 清理特殊符号
        if remove_chars:
            text = self.clean_special_chars(text)
        
        # 标准化空格
        if normalize_space:
            text = self.normalize_whitespace(text)
        
        # 转换数字
        if convert_numbers:
            text = self.normalize_numbers(text, convert_chinese=True)
        
        return text
    
    def clean_corpus(self, df: pd.DataFrame, content_col: str = 'content') -> pd.DataFrame:
        """
        批量清洗语料
        
        Args:
            df: 语料DataFrame
            content_col: 内容列名
            
        Returns:
            清洗后的DataFrame
        """
        logger.info(f"开始清洗语料，共 {len(df)} 条")
        
        # 清洗文本
        df[content_col] = df[content_col].apply(
            lambda x: self.clean_text(x) if isinstance(x, str) else ""
        )
        
        # 过滤清洗后为空的文本
        original_count = len(df)
        df = df[df[content_col].str.strip() != '']
        filtered_count = original_count - len(df)
        
        logger.info(f"清洗完成，过滤掉 {filtered_count} 条空文本，剩余 {len(df)} 条")
        
        return df

