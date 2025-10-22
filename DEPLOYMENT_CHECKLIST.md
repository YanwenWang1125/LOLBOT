# 🚀 LOLBOT 部署检查清单

## ✅ 环境变量配置

### 必需的环境变量
- [x] `RIOT_API_KEY` - Riot Games API 密钥
- [x] `VAL_API_KEY` - Valorant API 密钥 (Henrik API)
- [x] `OPENAI_API_KEY` - OpenAI API 密钥
- [x] `DISCORD_TOKEN` - Discord Bot 令牌
- [x] `VOICV_API_KEY` - VoicV TTS API 密钥
- [x] `VOICV_VOICE_ID` - VoicV 语音ID

### 可选的环境变量
- [x] `GAME_NAME` - 默认游戏用户名
- [x] `TAG_LINE` - 默认游戏标签
- [x] `REGION` - 游戏区域 (默认: na1)
- [x] `REGION_ROUTE` - API 路由区域 (默认: americas)

## ✅ 部署文件更新状态

### Docker 配置
- [x] `Dockerfile` - 已更新，包含所有依赖
- [x] `docker-compose.yml` - 已添加 VAL_API_KEY 环境变量
- [x] `requirements.txt` - 包含所有必要的 Python 包

### Azure 部署
- [x] `deploy-azure.sh` - 已更新环境变量检查
- [x] `QUICK_DEPLOY.md` - 已更新部署文档
- [x] `.github/workflows/deploy.yml` - 已更新 GitHub Actions 工作流
- [x] 环境变量检查包含 VAL_API_KEY

### 健康检查
- [x] `health_check.py` - 已添加 VAL_API_KEY 检查
- [x] 支持 JSON 输出模式用于监控

## ✅ 功能验证

### 核心功能
- [x] Discord Bot 连接
- [x] Riot API 连接 (LOL)
- [x] Valorant API 连接 (Henrik API)
- [x] OpenAI API 连接
- [x] VoicV TTS 连接
- [x] 游戏监控系统
- [x] 状态更新功能

### 新增功能
- [x] 自动游戏监控
- [x] 实时状态跟踪
- [x] 数据维护系统
- [x] 用户状态查询

## 🚀 部署步骤

### 1. 环境准备

#### 本地部署
```bash
# 设置环境变量
export RIOT_API_KEY="your_riot_api_key"
export VAL_API_KEY="your_val_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export DISCORD_TOKEN="your_discord_token"
export VOICV_API_KEY="your_voicv_api_key"
export VOICV_VOICE_ID="your_voicv_voice_id"
```

#### GitHub Actions 部署
在 GitHub 仓库设置中添加以下 Secrets：
- `RIOT_API_KEY` - Riot Games API 密钥
- `VAL_API_KEY` - Valorant API 密钥
- `OPENAI_API_KEY` - OpenAI API 密钥
- `DISCORD_TOKEN` - Discord Bot 令牌
- `VOICV_API_KEY` - VoicV TTS API 密钥
- `VOICV_VOICE_ID` - VoicV 语音ID
- `AZURE_CREDENTIALS` - Azure 服务主体凭据

### 2. 健康检查
```bash
# 运行健康检查
python health_check.py

# JSON 格式输出 (用于监控)
python health_check.py --json
```

### 3. 部署选项

#### 选项 A: Azure Container Apps (推荐)
```bash
chmod +x deploy-azure.sh
./deploy-azure.sh container-apps
```

#### 选项 B: Azure App Service
```bash
./deploy-azure.sh app-service
```

#### 选项 C: Docker Compose
```bash
docker-compose up -d
```

#### 选项 D: GitHub Actions (自动部署)
```bash
# 推送代码到 main 分支即可自动触发部署
git push origin main
```

## 🔍 部署后验证

### 1. 检查服务状态
```bash
# Container Apps
az containerapp show --name lolbot-app --resource-group lolbot-rg

# App Service
az webapp show --name lolbot-app --resource-group lolbot-rg
```

### 2. 查看日志
```bash
# Container Apps
az containerapp logs show --name lolbot-app --resource-group lolbot-rg

# App Service
az webapp log tail --name lolbot-app --resource-group lolbot-rg
```

### 3. 测试功能
- [ ] Discord Bot 在线状态
- [ ] 游戏监控功能
- [ ] 语音合成功能
- [ ] 数据分析功能

## 📊 监控和维护

### 定期检查
- [ ] 服务运行状态
- [ ] API 配额使用情况
- [ ] 错误日志分析
- [ ] 性能指标监控

### 故障排除
- [ ] 环境变量配置
- [ ] API 密钥有效性
- [ ] 网络连接状态
- [ ] 依赖包版本

## 🎯 部署完成确认

- [ ] 所有环境变量已设置
- [ ] 健康检查全部通过
- [ ] Discord Bot 成功连接
- [ ] 游戏监控功能正常
- [ ] 语音合成功能正常
- [ ] 数据分析功能正常

## 📞 支持信息

如果遇到问题，请检查：
1. 环境变量是否正确设置
2. API 密钥是否有效
3. 网络连接是否正常
4. 查看部署日志获取详细错误信息

---

**部署状态**: ✅ 准备就绪  
**最后更新**: 2025-10-21  
**版本**: v2.0 (包含游戏监控功能)
