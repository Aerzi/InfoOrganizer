"""缓存工具模块"""
import json
import hashlib
from pathlib import Path
from typing import Any, Optional
import pickle


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: str = ".cache"):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, content: str, dimensions: list) -> str:
        """
        生成缓存键
        
        Args:
            content: 内容
            dimensions: 自定义维度列表
            
        Returns:
            缓存键（MD5）
        """
        key_str = f"{content}_{','.join(sorted(dimensions))}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()
    
    def get(self, content: str, dimensions: list) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            content: 内容
            dimensions: 自定义维度列表
            
        Returns:
            缓存数据，不存在返回None
        """
        cache_key = self._get_cache_key(content, dimensions)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                return None
        return None
    
    def set(self, content: str, dimensions: list, data: Any) -> None:
        """
        设置缓存
        
        Args:
            content: 内容
            dimensions: 自定义维度列表
            data: 缓存数据
        """
        cache_key = self._get_cache_key(content, dimensions)
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception:
            pass
    
    def clear(self) -> None:
        """清空所有缓存"""
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()


# 全局缓存实例
cache_manager = CacheManager()

