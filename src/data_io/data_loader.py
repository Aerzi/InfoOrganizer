"""大规模数据加载模块"""
import pandas as pd
import dask.dataframe as dd
from pathlib import Path
from typing import Iterator, Union
from ..utils.logger import logger


class DataLoader:
    """大规模语料数据加载器"""
    
    def __init__(self, batch_size: int = 10000, min_content_length: int = 2):
        """
        初始化数据加载器
        
        Args:
            batch_size: 批次大小
            min_content_length: 最小内容长度
        """
        self.batch_size = batch_size
        self.min_content_length = min_content_length
    
    def load_large_corpus(self, file_path: Union[str, Path]) -> Iterator[pd.DataFrame]:
        """
        加载大规模语料，返回分批迭代器（通用化，无维度绑定）
        
        Args:
            file_path: 语料文件路径（支持 .xlsx, .csv）
            
        Yields:
            分批加载的DataFrame
            
        Raises:
            ValueError: 文件格式不支持或缺少必需字段
            FileNotFoundError: 文件不存在
        """
        file_path = Path(file_path)
        
        # 检查文件是否存在
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        logger.info(f"开始加载语料文件: {file_path}")
        
        # 根据文件格式选择读取方式
        try:
            if file_path.suffix.lower() == '.xlsx':
                # Excel文件使用dask读取
                ddf = dd.read_excel(
                    str(file_path),
                    engine='openpyxl'
                )
            elif file_path.suffix.lower() == '.csv':
                # CSV文件使用dask读取，尝试多种编码
                encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
                ddf = None
                for encoding in encodings:
                    try:
                        ddf = dd.read_csv(
                            str(file_path),
                            encoding=encoding,
                            low_memory=False
                        )
                        logger.info(f"成功使用编码 {encoding} 读取CSV文件")
                        break
                    except (UnicodeDecodeError, Exception):
                        continue
                
                if ddf is None:
                    raise ValueError(f"无法读取CSV文件，尝试了编码: {encodings}")
            else:
                raise ValueError(f"不支持的文件格式: {file_path.suffix}")
            
            # 校验核心字段
            required_cols = ["content"]
            if not all(col in ddf.columns for col in required_cols):
                raise ValueError(f"语料文件必须包含核心字段：{required_cols}，当前字段：{list(ddf.columns)}")
            
            logger.info(f"文件列名: {list(ddf.columns)}")
            
            # 计算总行数
            total_rows = len(ddf)
            logger.info(f"总语料数: {total_rows}")
            
            # 分批加载并过滤无效数据
            batch_count = 0
            for i in range(0, total_rows, self.batch_size):
                batch = ddf.iloc[i:i+self.batch_size].compute()  # 仅加载当前批次到内存
                
                # 过滤空值/无效行（通用规则，无维度绑定）
                original_count = len(batch)
                batch = batch[
                    batch['content'].notna() 
                    & (batch['content'].astype(str).str.strip() != '')
                    & (batch['content'].astype(str).str.len() >= self.min_content_length)
                ]
                
                # 确保content字段为字符串类型
                batch['content'] = batch['content'].astype(str)
                
                # 如果有type字段，确保为字符串类型
                if 'type' in batch.columns:
                    batch['type'] = batch['type'].fillna('unknown').astype(str)
                
                filtered_count = original_count - len(batch)
                batch_count += 1
                
                logger.info(f"批次 {batch_count}: 原始 {original_count} 条，过滤 {filtered_count} 条，有效 {len(batch)} 条")
                
                if len(batch) > 0:
                    yield batch
            
            logger.info(f"数据加载完成，共处理 {batch_count} 个批次")
            
        except Exception as e:
            logger.error(f"加载文件时出错: {str(e)}")
            raise
    
    def load_small_corpus(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        加载小规模语料（一次性加载到内存）
        
        Args:
            file_path: 语料文件路径
            
        Returns:
            完整的DataFrame
        """
        file_path = Path(file_path)
        
        logger.info(f"加载小规模语料文件: {file_path}")
        
        try:
            if file_path.suffix.lower() == '.xlsx':
                df = pd.read_excel(file_path, engine='openpyxl')
            elif file_path.suffix.lower() == '.csv':
                # 尝试多种编码
                encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
                df = None
                for encoding in encodings:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        logger.info(f"成功使用编码 {encoding} 读取CSV文件")
                        break
                    except (UnicodeDecodeError, Exception):
                        continue
                
                if df is None:
                    raise ValueError(f"无法读取CSV文件，尝试了编码: {encodings}")
            else:
                raise ValueError(f"不支持的文件格式: {file_path.suffix}")
            
            # 校验核心字段
            required_cols = ["content"]
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"语料文件必须包含核心字段：{required_cols}，当前字段：{list(df.columns)}")
            
            # 过滤无效数据
            original_count = len(df)
            df = df[
                df['content'].notna() 
                & (df['content'].astype(str).str.strip() != '')
                & (df['content'].astype(str).str.len() >= self.min_content_length)
            ]
            
            # 确保content字段为字符串类型
            df['content'] = df['content'].astype(str)
            
            # 如果有type字段，确保为字符串类型
            if 'type' in df.columns:
                df['type'] = df['type'].fillna('unknown').astype(str)
            
            filtered_count = original_count - len(df)
            logger.info(f"原始 {original_count} 条，过滤 {filtered_count} 条，有效 {len(df)} 条")
            
            return df
            
        except Exception as e:
            logger.error(f"加载文件时出错: {str(e)}")
            raise
    
    def auto_load(self, file_path: Union[str, Path], large_threshold: int = 50000) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """
        自动选择加载方式（根据文件大小）
        
        Args:
            file_path: 语料文件路径
            large_threshold: 大规模阈值（超过此行数使用分批加载）
            
        Returns:
            DataFrame 或分批迭代器
        """
        file_path = Path(file_path)
        
        # 简单估算：通过文件大小判断（粗略估计）
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        
        # 估算行数（假设每行平均1KB）
        estimated_rows = file_size_mb * 1000
        
        if estimated_rows > large_threshold:
            logger.info(f"检测到大规模文件（估算 {estimated_rows:.0f} 行），使用分批加载")
            return self.load_large_corpus(file_path)
        else:
            logger.info(f"检测到小规模文件（估算 {estimated_rows:.0f} 行），使用一次性加载")
            return self.load_small_corpus(file_path)

