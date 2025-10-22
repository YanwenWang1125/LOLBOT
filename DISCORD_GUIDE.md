# 🤖 LOLBOT Discord 使用指南

## 📋 支持的游戏
- **League of Legends** (英雄联盟)
- **Valorant** (无畏契约)

## 🎮 基本指令

### 游戏分析指令
```bash
!lol username#tag [style]     # 分析英雄联盟对局
!va username#tag [style]      # 分析Valorant对局
!test                        # 测试工作流程（不播放音频）
```

### 用户管理指令
```bash
!register_riot username#tag   # 注册你的Riot ID
!unregister_riot             # 取消注册Riot ID
!check_presence [RiotID]     # 检查用户在线状态
!online_players              # 显示在线玩家
!voice_players               # 显示语音频道玩家
```

### 监控指令
```bash
!start_monitoring            # 开始自动游戏监控
!stop_monitoring             # 停止游戏监控
!monitoring_status           # 检查监控状态
```

### 系统指令
```bash
!files                       # 显示文件统计
!maintenance_status          # 检查系统健康状态
```

## 🎨 支持的风格 (Styles)

| 风格 | 描述 | 默认语音 |
|------|------|----------|
| `default` | 搞子风格，轻佻嚣张，压力队友 | 默认 |
| `kfk_dp` | 专业电竞解说 | 专业 |
| `kfk` | 专业电竞解说 | 专业 |
| `azi` | 虚拟主播阿梓 | 阿梓 |
| `dingzhen` | 专业解说员 | 丁真 |
| `taffy` | 友好解说 | Taffy |
| `lol_loveu` | 温柔大哥哥 | LoveU |
| `lol_keli` | 虚拟主播 | Keli |
| `va_kfk_dp` | Valorant专业解说 | 专业 |
| `va_kfk` | Valorant卡夫卡风格 | 专业 |
| `va_azi` | Valorant阿梓风格 | 阿梓 |

## 📝 使用示例

### 基本用法
```bash
!lol PlayerName#1234
!va PlayerName#1234
```

### 指定风格
```bash
!lol PlayerName#1234 azi
!va PlayerName#1234 kfk
```

### 注册用户
```bash
!register_riot PlayerName#1234
!check_presence PlayerName#1234
```

### 自动监控
```bash
!start_monitoring
!monitoring_status
```

## ⚠️ 注意事项

1. **频道限制**: 所有指令只能在 "红温时刻" 频道使用
2. **语音频道**: 分析音频会在你当前的语音频道播放
3. **自动监控**: 进入语音频道后会自动开始监控你的游戏状态
4. **文件管理**: 系统会自动清理旧的分析文件和音频文件

## 🚀 快速开始

1. **注册你的Riot ID**:
   ```
   !register_riot YourName#1234
   ```

2. **进入语音频道** (系统会自动开始监控)

3. **开始游戏** (系统会自动检测并分析)

4. **或者手动分析**:
   ```
   !lol YourName#1234
   ```

## 🎯 默认设置

- **默认风格**: `default` (搞子风格)
- **默认语音**: 系统自动选择
- **自动监控**: 进入语音频道后自动开启
- **文件保留**: 保留最近5个分析文件

---

*享受AI驱动的游戏分析体验！* 🎮✨
