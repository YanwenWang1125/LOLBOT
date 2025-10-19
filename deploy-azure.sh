#!/bin/bash

# Azure部署脚本
# 使用方法: ./deploy-azure.sh [container-apps|app-service|vm]

set -e

RESOURCE_GROUP="lolbot-rg"
LOCATION="eastus"
APP_NAME="lolbot-app"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Azure CLI
check_azure_cli() {
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI未安装，请先安装Azure CLI"
        exit 1
    fi
    
    if ! az account show &> /dev/null; then
        print_error "请先登录Azure: az login"
        exit 1
    fi
}

# 检查环境变量
check_env_vars() {
    local required_vars=("RIOT_API_KEY" "GAME_NAME" "TAG_LINE" "OPENAI_API_KEY" "DISCORD_TOKEN" "VOICV_API_KEY" "VOICV_VOICE_ID")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        print_error "缺少环境变量: ${missing_vars[*]}"
        print_warning "请设置这些环境变量后再运行部署脚本"
        exit 1
    fi
}

# 部署到Container Apps
deploy_container_apps() {
    print_status "开始部署到Azure Container Apps..."
    
    # 创建资源组
    print_status "创建资源组: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $LOCATION
    
    # 创建Container Registry
    print_status "创建Azure Container Registry"
    az acr create --resource-group $RESOURCE_GROUP --name lolbotregistry --sku Basic
    
    # 登录到ACR
    print_status "登录到Container Registry"
    az acr login --name lolbotregistry
    
    # 构建并推送镜像
    print_status "构建Docker镜像"
    docker build -t lolbotregistry.azurecr.io/lolbot:latest .
    
    print_status "推送镜像到Registry"
    docker push lolbotregistry.azurecr.io/lolbot:latest
    
    # 创建Container App环境
    print_status "创建Container App环境"
    az containerapp env create \
        --name lolbot-env \
        --resource-group $RESOURCE_GROUP \
        --location $LOCATION
    
    # 创建Container App
    print_status "创建Container App"
    az containerapp create \
        --name $APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment lolbot-env \
        --image lolbotregistry.azurecr.io/lolbot:latest \
        --registry-server lolbotregistry.azurecr.io \
        --cpu 1.0 \
        --memory 2.0Gi \
        --min-replicas 1 \
        --max-replicas 3 \
        --env-vars \
            RIOT_API_KEY="$RIOT_API_KEY" \
            GAME_NAME="$GAME_NAME" \
            TAG_LINE="$TAG_LINE" \
            OPENAI_API_KEY="$OPENAI_API_KEY" \
            DISCORD_TOKEN="$DISCORD_TOKEN" \
            VOICV_API_KEY="$VOICV_API_KEY" \
            VOICV_VOICE_ID="$VOICV_VOICE_ID"
    
    print_status "Container App部署完成！"
    print_status "查看状态: az containerapp show --name $APP_NAME --resource-group $RESOURCE_GROUP"
}

# 部署到App Service
deploy_app_service() {
    print_status "开始部署到Azure App Service..."
    
    # 创建资源组
    print_status "创建资源组: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $LOCATION
    
    # 创建App Service Plan
    print_status "创建App Service Plan"
    az appservice plan create \
        --name lolbot-plan \
        --resource-group $RESOURCE_GROUP \
        --sku B1 \
        --is-linux
    
    # 创建Web App
    print_status "创建Web App"
    az webapp create \
        --resource-group $RESOURCE_GROUP \
        --plan lolbot-plan \
        --name $APP_NAME \
        --runtime "PYTHON|3.11"
    
    # 配置环境变量
    print_status "配置环境变量"
    az webapp config appsettings set \
        --resource-group $RESOURCE_GROUP \
        --name $APP_NAME \
        --settings \
            RIOT_API_KEY="$RIOT_API_KEY" \
            GAME_NAME="$GAME_NAME" \
            TAG_LINE="$TAG_LINE" \
            OPENAI_API_KEY="$OPENAI_API_KEY" \
            DISCORD_TOKEN="$DISCORD_TOKEN" \
            VOICV_API_KEY="$VOICV_API_KEY" \
            VOICV_VOICE_ID="$VOICV_VOICE_ID"
    
    # 创建部署包
    print_status "创建部署包"
    zip -r lolbot.zip . -x "*.git*" "*.pyc" "__pycache__/*" "analysis/*" "audio/*"
    
    # 部署代码
    print_status "部署代码到App Service"
    az webapp deployment source config-zip \
        --resource-group $RESOURCE_GROUP \
        --name $APP_NAME \
        --src lolbot.zip
    
    print_status "App Service部署完成！"
    print_status "查看状态: az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP"
}

# 部署到Virtual Machine
deploy_vm() {
    print_status "开始部署到Azure Virtual Machine..."
    
    # 创建资源组
    print_status "创建资源组: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $LOCATION
    
    # 创建VM
    print_status "创建Virtual Machine"
    az vm create \
        --resource-group $RESOURCE_GROUP \
        --name lolbot-vm \
        --image Ubuntu2204 \
        --size Standard_B2s \
        --admin-username azureuser \
        --generate-ssh-keys
    
    # 获取VM公网IP
    VM_IP=$(az vm show -d --resource-group $RESOURCE_GROUP --name lolbot-vm --query publicIps -o tsv)
    
    print_status "VM创建完成，IP地址: $VM_IP"
    print_warning "请手动SSH到VM完成以下步骤:"
    echo "1. ssh azureuser@$VM_IP"
    echo "2. 安装依赖: sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git"
    echo "3. 克隆项目: git clone <your-repo-url>"
    echo "4. 安装Python依赖: pip3 install -r requirements.txt"
    echo "5. 配置环境变量和systemd服务"
}

# 主函数
main() {
    local deployment_type=${1:-"container-apps"}
    
    print_status "LOLBOT Azure部署脚本"
    print_status "部署类型: $deployment_type"
    
    # 检查前置条件
    check_azure_cli
    check_env_vars
    
    case $deployment_type in
        "container-apps")
            deploy_container_apps
            ;;
        "app-service")
            deploy_app_service
            ;;
        "vm")
            deploy_vm
            ;;
        *)
            print_error "不支持的部署类型: $deployment_type"
            print_status "支持的部署类型: container-apps, app-service, vm"
            exit 1
            ;;
    esac
    
    print_status "部署完成！"
}

# 运行主函数
main "$@"
