#!/usr/bin/env python3
"""
优化后的AI提示词和系统角色配置模块
使用外部文件管理prompt模板，提高可维护性和可读性
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class PromptManager:
    """Prompt管理器 - 负责加载和管理所有prompt配置"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        初始化Prompt管理器
        
        Args:
            prompts_dir (str): prompt文件目录路径
        """
        self.prompts_dir = Path(prompts_dir)
        self.config_file = self.prompts_dir / "config.json"
        self._config = None
        self._cache = {}  # 缓存已加载的prompt文件
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self._config is None:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
            except json.JSONDecodeError as e:
                raise ValueError(f"配置文件格式错误: {e}")
        return self._config
    
    def _load_prompt_file(self, filename: str) -> str:
        """加载prompt文件内容"""
        if filename in self._cache:
            return self._cache[filename]
            
        prompt_file = self.prompts_dir / filename
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self._cache[filename] = content
                return content
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt文件不存在: {prompt_file}")
    
    def get_style_config(self, style_name: str = "default") -> Dict[str, str]:
        """
        获取指定风格的配置
        
        Args:
            style_name (str): 风格名称
            
        Returns:
            Dict[str, str]: 包含prompt, system_role和voice_id的配置字典
        """
        # DEBUG: 打印正在使用的prompt - 放在最前面确保每次都会执行
        print("=" * 80)
        print(f"DEBUG - 正在使用风格: {style_name}")
        print("=" * 80)
        
        config = self._load_config()
        styles = config.get("styles", {})
        
        if style_name not in styles:
            print(f"警告: 风格 '{style_name}' 不存在，使用默认风格")
            style_name = "default"
            
        style_config = styles.get(style_name, {})
        
        # 加载prompt文件内容
        prompt_file = style_config.get("prompt_file")
        if prompt_file:
            prompt_content = self._load_prompt_file(prompt_file)
        else:
            prompt_content = ""
        
        # 继续DEBUG信息
        print(f"Prompt文件: {prompt_file}")
        print(f"System Role: {style_config.get('system_role', 'N/A')}")
        print(f"Voice ID: {style_config.get('voice_id', 'N/A')}")
        print(f"Prompt内容长度: {len(prompt_content)} 字符")
        print("-" * 80)
        print("完整Prompt内容:")
        print("-" * 80)
        print(prompt_content)
        print("-" * 80)
        print("=" * 80)
            
        return {
            "prompt": prompt_content,
            "system_role": style_config.get("system_role", ""),
            "voice_id": style_config.get("voice_id", "")
        }
    
    def get_available_styles(self) -> list:
        """
        获取所有可用的风格列表
        
        Returns:
            list: 风格名称列表
        """
        config = self._load_config()
        return list(config.get("styles", {}).keys())
    
    def format_prompt(self, prompt_template: str, match_data: Dict[str, Any]) -> str:
        """
        格式化提示词模板
        
        Args:
            prompt_template (str): 提示词模板
            match_data (dict): 比赛数据
            
        Returns:
            str: 格式化后的提示词
        """
        # 提取用户名（去掉#号后的部分）
        mvp_username = match_data['team_mvp']['name'].split('#')[0]
        lvp_username = match_data['team_lvp']['name'].split('#')[0]
        
        # 提取其他需要的字段
        player_result = match_data['player_info']['result']
        mvp_champion = match_data['team_mvp']['champion_chinese']
        lvp_champion = match_data['team_lvp']['champion_chinese']
        
        return prompt_template.format(
            match_data=match_data,
            mvp_username=mvp_username,
            lvp_username=lvp_username,
            player_result=player_result,
            mvp_champion=mvp_champion,
            lvp_champion=lvp_champion
        )
    
    def reload_config(self):
        """重新加载配置（用于热更新）"""
        self._config = None
        self._cache.clear()
    
    def add_style(self, style_name: str, prompt_file: str, system_role: str, voice_id: str):
        """
        动态添加新的风格配置
        
        Args:
            style_name (str): 风格名称
            prompt_file (str): prompt文件名
            system_role (str): 系统角色
            voice_id (str): 语音ID
        """
        config = self._load_config()
        if "styles" not in config:
            config["styles"] = {}
            
        config["styles"][style_name] = {
            "prompt_file": prompt_file,
            "system_role": system_role,
            "voice_id": voice_id
        }
        
        # 保存配置
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        # 清除缓存
        self._cache.clear()


# 全局prompt管理器实例
prompt_manager = PromptManager()

# 向后兼容的函数接口
def get_style_config(style_name: str = "default") -> Dict[str, str]:
    """获取指定风格的配置（向后兼容接口）"""
    return prompt_manager.get_style_config(style_name)

def get_available_styles() -> list:
    """获取所有可用的风格列表（向后兼容接口）"""
    return prompt_manager.get_available_styles()

def format_prompt(prompt_template: str, match_data: Dict[str, Any]) -> str:
    """格式化提示词模板（向后兼容接口）"""
    return prompt_manager.format_prompt(prompt_template, match_data)

# 向后兼容的常量（已废弃，建议使用PromptManager）
DEFAULT_PROMPT = "请使用 get_style_config('default') 获取"
DEFAULT_SYSTEM_ROLE = "请使用 get_style_config('default') 获取"
