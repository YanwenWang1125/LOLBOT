# 英雄联盟游戏数据分析工作流程

这是一个完整的英雄联盟游戏数据分析系统，能够自动获取游戏数据、生成AI分析、合成语音并在Discord中播放。

## 🎮 功能特性

- **自动数据获取**: 通过Riot Games API获取最新游戏数据
- **AI智能分析**: 使用OpenAI GPT生成成熟语调的中文分析
- **语音合成**: 使用VoicV TTS API将分析转换为语音
- **Discord集成**: 在Discord语音频道中播放分析音频
- **模块化设计**: 清晰的目录结构，易于维护和扩展

## 📁 项目结构

```
project-root/
├─ analysis/                  # 生成的 match_analysis_*.json（步骤1 输出）
├─ audio/                     # 生成的语音 mp3（步骤3 输出）
├─ bots/
│  └─ discord_bot.py          # 主入口（步骤4）
├─ services/
│  ├─ riot_checker.py         # 步骤1：获取并保存对局 JSON
│  ├─ json_to_chinese_lu.py   # 步骤2：调用 OpenAI → 中文分析
│  ├─ voicv_tts.py            # 步骤3：VoicV TTS 合成
│  └─ utils.py                # 公共工具函数
├─ .env                       # 环境变量配置
├─ requirements.txt
├─ main.py                    # 主入口文件
└─ README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并设置以下变量：

```env
# Riot Games API
RIOT_API_KEY=your_riot_api_key_here
GAME_NAME=YourGameName
TAG_LINE=YourTagLine
REGION=na1
REGION_ROUTE=americas

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Discord Bot
DISCORD_TOKEN=your_discord_bot_token_here

# VoicV TTS
VOICV_API_KEY=your_voicv_api_key_here
VOICV_VOICE_ID=your_voicv_voice_id_here
```

### 3. 运行程序

```bash
python main.py
```

## 🎯 工作流程

### 步骤1: 获取游戏数据 🔍
- 调用Riot Games API获取玩家最新游戏数据
- 分析游戏表现，识别MVP和LVP
- 保存为JSON文件到 `analysis/` 目录

### 步骤2: AI中文分析 🤖
- 使用OpenAI GPT-4生成成熟语调的中文分析
- 采用"御姐"风格，兼具理性和情感
- 包含语气标签和停顿标记

### 步骤3: 语音合成 🎵
- 使用VoicV TTS API将中文分析转换为语音
- 支持自定义声音克隆
- 保存为MP3文件到 `audio/` 目录

### 步骤4: Discord播放 🔊
- 连接Discord语音频道
- 使用FFmpeg播放生成的音频
- 播放完成后自动断开连接

## 🤖 Discord Bot 命令

- `!lol [语音频道ID]` - 运行完整分析流程
- `!test` - 测试工作流程（不播放音频）

## 🔧 技术栈

- **数据获取**: Riot Games API
- **AI分析**: OpenAI GPT-4
- **语音合成**: VoicV TTS API
- **语音播放**: Discord.py + FFmpeg
- **数据存储**: JSON文件 + 音频文件

## 📋 环境变量说明

| 变量名 | 描述 | 必需 | 默认值 |
|--------|------|------|--------|
| `RIOT_API_KEY` | Riot Games API密钥 | ✅ | - |
| `GAME_NAME` | 游戏名称（#号前部分） | ✅ | - |
| `TAG_LINE` | 标签（#号后部分） | ✅ | - |
| `REGION` | 平台区域 | ❌ | na1 |
| `REGION_ROUTE` | 区域路由 | ❌ | americas |
| `OPENAI_API_KEY` | OpenAI API密钥 | ✅ | - |
| `DISCORD_TOKEN` | Discord Bot令牌 | ✅ | - |
| `VOICV_API_KEY` | VoicV API密钥 | ✅ | - |
| `VOICV_VOICE_ID` | VoicV声音ID | ✅ | - |

## 🛠️ 开发说明

### 模块化设计
- `services/` - 核心服务模块
- `bots/` - Discord Bot相关功能
- `utils.py` - 公共工具函数

### 扩展功能
- 支持自定义分析风格
- 可配置语音参数
- 支持多种输出格式

## 📝 使用示例

1. **启动Discord Bot**:
   ```bash
   python main.py
   # 选择选项 1
   ```

2. **在Discord中使用**:
   ```
   !lol 123456789012345678  # 指定语音频道ID
   !lol                     # 使用当前语音频道
   !test                    # 测试模式
   ```

3. **测试工作流程**:
   ```bash
   python main.py
   # 选择选项 2
   ```

## 🐛 故障排除

### 常见问题

1. **API密钥错误**: 检查 `.env` 文件中的API密钥是否正确
2. **网络连接问题**: 确保网络连接正常，API服务可用
3. **Discord权限**: 确保Bot有语音频道权限
4. **FFmpeg路径**: 检查FFmpeg路径是否正确配置

### 调试模式

使用 `!test` 命令可以测试前3个步骤，不进行Discord播放。

## 📄 许可证

本项目仅供学习和个人使用。