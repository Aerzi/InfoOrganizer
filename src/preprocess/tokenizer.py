"""分词模块"""
import jieba
import pandas as pd
from pathlib import Path
from typing import List, Set
from ..utils.logger import logger


class Tokenizer:
    """分词器（支持PPT场景专属词典）"""
    
    def __init__(self, business_dict_path: str = None, stopwords_path: str = None):
        """
        初始化分词器
        
        Args:
            business_dict_path: PPT业务词典路径
            stopwords_path: 停用词词典路径
        """
        self.business_dict_path = business_dict_path
        self.stopwords_path = stopwords_path
        self.stopwords: Set[str] = set()
        
        # 加载业务词典
        if business_dict_path:
            self._load_business_dict(business_dict_path)
        
        # 加载停用词
        if stopwords_path:
            self._load_stopwords(stopwords_path)
    
    def _load_business_dict(self, dict_path: str) -> None:
        """
        加载PPT业务词典
        
        Args:
            dict_path: 词典文件路径
        """
        dict_file = Path(dict_path)
        if dict_file.exists():
            try:
                with open(dict_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            jieba.add_word(word)
                logger.info(f"成功加载PPT业务词典: {dict_path}")
            except Exception as e:
                logger.warning(f"加载业务词典失败: {str(e)}")
        else:
            logger.warning(f"业务词典文件不存在: {dict_path}")
    
    def _load_stopwords(self, stopwords_path: str) -> None:
        """
        加载停用词
        
        Args:
            stopwords_path: 停用词文件路径
        """
        stopwords_file = Path(stopwords_path)
        if stopwords_file.exists():
            try:
                with open(stopwords_file, 'r', encoding='utf-8') as f:
                    self.stopwords = {line.strip() for line in f if line.strip()}
                logger.info(f"成功加载停用词，共 {len(self.stopwords)} 个")
            except Exception as e:
                logger.warning(f"加载停用词失败: {str(e)}")
        else:
            logger.warning(f"停用词文件不存在: {stopwords_path}")
    
    def tokenize(self, text: str, remove_stopwords: bool = True) -> List[str]:
        """
        分词
        
        Args:
            text: 待分词文本
            remove_stopwords: 是否过滤停用词
            
        Returns:
            分词结果列表
        """
        if not text or not isinstance(text, str):
            return []
        
        # jieba分词
        tokens = list(jieba.cut(text))
        
        # 过滤停用词
        if remove_stopwords and self.stopwords:
            tokens = [token for token in tokens if token not in self.stopwords]
        
        # 过滤空白和单字符（保留数字和有意义的单字）
        tokens = [
            token.strip() for token in tokens 
            if token.strip() and (len(token.strip()) > 1 or token.isdigit())
        ]
        
        return tokens
    
    def tokenize_corpus(self, df: pd.DataFrame, content_col: str = 'content', 
                       remove_stopwords: bool = True) -> pd.DataFrame:
        """
        批量分词
        
        Args:
            df: 语料DataFrame
            content_col: 内容列名
            remove_stopwords: 是否过滤停用词
            
        Returns:
            添加tokens列的DataFrame
        """
        logger.info(f"开始分词，共 {len(df)} 条")
        
        df['tokens'] = df[content_col].apply(
            lambda x: self.tokenize(x, remove_stopwords=remove_stopwords)
        )
        
        # 过滤分词后为空的行
        original_count = len(df)
        df = df[df['tokens'].apply(len) > 0]
        filtered_count = original_count - len(df)
        
        logger.info(f"分词完成，过滤掉 {filtered_count} 条空结果，剩余 {len(df)} 条")
        
        return df

