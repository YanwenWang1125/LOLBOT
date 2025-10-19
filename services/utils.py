#!/usr/bin/env python3
"""
公共工具函数
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any


def find_latest_json_file(analysis_dir: str = "analysis") -> Optional[str]:
    """
    找到最新的match_analysis_*.json文件
    
    Args:
        analysis_dir: 分析文件目录
        
    Returns:
        最新文件的完整路径，如果没找到返回None
    """
    if not os.path.exists(analysis_dir):
        return None
    
    json_files = [f for f in os.listdir(analysis_dir) 
                  if f.startswith('match_analysis_') and f.endswith('.json')]
    
    if not json_files:
        return None
    
    # 获取最新的文件
    latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(analysis_dir, x)))
    return os.path.join(analysis_dir, latest_file)


def load_json_file(file_path: str) -> Optional[Dict[Any, Any]]:
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        解析后的JSON数据，失败返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 加载JSON文件失败: {e}")
        return None


def save_json_file(data: Dict[Any, Any], file_path: str) -> bool:
    """
    保存JSON文件
    
    Args:
        data: 要保存的数据
        file_path: 保存路径
        
    Returns:
        保存成功返回True，失败返回False
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] 保存JSON文件失败: {e}")
        return False


def generate_timestamp() -> str:
    """
    生成时间戳字符串
    
    Returns:
        格式化的时间戳字符串 (YYYYMMDD_HHMMSS)
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def ensure_directory(directory: str) -> bool:
    """
    确保目录存在
    
    Args:
        directory: 目录路径
        
    Returns:
        成功返回True，失败返回False
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"[ERROR] 创建目录失败: {e}")
        return False


def get_audio_filename(timestamp: str = None) -> str:
    """
    生成音频文件名
    
    Args:
        timestamp: 时间戳，如果为None则自动生成
        
    Returns:
        音频文件路径
    """
    if not timestamp:
        timestamp = generate_timestamp()
    
    ensure_directory("audio")
    return f"audio/match_analysis_{timestamp}.mp3"


def get_analysis_filename(timestamp: str = None) -> str:
    """
    生成分析文件名
    
    Args:
        timestamp: 时间戳，如果为None则自动生成
        
    Returns:
        分析文件路径
    """
    if not timestamp:
        timestamp = generate_timestamp()
    
    ensure_directory("analysis")
    return f"analysis/match_analysis_{timestamp}.json"
