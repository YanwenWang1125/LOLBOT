# 🤖 LOLBOT Discord Bot Module

This directory contains the core Discord bot implementation for LOLBOT, including command handlers, event listeners, and workflow management.

## 📁 File Structure

```
bots/
├── __init__.py              # Package initialization
├── discord_bot.py           # Main Discord bot implementation
└── commands_presence.py     # Presence and monitoring commands
```

## 🔧 Core Components

### **`discord_bot.py`** - Main Bot Implementation
- **Purpose**: Core Discord bot functionality and command handlers
- **Key Features**:
  - Discord bot initialization and configuration
  - Game analysis workflow management (LOL & Valorant)
  - Command processing and response handling
  - Audio playback integration
  - File management and cleanup

**Main Classes**:
- `LOLWorkflow` - Complete LOL game analysis workflow
- `VAWorkflow` - Complete Valorant game analysis workflow

**Key Commands**:
- `!lol username#tag [style]` - Analyze LOL game data
- `!va username#tag [style]` - Analyze Valorant game data
- `!test` - Test workflow without audio playback
- `!files` - Show file statistics

### **`commands_presence.py`** - Presence Management Commands
- **Purpose**: User presence tracking and game monitoring commands
- **Key Features**:
  - Riot ID registration and management
  - User presence status tracking
  - Automatic game monitoring
  - Voice channel event handling
  - Data maintenance commands

**Main Classes**:
- `PresenceCommands` - Discord command cog for presence management

**Key Commands**:
- `!register_riot username#tag` - Register Riot ID
- `!unregister_riot` - Unregister Riot ID
- `!check_presence [RiotID]` - Check user presence
- `!online_players` - Show online players
- `!voice_players` - Show players in voice channels
- `!start_monitoring` - Start game monitoring
- `!stop_monitoring` - Stop game monitoring
- `!monitoring_status` - Check monitoring status

## 🎮 Workflow System

### LOL Analysis Workflow
1. **Data Retrieval** - Get summoner info and match data
2. **Chinese Analysis** - Convert to Chinese analysis using AI
3. **TTS Generation** - Generate audio from analysis
4. **Discord Playback** - Play audio in voice channel
5. **Cleanup** - Remove old files

### Valorant Analysis Workflow
1. **Data Retrieval** - Get Valorant match data via Henrik API
2. **Chinese Analysis** - Convert to Chinese analysis using AI
3. **TTS Generation** - Generate audio from analysis
4. **Discord Playback** - Play audio in voice channel
5. **Cleanup** - Remove old files

## 🔄 Event System

### Voice Channel Events
- **User joins voice** → Start automatic game monitoring
- **User leaves voice** → Stop game monitoring
- **User switches voice** → Restart monitoring in new channel

### Presence Events
- **User comes online** → Log status change
- **User goes offline** → Log status change
- **Status updates** → Track user activity

## 🎯 Command Categories

### **Game Analysis Commands**
```bash
!lol username#tag [style]     # Analyze LOL game
!va username#tag [style]      # Analyze Valorant game
!test                        # Test workflow
```

### **User Management Commands**
```bash
!register_riot username#tag   # Register Riot ID
!unregister_riot             # Unregister Riot ID
!check_presence [RiotID]     # Check user presence
!user_status [RiotID]        # Detailed user status
```

### **Monitoring Commands**
```bash
!start_monitoring            # Start game monitoring
!stop_monitoring             # Stop game monitoring
!monitoring_status           # Check monitoring status
!online_players              # Show online players
!voice_players               # Show voice players
```

### **System Commands**
```bash
!files                       # Show file statistics
!show_data_location          # Show data storage info
!maintenance_status          # Check maintenance status
```

## 🔧 Configuration

### Bot Configuration
```python
# Discord bot settings
DISCORD_TOKEN = "your_discord_token"
ALLOWED_CHANNEL_NAME = "红温时刻"  # Restricted channel name

# Workflow settings
KEEP_FILES_COUNT = 5  # Number of files to keep
AUDIO_DIR = "audio"
ANALYSIS_DIR = "analysis"
```

### Command Permissions
- **Public Commands**: Most analysis and status commands
- **Admin Commands**: Maintenance and system management
- **Channel Restricted**: All commands limited to "红温时刻" channel

## 🎵 Audio Integration

### TTS Audio Generation
- **Voice Selection**: Based on style configuration
- **Audio Quality**: High-quality TTS output
- **File Management**: Automatic cleanup of old audio files

### Discord Voice Integration
- **Voice Channel Connection**: Automatic connection to user's voice channel
- **Audio Playback**: Seamless audio playback
- **Cleanup**: Automatic disconnection after playback

## 📊 Monitoring System

### Automatic Game Detection
- **Real-time Monitoring**: Continuous game state checking
- **Smart Intervals**: 30s during games, 90s when idle
- **Auto-cleanup**: Stops monitoring after extended inactivity

### Status Tracking
- **User Presence**: Discord online/offline status
- **Voice Activity**: Voice channel participation
- **Game Activity**: Active game detection
- **Data Persistence**: Status saved to JSON files

## 🐛 Error Handling

### Common Error Scenarios
- **API Failures**: Riot API connection issues
- **Audio Errors**: TTS generation failures
- **Discord Errors**: Voice channel connection issues
- **File Errors**: Permission or disk space issues

### Error Recovery
- **Retry Logic**: Automatic retry for transient failures
- **Graceful Degradation**: Continue operation despite errors
- **User Feedback**: Clear error messages to users
- **Logging**: Comprehensive error logging

## 🚀 Usage Examples

### Basic Bot Usage
```python
# Initialize bot
from bots.discord_bot import bot

# Start bot
bot.run(DISCORD_TOKEN)
```

### Command Integration
```python
# Add custom commands
@bot.command(name='custom')
async def custom_command(ctx):
    await ctx.send("Custom command response")
```

### Workflow Integration
```python
# Use workflows programmatically
from bots.discord_bot import LOLWorkflow

workflow = LOLWorkflow()
success = await workflow.run_full_workflow(
    voice_channel_id=channel_id,
    game_name="username",
    tag_line="tag",
    style="default"
)
```

## 🔒 Security Features

### Channel Restrictions
- **Channel Limitation**: Commands only work in "红温时刻" channel
- **Permission Checks**: Admin commands require proper permissions
- **User Validation**: Riot ID registration validation

### Data Protection
- **Secure Storage**: User data stored securely
- **API Key Management**: Environment variable protection
- **Input Validation**: Command input sanitization

## 📈 Performance Optimization

### Resource Management
- **File Cleanup**: Automatic old file removal
- **Memory Management**: Efficient data structures
- **API Rate Limiting**: Respectful API usage
- **Async Operations**: Non-blocking operations

### Monitoring
- **Status Tracking**: Real-time user status
- **Error Monitoring**: Comprehensive error tracking
- **Performance Metrics**: Response time monitoring
- **Resource Usage**: Memory and CPU monitoring

## 🧪 Testing

### Test Commands
```bash
!test                        # Test workflow
!test_game_detection [RiotID] # Test game detection
!force_check_game [RiotID]   # Force game status check
```

### Debug Information
- **Console Logging**: Detailed operation logs
- **Error Tracking**: Comprehensive error information
- **Status Reports**: Real-time status information
- **Performance Metrics**: System performance data

## 🔄 Maintenance

### Automated Maintenance
- **File Cleanup**: Automatic old file removal
- **Data Validation**: Regular data integrity checks
- **Status Updates**: Real-time status synchronization
- **Error Recovery**: Automatic error recovery

### Manual Maintenance
- **Status Commands**: Manual status checking
- **Data Commands**: Manual data management
- **System Commands**: System health monitoring
- **Admin Commands**: Administrative operations

## 📚 Dependencies

### Core Dependencies
```python
import discord
import asyncio
import json
import os
from datetime import datetime
```

### Service Dependencies
```python
from services.riot_checker import get_summoner_info
from services.match_analyzer import convert_to_chinese_mature_tone
from services.voicv_tts import generate_tts_audio
from services.presence_manager import PresenceManager
```

## 🤝 Contributing

### Adding New Commands
1. Create command function with proper decorators
2. Add error handling and validation
3. Include help documentation
4. Test thoroughly
5. Update this README

### Modifying Workflows
1. Understand existing workflow structure
2. Maintain backward compatibility
3. Add proper error handling
4. Test all scenarios
5. Update documentation

---

*This module is the core of the LOLBOT Discord bot. All major functionality is implemented here.*
