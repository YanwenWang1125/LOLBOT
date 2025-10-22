# 📊 Data Storage Directory

This directory contains all persistent data files used by the LOLBOT system, including user bindings, configuration data, and system state information.

## 📁 File Structure

```
data/
├── player_links.json    # User binding and status data
└── README.md           # This documentation
```

## 📋 Data Files

### **`player_links.json`** - User Binding Database
- **Purpose**: Stores Discord user to Riot ID bindings and real-time status
- **Format**: JSON
- **Content**: User registration data, presence status, game monitoring state
- **Updated by**: `services/presence_manager.py`
- **Accessed by**: All services requiring user data

## 🔧 Data Structure

### **Player Links JSON Structure**
```json
{
  "players": [
    {
      "discord_id": "416411638812639238",
      "riot_id": "exm233#233",
      "game": "LOL",
      "registered_at": "2025-10-21T15:54:52.242497",
      "last_match_id": "NA1_1234567890",
      "is_in_voice": true,
      "is_in_game": false,
      "active_match": null,
      "last_check": "2025-10-21T17:33:21.766817"
    }
  ]
}
```

### **Field Descriptions**
- **`discord_id`**: Discord user ID (string)
- **`riot_id`**: Riot Games ID (username#tag format)
- **`game`**: Game type (LOL, VALORANT)
- **`registered_at`**: Registration timestamp (ISO format)
- **`last_match_id`**: Last processed match ID
- **`is_in_voice`**: Current voice channel status (boolean)
- **`is_in_game`**: Current game status (boolean)
- **`active_match`**: Current active match ID (if any)
- **`last_check`**: Last status check timestamp (ISO format)

## 🔄 Data Management

### **Automatic Updates**
The data files are automatically updated by various services:

- **User Registration**: `!register_riot` command
- **Status Updates**: Real-time presence monitoring
- **Game Detection**: Automatic game state changes
- **Maintenance**: Regular data cleanup and validation

### **Data Persistence**
```python
# Data persistence is handled by PresenceManager
from services.presence_manager import PresenceManager

presence_manager = PresenceManager()

# Register new user
presence_manager.register_binding(
    discord_id="123456789",
    riot_id="username#tag",
    game="LOL"
)

# Update user status
presence_manager.update_user_status(
    riot_id="username#tag",
    is_in_voice=True,
    is_in_game=False,
    active_match=None
)
```

## 📊 Data Operations

### **User Registration**
```python
# Register new user binding
def register_user(discord_id, riot_id, game="LOL"):
    success = presence_manager.register_binding(
        discord_id=discord_id,
        riot_id=riot_id,
        game=game
    )
    return success
```

### **Status Updates**
```python
# Update user status
def update_status(riot_id, is_in_voice, is_in_game, active_match=None):
    success = presence_manager.update_user_status(
        riot_id=riot_id,
        is_in_voice=is_in_voice,
        is_in_game=is_in_game,
        active_match=active_match
    )
    return success
```

### **Data Retrieval**
```python
# Get user binding
def get_user_binding(discord_id):
    binding = presence_manager.get_binding_by_discord(discord_id)
    return binding

# Get all users
def get_all_users():
    users = presence_manager.get_all_active_bindings()
    return users
```

## 🔒 Data Security

### **Privacy Considerations**
- **User Data**: Contains Discord and Riot IDs
- **Status Information**: Real-time user presence data
- **Game Data**: Match IDs and game status
- **Access Control**: Restricted to authorized services

### **Data Protection**
- **File Permissions**: Secure file system permissions
- **Backup Strategy**: Regular data backup
- **Access Logging**: Monitor data access
- **Data Validation**: Input validation and sanitization

## 🧪 Data Validation

### **Schema Validation**
```python
def validate_player_data(data):
    """Validate player data structure"""
    required_fields = [
        "discord_id", "riot_id", "game", "registered_at",
        "last_match_id", "is_in_voice", "is_in_game", 
        "active_match", "last_check"
    ]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    
    return True, "Valid data structure"
```

### **Data Integrity Checks**
- **JSON Validity**: Verify JSON structure
- **Field Validation**: Check required fields
- **Type Validation**: Validate data types
- **Range Validation**: Check value ranges

## 🔄 Data Maintenance

### **Automatic Maintenance**
```python
# Data maintenance is handled by data_maintenance.py
from services.data_maintenance import DataMaintenance

maintenance = DataMaintenance()

# Start maintenance
await maintenance.start_maintenance()

# Check maintenance status
status = maintenance.get_maintenance_status()
```

### **Manual Maintenance**
```bash
# Check data status
!maintenance_status

# Start maintenance
!start_maintenance

# Stop maintenance
!stop_maintenance
```

## 📈 Performance Monitoring

### **Data Metrics**
- **User Count**: Number of registered users
- **Status Updates**: Frequency of status changes
- **Data Size**: File size and growth rate
- **Access Patterns**: Data access frequency

### **Performance Optimization**
- **File Caching**: Cache frequently accessed data
- **Batch Operations**: Efficient bulk operations
- **Async I/O**: Non-blocking file operations
- **Memory Management**: Efficient memory usage

## 🔧 Configuration

### **Data Settings**
```python
# Data configuration
PLAYER_LINKS_PATH = "data/player_links.json"
DATA_BACKUP_ENABLED = True
DATA_VALIDATION_ENABLED = True
AUTO_CLEANUP_ENABLED = True
```

### **Maintenance Settings**
```python
# Maintenance configuration
MAINTENANCE_INTERVAL = 300  # 5 minutes
CLEANUP_THRESHOLD = 100    # Max records
VALIDATION_ENABLED = True   # Enable validation
```

## 🎯 Use Cases

### **User Management**
- **Registration**: New user registration
- **Status Tracking**: Real-time user status
- **Game Monitoring**: Active game detection
- **Data Persistence**: Long-term data storage

### **System Integration**
- **Bot Commands**: User data for commands
- **Monitoring**: Game monitoring data
- **Analytics**: User behavior analysis
- **Reporting**: System status reports

## 📚 Integration Examples

### **Data Access**
```python
# Access user data
from services.presence_manager import PresenceManager

pm = PresenceManager()

# Get user by Discord ID
user = pm.get_binding_by_discord("123456789")

# Get user by Riot ID
user = pm.get_binding_by_riot("username#tag")

# Get all users
users = pm.get_all_active_bindings()
```

### **Status Management**
```python
# Update user status
pm.update_user_status(
    riot_id="username#tag",
    is_in_voice=True,
    is_in_game=False,
    active_match="NA1_1234567890"
)

# Check user presence
presence = pm.check_discord_presence("username#tag", bot)
```

## 🔄 Data Workflow

### **User Registration Workflow**
1. **User Command** → `!register_riot username#tag`
2. **Validation** → Check Riot ID format and availability
3. **Registration** → Create user binding
4. **Data Storage** → Save to player_links.json
5. **Confirmation** → Send success message

### **Status Update Workflow**
1. **Event Trigger** → Voice channel or game state change
2. **Status Check** → Verify current status
3. **Data Update** → Update user status in JSON
4. **Notification** → Log status change
5. **Integration** → Update monitoring systems

## 🐛 Troubleshooting

### **Common Issues**
- **File Corruption**: JSON file corruption
- **Permission Errors**: File system permissions
- **Data Validation**: Invalid data structure
- **Access Issues**: File access problems

### **Debug Commands**
```bash
# Check data location
!show_data_location

# Check user status
!user_status [RiotID]

# Check maintenance status
!maintenance_status
```

## 📊 Data Analytics

### **User Statistics**
- **Total Users**: Number of registered users
- **Active Users**: Users currently online
- **Game Activity**: Users currently in games
- **Voice Activity**: Users in voice channels

### **System Metrics**
- **Data Growth**: Rate of data accumulation
- **Access Frequency**: How often data is accessed
- **Update Frequency**: How often data is updated
- **Error Rate**: Data operation error rate

## 🔒 Backup and Recovery

### **Backup Strategy**
- **Regular Backups**: Automated data backup
- **Version Control**: Track data changes
- **Recovery Procedures**: Data recovery processes
- **Validation**: Backup integrity checks

### **Recovery Procedures**
```python
# Data recovery
def recover_data(backup_file):
    """Recover data from backup"""
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    # Validate backup data
    if validate_player_data(backup_data):
        # Restore data
        with open(PLAYER_LINKS_PATH, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        return True
    
    return False
```

---

*This directory contains the core persistent data for the LOLBOT system. All user bindings, status information, and system state are stored here for reliable operation and data persistence.*
