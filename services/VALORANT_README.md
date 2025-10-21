# Valorant API Checker

这个模块用于检查Riot API密钥是否可以获取Valorant游戏数据。

## 文件说明

- `valorant_checker.py` - 主要的Valorant API检查脚本
- `valorant_api_test.py` - 快速测试脚本

## 功能特性

1. **API密钥验证** - 检查API密钥是否有效
2. **账户信息获取** - 获取Valorant玩家账户信息
3. **比赛数据访问** - 尝试获取最近的Valorant比赛数据
4. **权限检查** - 检测API密钥是否有Valorant数据访问权限
5. **错误处理** - 详细的错误信息和解决建议

## 使用方法

### 基本使用
```bash
python services/valorant_checker.py
```

### 快速测试
```bash
python services/valorant_api_test.py
```

## 环境变量要求

确保在`.env`文件中设置以下变量：
- `RIOT_API_KEY` - Riot Games API密钥
- `GAME_NAME` - 游戏用户名
- `TAG_LINE` - 用户标签

## 可能的输出结果

### 1. 完全成功
- API密钥有效
- 可以获取账户信息
- 可以获取比赛数据

### 2. 部分成功
- API密钥有效
- 可以获取账户信息
- 无法获取比赛数据（权限不足）

### 3. 失败
- API密钥无效或过期
- 网络连接问题
- 账户信息获取失败

## 常见问题

### 403 Forbidden 错误
这通常表示API密钥没有Valorant数据访问权限，可能原因：
1. 使用的是开发密钥，权限有限
2. 需要申请生产密钥
3. API密钥已过期

### 解决方案
1. 检查API密钥是否有效
2. 申请生产级别的API密钥
3. 确认密钥有Valorant数据访问权限

## API端点

脚本使用以下Riot Games API端点：
- 账户信息: `https://americas.api.riotgames.com/riot/account/v1`
- 比赛列表: `https://americas.api.riotgames.com/val/match/v1`
- 排位信息: `https://americas.api.riotgames.com/val/ranked/v1`
