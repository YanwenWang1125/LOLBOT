# Prompt管理系统

这是优化后的prompt管理系统，使用外部文件来管理所有的prompt模板和配置。

## 📁 目录结构

```
prompts/
├── config.json          # 主配置文件
├── README.md            # 说明文档
├── default.txt          # 默认风格prompt
├── kfk_dp.txt          # KFK_DP风格prompt
├── kfk.txt             # KFK风格prompt
├── azi.txt             # Azi风格prompt
├── dingzhen.txt        # 丁真风格prompt
├── taffy.txt           # Taffy风格prompt
├── va_kfk_dp.txt       # Valorant KFK_DP风格prompt
└── va_kfk.txt          # Valorant KFK风格prompt
```

## 🔧 配置文件说明

### config.json
```json
{
  "styles": {
    "style_name": {
      "prompt_file": "prompt文件名.txt",
      "system_role": "系统角色描述",
      "voice_id": "语音ID"
    }
  }
}
```

## 📝 使用方法

### 1. 基本使用
```python
from services.prompts import prompt_manager

# 获取风格配置
config = prompt_manager.get_style_config("default")
prompt = config["prompt"]
system_role = config["system_role"]
voice_id = config["voice_id"]
```

### 2. 获取所有可用风格
```python
styles = prompt_manager.get_available_styles()
print(styles)  # ['default', 'kfk_dp', 'kfk', ...]
```

### 3. 格式化prompt
```python
formatted_prompt = prompt_manager.format_prompt(prompt, match_data)
```

## ✨ 优势

1. **可维护性**: prompt内容与代码分离，易于编辑
2. **可读性**: 每个prompt都是独立的文本文件
3. **版本控制**: prompt修改不会污染代码历史
4. **热更新**: 支持运行时重新加载配置
5. **扩展性**: 添加新风格只需添加文件并更新配置

## 🚀 添加新风格

1. 创建新的prompt文件，如 `new_style.txt`
2. 在 `config.json` 中添加新配置：
```json
{
  "styles": {
    "new_style": {
      "prompt_file": "new_style.txt",
      "system_role": "新的系统角色描述",
      "voice_id": "新的语音ID"
    }
  }
}
```

## 🔄 热更新

```python
# 重新加载配置（用于热更新）
prompt_manager.reload_config()
```

## 📋 迁移指南

从旧的 `prompts.py` 迁移到新结构：

1. 运行迁移脚本：
```bash
python migrate_prompts.py
```

2. 更新代码中的导入：
```python
# 旧方式
from services.prompts import prompt_manager

# 新方式
from services.prompts import prompt_manager
config = prompt_manager.get_style_config("default")
```

## 🐛 故障排除

### 文件不存在错误
- 检查 `prompts/` 目录是否存在
- 检查 `config.json` 文件是否存在
- 检查对应的 `.txt` 文件是否存在

### 配置格式错误
- 检查 `config.json` 的JSON格式是否正确
- 确保所有必需的字段都存在

### 编码问题
- 确保所有文件都使用UTF-8编码
- 检查中文字符是否正确显示
