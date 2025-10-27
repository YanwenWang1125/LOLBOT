# 🎮 LOLBOT Services Documentation

This directory contains all the core services that power the LOLBOT Discord bot. Each service handles a specific aspect of the bot's functionality.

## 📁 Service Overview

### 🔧 Core Services

#### **`config.py`** - Configuration Management
- **Purpose**: Centralized configuration management for all API keys and settings
- **Key Features**:
  - Environment variable loading
  - API key validation
  - Default value management
  - Configuration validation

#### **`utils.py`** - Utility Functions
- **Purpose**: Common utility functions used across the bot
- **Key Features**:
  - File system operations
  - Directory management
  - JSON file handling
  - Data validation

#### **`models.py`** - Data Models
- **Purpose**: Data structures and models for the bot
- **Key Features**:
  - User data models
  - Game data structures
  - API response models

### 🎮 Game Services

#### **`riot_checker.py`** - League of Legends API Integration
- **Purpose**: Handles all LOL-related API calls and data processing
- **Key Features**:
  - Summoner information retrieval
  - Match history fetching
  - Match details analysis
  - Champion name translation (English ↔ Chinese)
  - KDA calculation and analysis

**API Endpoints Used**:
- `https://americas.api.riotgames.com/riot/account/v1` - Account information
- `https://na1.api.riotgames.com/lol/summoner/v4` - Summoner data
- `https://americas.api.riotgames.com/lol/match/v5` - Match data

#### **`valorant_checker.py`** - Valorant API Integration
- **Purpose**: Handles Valorant game data retrieval using Henrik API
- **Key Features**:
  - Player account information
  - Match history retrieval
  - Rank information
  - Region mapping

**API Endpoints Used**:
- `https://api.henrikdev.xyz/valorant/v3` - Henrik API for Valorant data

### 🤖 AI & Analysis Services

#### **`match_analyzer.py`** - LOL Match Analysis
- **Purpose**: Analyzes LOL match data and generates Chinese analysis reports
- **Key Features**:
  - Match data processing
  - Performance analysis
  - Chinese report generation
  - AI-powered insights

#### **`va_match_analyzer.py`** - Valorant Match Analysis
- **Purpose**: Analyzes Valorant match data and generates Chinese analysis reports
- **Key Features**:
  - Valorant-specific analysis
  - Performance metrics
  - Chinese report generation
  - Game-specific insights

#### **`prompts.py`** - AI Prompt Management
- **Purpose**: Manages AI prompts and style configurations
- **Key Features**:
  - Style-based prompt selection
  - Dynamic prompt loading
  - Configuration management
  - Multi-language support

### 🎵 Audio Services

#### **`voicv_tts.py`** - Text-to-Speech Generation
- **Purpose**: Converts Chinese text to speech using VoicV API
- **Key Features**:
  - TTS audio generation
  - Voice cloning support
  - Audio file management
  - Quality optimization

#### **`voicV_clone.py`** - Voice Cloning
- **Purpose**: Handles voice cloning operations
- **Key Features**:
  - Voice model training
  - Voice ID management
  - Clone quality optimization

### 👥 User Management Services

#### **`presence_manager.py`** - User Presence Management
- **Purpose**: Manages user presence and status tracking
- **Key Features**:
  - Discord user binding
  - Riot ID registration
  - Status tracking
  - Data persistence


### 🔧 Maintenance Services

#### **`data_maintenance.py`** - Data Maintenance
- **Purpose**: Handles data cleanup and maintenance tasks
- **Key Features**:
  - Old file cleanup
  - Data integrity checks
  - Status validation
  - Automated maintenance

#### **`kda_calculator.py`** - KDA Calculation
- **Purpose**: Calculates and analyzes KDA statistics
- **Key Features**:
  - KDA computation
  - Performance scoring
  - Statistical analysis
  - Weighted calculations

## 🚀 Usage Examples

### Basic Service Usage

```python
# Import services
from services.riot_checker import get_summoner_info, get_recent_matches
from services.match_analyzer import convert_to_chinese_mature_tone
from services.voicv_tts import generate_tts_audio
from services.presence_manager import PresenceManager

# Get user data
summoner_info = get_summoner_info("username", "tag")
recent_matches = get_recent_matches(summoner_info['puuid'], 1)

# Analyze match
analysis = convert_to_chinese_mature_tone(match_data)

# Generate audio
audio_file = generate_tts_audio(analysis, voice_id="default")

# Manage user presence
presence_manager = PresenceManager()
presence_manager.register_binding("discord_id", "riot_id", "LOL")
```

### Service Integration

```python
# Complete workflow example
from services.presence_manager import PresenceManager

# Initialize managers
presence_manager = PresenceManager()

```

## 🔧 Configuration

### Environment Variables

All services require the following environment variables:

```env
# API Keys
RIOT_API_KEY=your_riot_api_key
OPENAI_API_KEY=your_openai_api_key
VOICV_API_KEY=your_voicv_api_key
DISCORD_TOKEN=your_discord_token

# Game Configuration
GAME_NAME=default_username
TAG_LINE=default_tag
REGION=na1
REGION_ROUTE=americas

# Optional Configuration
DISCORD_POLL_INTERVAL=300
RIOT_POLL_INTERVAL=180
PLAYER_LINKS_PATH=data/player_links.json
```

### Service Dependencies

```python
# Core dependencies
import discord
import requests
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# AI dependencies
import openai

# Audio dependencies
import voicv
```

## 🐛 Troubleshooting

### Common Issues

#### **API Connection Errors**
- Check API keys are correctly set
- Verify network connectivity
- Ensure API rate limits are not exceeded

#### **File Permission Errors**
- Check write permissions for data directories
- Ensure proper file ownership
- Verify disk space availability

#### **Service Integration Issues**
- Verify all dependencies are installed
- Check service initialization order
- Ensure proper error handling

### Debug Commands

```bash
# Test Riot API
python services/riot_checker.py

# Test Valorant API
python services/valorant_checker.py

# Test TTS generation
python services/voicv_tts.py

# Test voice cloning
python services/voicV_clone.py
```

## 📊 Service Architecture

```
services/
├── config.py              # Configuration management
├── utils.py               # Utility functions
├── models.py              # Data models
├── riot_checker.py        # LOL API integration
├── valorant_checker.py   # Valorant API integration
├── match_analyzer.py      # LOL match analysis
├── va_match_analyzer.py   # Valorant match analysis
├── prompts.py             # AI prompt management
├── voicv_tts.py           # Text-to-speech
├── voicV_clone.py         # Voice cloning
├── presence_manager.py    # User management
├── data_maintenance.py    # Data maintenance
└── kda_calculator.py      # KDA calculations
```

## 🔄 Service Workflow

### Automatic Game Analysis Workflow

1. **User enters voice channel** → `presence_manager.py`
2. **Detect active game** → `riot_checker.py` / `valorant_checker.py`
3. **Game ends** → `match_analyzer.py` / `va_match_analyzer.py`
4. **Generate analysis** → `prompts.py` + AI
5. **Create audio** → `voicv_tts.py`
6. **Play in Discord** → Discord bot integration
7. **Cleanup** → `data_maintenance.py`

### Manual Analysis Workflow

1. **User command** → Discord bot
2. **Get game data** → `riot_checker.py` / `valorant_checker.py`
3. **Analyze match** → `match_analyzer.py` / `va_match_analyzer.py`
4. **Generate audio** → `voicv_tts.py`
5. **Play audio** → Discord bot

## 📈 Performance Considerations

### Optimization Tips

- **API Rate Limiting**: Implement proper rate limiting for Riot API calls
- **Caching**: Cache frequently accessed data
- **Async Operations**: Use async/await for I/O operations
- **Error Handling**: Implement comprehensive error handling
- **Resource Management**: Clean up resources after use


- **API Usage**: Monitor API call frequency and limits
- **Error Rates**: Track service error rates
- **Performance**: Monitor service response times
- **Resource Usage**: Track memory and CPU usage

## 🔒 Security Considerations

### API Key Management

- Store API keys in environment variables
- Never commit API keys to version control
- Use different keys for development and production
- Regularly rotate API keys

### Data Protection

- Encrypt sensitive user data
- Implement proper access controls
- Regular security audits
- Secure data transmission

## 📚 Additional Resources

- [Riot Games API Documentation](https://developer.riotgames.com/)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [VoicV API Documentation](https://voicv.com/docs)

## 🤝 Contributing

When adding new services:

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include proper documentation
4. Add unit tests where possible
5. Update this README with new service information

## 📝 Changelog

### Version 1.0.0
- Initial service architecture
- AI analysis integration
- TTS audio generation
- User presence management

---

*This documentation is maintained alongside the codebase. Please update it when adding or modifying services.*
