#!/bin/bash

# 部署后健康检查脚本
# 用于验证LOLBOT在Azure Container Apps中的运行状态

set -e

# 配置
CONTAINER_APP_NAME=${1:-"lolbot"}
RESOURCE_GROUP=${2:-"rg-lolbot"}
MAX_RETRIES=5
RETRY_INTERVAL=30

echo "🔍 开始部署后健康检查..."
echo "容器应用: $CONTAINER_APP_NAME"
echo "资源组: $RESOURCE_GROUP"
echo "最大重试次数: $MAX_RETRIES"
echo "重试间隔: ${RETRY_INTERVAL}秒"
echo ""

# 检查容器应用状态
check_container_status() {
    local status=$(az containerapp show \
        -n $CONTAINER_APP_NAME \
        -g $RESOURCE_GROUP \
        --query "properties.runningStatus" \
        -o tsv 2>/dev/null)
    
    echo "📊 容器状态: $status"
    return $([ "$status" = "Running" ] && echo 0 || echo 1)
}

# 检查环境变量
check_environment_variables() {
    echo "🔍 检查环境变量..."
    
    local env_vars=$(az containerapp show \
        -n $CONTAINER_APP_NAME \
        -g $RESOURCE_GROUP \
        --query "properties.template.containers[0].env[].name" \
        -o tsv 2>/dev/null)
    
    local required_vars=("RIOT_API_KEY" "OPENAI_API_KEY" "DISCORD_TOKEN" "VOICV_API_KEY")
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if ! echo "$env_vars" | grep -q "$var"; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -eq 0 ]; then
        echo "✅ 所有必需环境变量已设置"
        return 0
    else
        echo "❌ 缺少环境变量: ${missing_vars[*]}"
        return 1
    fi
}

# 检查容器日志
check_container_logs() {
    echo "📋 检查容器日志..."
    
    local logs=$(az containerapp logs show \
        -n $CONTAINER_APP_NAME \
        -g $RESOURCE_GROUP \
        --tail 50 \
        -o tsv 2>/dev/null)
    
    if echo "$logs" | grep -q "✅ 所有配置检查通过"; then
        echo "✅ 配置检查通过"
        return 0
    else
        echo "❌ 配置检查失败"
        echo "最新日志:"
        echo "$logs" | tail -10
        return 1
    fi
}

# 检查Discord Bot连接
check_discord_connection() {
    echo "🤖 检查Discord Bot连接..."
    
    local logs=$(az containerapp logs show \
        -n $CONTAINER_APP_NAME \
        -g $RESOURCE_GROUP \
        --tail 100 \
        -o tsv 2>/dev/null)
    
    if echo "$logs" | grep -q "Bot已上线"; then
        echo "✅ Discord Bot连接成功"
        return 0
    else
        echo "⚠️ Discord Bot连接状态未知"
        return 1
    fi
}

# 主检查函数
main() {
    local retry_count=0
    local all_checks_passed=false
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        echo "🔄 第 $((retry_count + 1)) 次检查..."
        
        local checks_passed=0
        local total_checks=4
        
        # 检查容器状态
        if check_container_status; then
            echo "✅ 容器状态检查通过"
            ((checks_passed++))
        else
            echo "❌ 容器状态检查失败"
        fi
        
        # 检查环境变量
        if check_environment_variables; then
            echo "✅ 环境变量检查通过"
            ((checks_passed++))
        else
            echo "❌ 环境变量检查失败"
        fi
        
        # 检查容器日志
        if check_container_logs; then
            echo "✅ 日志检查通过"
            ((checks_passed++))
        else
            echo "❌ 日志检查失败"
        fi
        
        # 检查Discord连接
        if check_discord_connection; then
            echo "✅ Discord连接检查通过"
            ((checks_passed++))
        else
            echo "⚠️ Discord连接检查失败"
        fi
        
        echo "📊 检查结果: $checks_passed/$total_checks 通过"
        
        if [ $checks_passed -ge 3 ]; then
            all_checks_passed=true
            break
        fi
        
        if [ $retry_count -lt $((MAX_RETRIES - 1)) ]; then
            echo "⏳ 等待 ${RETRY_INTERVAL} 秒后重试..."
            sleep $RETRY_INTERVAL
        fi
        
        ((retry_count++))
    done
    
    echo ""
    echo "🎯 最终结果:"
    
    if [ "$all_checks_passed" = true ]; then
        echo "✅ 部署健康检查通过！"
        echo "🚀 LOLBOT 已成功部署并运行"
        exit 0
    else
        echo "❌ 部署健康检查失败！"
        echo "🔧 请检查以下问题："
        echo "   1. 容器应用是否正常运行"
        echo "   2. 环境变量是否正确设置"
        echo "   3. 应用日志是否有错误"
        echo "   4. Discord Bot是否成功连接"
        exit 1
    fi
}

# 运行主检查
main
