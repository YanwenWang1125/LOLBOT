# Azure部署指南

## 方案1: Azure Container Apps (推荐)

### 前置条件
- Azure CLI已安装
- Docker已安装
- Azure订阅

### 部署步骤

#### 1. 创建资源组
```bash
az group create --name lolbot-rg --location eastus
```

#### 2. 创建Azure Container Registry
```bash
az acr create --resource-group lolbot-rg --name lolbotregistry --sku Basic
```

#### 3. 构建并推送镜像
```bash
# 登录到ACR
az acr login --name lolbotregistry

# 构建镜像
docker build -t lolbotregistry.azurecr.io/lolbot:latest .

# 推送镜像
docker push lolbotregistry.azurecr.io/lolbot:latest
```

#### 4. 创建Container App环境
```bash
# 创建Container App环境
az containerapp env create \
  --name lolbot-env \
  --resource-group lolbot-rg \
  --location eastus

# 创建Container App
az containerapp create \
  --name lolbot-app \
  --resource-group lolbot-rg \
  --environment lolbot-env \
  --image lolbotregistry.azurecr.io/lolbot:latest \
  --registry-server lolbotregistry.azurecr.io \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --env-vars \
    RIOT_API_KEY=your_riot_api_key \
    GAME_NAME=your_game_name \
    TAG_LINE=your_tag_line \
    OPENAI_API_KEY=your_openai_api_key \
    DISCORD_TOKEN=your_discord_token \
    VOICV_API_KEY=your_voicv_api_key \
    VOICV_VOICE_ID=your_voicv_voice_id
```

## 方案2: Azure App Service

### 部署步骤

#### 1. 创建App Service Plan
```bash
az appservice plan create \
  --name lolbot-plan \
  --resource-group lolbot-rg \
  --sku B1 \
  --is-linux
```

#### 2. 创建Web App
```bash
az webapp create \
  --resource-group lolbot-rg \
  --plan lolbot-plan \
  --name lolbot-app \
  --runtime "PYTHON|3.11"
```

#### 3. 配置环境变量
```bash
az webapp config appsettings set \
  --resource-group lolbot-rg \
  --name lolbot-app \
  --settings \
    RIOT_API_KEY=your_riot_api_key \
    GAME_NAME=your_game_name \
    TAG_LINE=your_tag_line \
    OPENAI_API_KEY=your_openai_api_key \
    DISCORD_TOKEN=your_discord_token \
    VOICV_API_KEY=your_voicv_api_key \
    VOICV_VOICE_ID=your_voicv_voice_id
```

#### 4. 部署代码
```bash
# 使用Azure CLI部署
az webapp deployment source config-zip \
  --resource-group lolbot-rg \
  --name lolbot-app \
  --src lolbot.zip
```

## 方案3: Azure Virtual Machine

### 部署步骤

#### 1. 创建VM
```bash
az vm create \
  --resource-group lolbot-rg \
  --name lolbot-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys
```

#### 2. 安装依赖
```bash
# SSH连接到VM
ssh azureuser@<vm-public-ip>

# 安装Python和依赖
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg git

# 克隆项目
git clone <your-repo-url>
cd LOLBOT

# 安装Python依赖
pip3 install -r requirements.txt
```

#### 3. 创建systemd服务
```bash
sudo nano /etc/systemd/system/lolbot.service
```

服务文件内容：
```ini
[Unit]
Description=LOL Bot Service
After=network.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser/LOLBOT
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10
Environment=RIOT_API_KEY=your_riot_api_key
Environment=GAME_NAME=your_game_name
Environment=TAG_LINE=your_tag_line
Environment=OPENAI_API_KEY=your_openai_api_key
Environment=DISCORD_TOKEN=your_discord_token
Environment=VOICV_API_KEY=your_voicv_api_key
Environment=VOICV_VOICE_ID=your_voicv_voice_id

[Install]
WantedBy=multi-user.target
```

#### 4. 启动服务
```bash
sudo systemctl daemon-reload
sudo systemctl enable lolbot
sudo systemctl start lolbot
sudo systemctl status lolbot
```

## 环境变量配置

### 必需的环境变量
- `RIOT_API_KEY`: Riot Games API密钥
- `GAME_NAME`: 游戏名称
- `TAG_LINE`: 游戏标签
- `OPENAI_API_KEY`: OpenAI API密钥
- `DISCORD_TOKEN`: Discord Bot令牌
- `VOICV_API_KEY`: VoicV API密钥
- `VOICV_VOICE_ID`: VoicV语音ID

### 可选环境变量
- `REGION`: 游戏区域 (默认: na1)
- `REGION_ROUTE`: 区域路由 (默认: americas)

## 监控和日志

### Container Apps
```bash
# 查看日志
az containerapp logs show --name lolbot-app --resource-group lolbot-rg

# 查看指标
az monitor metrics list --resource lolbot-app --resource-group lolbot-rg
```

### App Service
```bash
# 查看日志
az webapp log tail --name lolbot-app --resource-group lolbot-rg
```

### Virtual Machine
```bash
# 查看服务状态
sudo systemctl status lolbot

# 查看日志
sudo journalctl -u lolbot -f
```

## 成本估算

### Container Apps (推荐)
- 基础费用: ~$0.0004/vCPU/秒
- 内存费用: ~$0.000004/GB/秒
- 预计月费用: $10-30

### App Service
- B1计划: ~$13.14/月
- 适合小规模使用

### Virtual Machine
- Standard_B2s: ~$30/月
- 完全控制，适合复杂需求

## 安全建议

1. **使用Azure Key Vault存储敏感信息**
2. **配置网络安全组**
3. **启用日志监控**
4. **定期更新依赖**
5. **使用HTTPS连接**

## 故障排除

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
