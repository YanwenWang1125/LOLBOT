# 🔧 Deployment Scripts Directory

This directory contains deployment and maintenance scripts for the LOLBOT system. These scripts automate various deployment, monitoring, and maintenance tasks.

## 📁 File Structure

```
scripts/
├── deployment_check.sh    # Deployment verification script
└── README.md             # This documentation
```

## 🚀 Deployment Scripts

### **`deployment_check.sh`** - Deployment Verification
- **Purpose**: Verify deployment status and system health
- **Functionality**:
  - Check system status
  - Verify service availability
  - Test API connections
  - Validate configuration
  - Generate health report

## 🔧 Script Functionality

### **Deployment Verification**
```bash
#!/bin/bash
# deployment_check.sh - Verify deployment status

echo "🔍 Starting deployment verification..."

# Check system status
echo "📊 Checking system status..."
systemctl status lolbot

# Verify services
echo "🔧 Verifying services..."
python3 -c "import services.config; print('✅ Services OK')"

# Test API connections
echo "🌐 Testing API connections..."
python3 -c "from services.riot_checker import get_summoner_info; print('✅ Riot API OK')"

# Check file permissions
echo "📁 Checking file permissions..."
ls -la data/player_links.json

echo "✅ Deployment verification complete!"
```

## 🎯 Script Usage

### **Manual Execution**
```bash
# Run deployment check
./scripts/deployment_check.sh

# Make script executable
chmod +x scripts/deployment_check.sh
```

### **Automated Execution**
```bash
# Add to crontab for regular checks
0 */6 * * * /path/to/scripts/deployment_check.sh

# Run on system startup
@reboot /path/to/scripts/deployment_check.sh
```

## 🔍 Health Monitoring

### **System Health Checks**
- **Service Status**: Check if LOLBOT service is running
- **API Connectivity**: Test Riot API and other external APIs
- **File System**: Verify file permissions and disk space
- **Configuration**: Validate environment variables
- **Database**: Check data file integrity

### **Performance Monitoring**
- **Memory Usage**: Monitor system memory consumption
- **CPU Usage**: Check CPU utilization
- **Disk Space**: Monitor available disk space
- **Network**: Test network connectivity
- **Logs**: Check for errors in system logs

## 🛠️ Maintenance Tasks

### **Regular Maintenance**
```bash
# Clean up old files
find analysis/ -name "*.json" -mtime +7 -delete
find audio/ -name "*.mp3" -mtime +7 -delete

# Check disk space
df -h

# Verify file permissions
chmod 644 data/player_links.json
chmod 755 scripts/
```

### **Data Maintenance**
```bash
# Backup data files
cp data/player_links.json data/backup_$(date +%Y%m%d).json

# Validate JSON files
python3 -c "import json; json.load(open('data/player_links.json'))"

# Check file sizes
du -sh analysis/ audio/ data/
```

## 🔧 Configuration Management

### **Environment Validation**
```bash
# Check environment variables
echo "RIOT_API_KEY: ${RIOT_API_KEY:0:10}..."
echo "DISCORD_TOKEN: ${DISCORD_TOKEN:0:10}..."
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:0:10}..."

# Verify required files
test -f .env && echo "✅ .env file exists" || echo "❌ .env file missing"
test -f requirements.txt && echo "✅ requirements.txt exists" || echo "❌ requirements.txt missing"
```

### **Service Configuration**
```bash
# Check service configuration
systemctl show lolbot | grep -E "(Active|MainPID|Status)"

# Verify port availability
netstat -tlnp | grep :8000

# Check log files
tail -n 50 /var/log/lolbot.log
```

## 📊 Monitoring and Alerting

### **Health Metrics**
```bash
# System metrics
echo "=== System Health Report ==="
echo "Date: $(date)"
echo "Uptime: $(uptime)"
echo "Memory: $(free -h | grep Mem)"
echo "Disk: $(df -h | grep /)"
echo "CPU: $(top -bn1 | grep "Cpu(s)")"
```

### **Service Metrics**
```bash
# LOLBOT specific metrics
echo "=== LOLBOT Metrics ==="
echo "Analysis files: $(find analysis/ -name "*.json" | wc -l)"
echo "Audio files: $(find audio/ -name "*.mp3" | wc -l)"
echo "Data size: $(du -sh data/)"
echo "Log size: $(du -sh logs/)"
```

## 🚨 Error Handling

### **Error Detection**
```bash
# Check for common errors
grep -i "error\|exception\|failed" logs/lolbot.log | tail -10

# Check API errors
grep -i "riot\|api\|timeout" logs/lolbot.log | tail -10

# Check Discord errors
grep -i "discord\|token\|permission" logs/lolbot.log | tail -10
```

### **Recovery Procedures**
```bash
# Restart service on error
if ! systemctl is-active --quiet lolbot; then
    echo "❌ Service not running, restarting..."
    systemctl restart lolbot
fi

# Clear temporary files
rm -f /tmp/lolbot_*.tmp

# Reset file permissions
chown -R lolbot:lolbot /opt/lolbot/
```

## 🔄 Automation

### **Cron Jobs**
```bash
# Add to crontab
crontab -e

# Every 6 hours
0 */6 * * * /opt/lolbot/scripts/deployment_check.sh

# Daily cleanup
0 2 * * * /opt/lolbot/scripts/cleanup.sh

# Weekly backup
0 3 * * 0 /opt/lolbot/scripts/backup.sh
```

### **Systemd Timers**
```bash
# Create systemd timer
sudo systemctl edit --full lolbot-health.timer

[Unit]
Description=LOLBOT Health Check Timer

[Timer]
OnCalendar=*-*-* 00,06,12,18:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

## 📈 Performance Optimization

### **Resource Monitoring**
```bash
# Monitor resource usage
top -p $(pgrep -f lolbot)

# Check memory usage
ps aux | grep lolbot | awk '{print $4, $6}'

# Monitor disk I/O
iostat -x 1 5
```

### **Optimization Tasks**
```bash
# Optimize file system
sync && echo 3 > /proc/sys/vm/drop_caches

# Clean up logs
find logs/ -name "*.log" -mtime +30 -delete

# Optimize database
python3 -c "from services.data_maintenance import cleanup; cleanup()"
```

## 🔒 Security

### **Security Checks**
```bash
# Check file permissions
find /opt/lolbot -type f -perm /o+w

# Verify API keys
grep -E "API_KEY|TOKEN" .env | wc -l

# Check network security
netstat -tlnp | grep lolbot
```

### **Access Control**
```bash
# Set proper permissions
chmod 600 .env
chmod 644 data/player_links.json
chmod 755 scripts/

# Verify ownership
ls -la /opt/lolbot/
```

## 🧪 Testing

### **Integration Testing**
```bash
# Test API connections
python3 -c "
from services.riot_checker import get_summoner_info
from services.voicv_tts import generate_tts_audio
print('✅ All services working')
"

# Test Discord connection
python3 -c "
import discord
bot = discord.Client()
print('✅ Discord client OK')
"
```

### **Performance Testing**
```bash
# Load testing
ab -n 100 -c 10 http://localhost:8000/health

# Memory testing
python3 -c "
import psutil
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'CPU: {psutil.cpu_percent()}%')
"
```

## 📚 Documentation

### **Script Documentation**
Each script should include:
- **Purpose**: What the script does
- **Usage**: How to run the script
- **Parameters**: Command line parameters
- **Output**: Expected output format
- **Errors**: Common error conditions

### **Maintenance Logs**
```bash
# Log maintenance activities
echo "$(date): Deployment check completed" >> logs/maintenance.log
echo "$(date): Cleanup completed" >> logs/maintenance.log
echo "$(date): Backup completed" >> logs/maintenance.log
```

## 🔧 Customization

### **Adding New Scripts**
1. **Create Script**: Add new shell script
2. **Set Permissions**: Make executable
3. **Add Documentation**: Update README
4. **Test Script**: Verify functionality
5. **Add to Automation**: Include in cron/systemd

### **Script Templates**
```bash
#!/bin/bash
# Template for new scripts

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
SCRIPT_NAME="$(basename "$0")"
LOG_FILE="logs/${SCRIPT_NAME}.log"

# Functions
log() {
    echo "$(date): $1" | tee -a "$LOG_FILE"
}

error() {
    echo "ERROR: $1" >&2
    log "ERROR: $1"
    exit 1
}

# Main execution
main() {
    log "Starting $SCRIPT_NAME"
    
    # Script logic here
    
    log "Completed $SCRIPT_NAME"
}

# Run main function
main "$@"
```

## 🐛 Troubleshooting

### **Common Issues**
- **Permission Errors**: Check file permissions
- **Path Issues**: Verify script paths
- **Environment**: Check environment variables
- **Dependencies**: Verify required tools

### **Debug Mode**
```bash
# Enable debug mode
set -x  # Enable debug output
set -e  # Exit on error
set -u  # Exit on undefined variable

# Run with debug
bash -x scripts/deployment_check.sh
```

---

*This directory contains deployment and maintenance scripts that automate various system operations for the LOLBOT project. These scripts ensure reliable deployment, monitoring, and maintenance of the system.*
