# 🚀 LOLBOT Azure快速部署指南

## 选择部署方案

### 🎯 推荐方案对比

| 方案 | 复杂度 | 成本 | 适用场景 | 推荐度 |
|------|--------|------|----------|--------|
| **Container Apps** | ⭐⭐ | 💰💰 | 生产环境 | ⭐⭐⭐⭐⭐ |
| **App Service** | ⭐ | 💰💰💰 | 快速部署 | ⭐⭐⭐⭐ |
| **Virtual Machine** | ⭐⭐⭐ | 💰💰💰💰 | 完全控制 | ⭐⭐⭐ |

## 🚀 一键部署 (Container Apps - 推荐)

### 前置条件
```bash
# 1. 安装Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. 登录Azure
az login

# 3. 设置环境变量
export RIOT_API_KEY="your_riot_api_key"
export VAL_API_KEY="your_val_api_key"
export GAME_NAME="YourGameName"
export TAG_LINE="YourTagLine"
export OPENAI_API_KEY="your_openai_api_key"
export DISCORD_TOKEN="your_discord_token"
export VOICV_API_KEY="your_voicv_api_key"
export VOICV_VOICE_ID="your_voicv_voice_id"
```

### 一键部署命令
```bash
# 给脚本执行权限
chmod +x deploy-azure.sh

# 部署到Container Apps (推荐)
./deploy-azure.sh container-apps

# 或者部署到App Service
./deploy-azure.sh app-service
```

## 📋 手动部署步骤

### 方案1: Container Apps (推荐)

```bash
# 1. 创建资源组
az group create --name lolbot-rg --location eastus

# 2. 创建Container Registry
az acr create --resource-group lolbot-rg --name lolbotregistry --sku Basic

# 3. 构建并推送镜像
az acr login --name lolbotregistry
docker build -t lolbotregistry.azurecr.io/lolbot:latest .
docker push lolbotregistry.azurecr.io/lolbot:latest

# 4. 创建Container App
az containerapp env create --name lolbot-env --resource-group lolbot-rg --location eastus
az containerapp create \
  --name lolbot-app \
  --resource-group lolbot-rg \
  --environment lolbot-env \
  --image lolbotregistry.azurecr.io/lolbot:latest \
  --registry-server lolbotregistry.azurecr.io \
  --cpu 1.0 --memory 2.0Gi \
  --env-vars RIOT_API_KEY=$RIOT_API_KEY VAL_API_KEY=$VAL_API_KEY GAME_NAME=$GAME_NAME TAG_LINE=$TAG_LINE OPENAI_API_KEY=$OPENAI_API_KEY DISCORD_TOKEN=$DISCORD_TOKEN VOICV_API_KEY=$VOICV_API_KEY VOICV_VOICE_ID=$VOICV_VOICE_ID
```

### 方案2: App Service

```bash
# 1. 创建App Service Plan
az appservice plan create --name lolbot-plan --resource-group lolbot-rg --sku B1 --is-linux

# 2. 创建Web App
az webapp create --resource-group lolbot-rg --plan lolbot-plan --name lolbot-app --runtime "PYTHON|3.11"

# 3. 配置环境变量
az webapp config appsettings set --resource-group lolbot-rg --name lolbot-app --settings RIOT_API_KEY=$RIOT_API_KEY VAL_API_KEY=$VAL_API_KEY GAME_NAME=$GAME_NAME TAG_LINE=$TAG_LINE OPENAI_API_KEY=$OPENAI_API_KEY DISCORD_TOKEN=$DISCORD_TOKEN VOICV_API_KEY=$VOICV_API_KEY VOICV_VOICE_ID=$VOICV_VOICE_ID

# 4. 部署代码
zip -r lolbot.zip . -x "*.git*" "*.pyc" "__pycache__/*"
az webapp deployment source config-zip --resource-group lolbot-rg --name lolbot-app --src lolbot.zip
```

## 🔍 健康检查

```bash
# 运行健康检查
python health_check.py

# JSON格式输出 (用于监控)
python health_check.py --json
```

## 📊 监控和维护

### 查看服务状态
```bash
# Container Apps
az containerapp show --name lolbot-app --resource-group lolbot-rg

# App Service
az webapp show --name lolbot-app --resource-group lolbot-rg
```

### 查看日志
```bash
# Container Apps
az containerapp logs show --name lolbot-app --resource-group lolbot-rg

# App Service
az webapp log tail --name lolbot-app --resource-group lolbot-rg
```

## 💰 成本估算

### Container Apps (推荐)
- **基础费用**: ~$0.0004/vCPU/秒
- **内存费用**: ~$0.000004/GB/秒
- **预计月费用**: $10-30

### App Service
- **B1计划**: ~$13.14/月
- **适合**: 小规模使用

### Virtual Machine
- **Standard_B2s**: ~$30/月
- **适合**: 完全控制需求

## 🛠️ 故障排除

### 常见问题
1. **环境变量未设置**: 检查Azure配置
2. **依赖安装失败**: 检查requirements.txt
3. **网络连接问题**: 检查防火墙设置
4. **Discord Bot离线**: 检查令牌和权限

### 调试命令
```bash
# 检查容器状态
docker ps -a

# 查看容器日志
docker logs <container-id>

# 进入容器调试
docker exec -it <container-id> /bin/bash
```

## 🔐 安全建议

1. **使用Azure Key Vault存储敏感信息**
2. **配置网络安全组**
3. **启用日志监控**
4. **定期更新依赖**
5. **使用HTTPS连接**

## 📞 支持

如果遇到问题，请检查：
1. 环境变量是否正确设置
2. API密钥是否有效
3. 网络连接是否正常
4. 查看Azure日志获取详细错误信息
