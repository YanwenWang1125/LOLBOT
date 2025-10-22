# 🎮 LOLBOT - Multi-Game AI Analysis Discord Bot

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-blue.svg)](https://discordpy.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Azure](https://img.shields.io/badge/Deploy-Azure-blue.svg)](QUICK_DEPLOY.md)

A comprehensive Discord bot that provides real-time game analysis for **League of Legends** and **Valorant**, featuring AI-powered Chinese commentary, voice synthesis, and automatic game monitoring.

## ✨ Key Features

### 🎯 Multi-Game Support
- **League of Legends**: Complete match analysis with KDA calculations
- **Valorant**: Ranked match analysis with performance metrics
- **Real-time Monitoring**: Automatic game detection and analysis

### 🤖 AI-Powered Analysis
- **Chinese Commentary**: Natural, mature-toned analysis in Chinese
- **Multiple Personalities**: Various commentator styles (professional, casual, humorous)
- **Smart Insights**: AI-generated performance analysis and recommendations

### 🎵 Voice Integration
- **Text-to-Speech**: High-quality Chinese voice synthesis
- **Voice Cloning**: Custom voice personalities for different styles
- **Discord Audio**: Seamless voice channel integration

### 🔄 Automated Workflows
- **Auto-Monitoring**: Detects when users are in games
- **Smart Triggers**: Automatic analysis when games end
- **Voice Channel Integration**: Plays analysis in user's voice channel

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Discord Bot Token
- Riot Games API Key
- OpenAI API Key
- VoicV API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YanwenWang1125/LOLBOT.git
   cd lolbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `RIOT_API_KEY` | Riot Games API key | ✅ | - |
| `OPENAI_API_KEY` | OpenAI API key | ✅ | - |
| `DISCORD_TOKEN` | Discord bot token | ✅ | - |
| `VOICV_API_KEY` | VoicV TTS API key | ✅ | - |
| `VOICV_VOICE_ID` | VoicV voice ID | ✅ | - |
| `GAME_NAME` | Default game username | ❌ | - |
| `TAG_LINE` | Default game tag | ❌ | - |
| `REGION` | Game region | ❌ | na1 |
| `REGION_ROUTE` | API region route | ❌ | americas |

### Example `.env` file
```env
# API Keys
RIOT_API_KEY=your_riot_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DISCORD_TOKEN=your_discord_bot_token_here
VOICV_API_KEY=your_voicv_api_key_here
VOICV_VOICE_ID=your_voicv_voice_id_here

# Game Configuration
GAME_NAME=YourGameName
TAG_LINE=YourTagLine
REGION=na1
REGION_ROUTE=americas
```

## 🎮 Discord Commands

### Game Analysis Commands
```bash
!lol username#tag [style]     # Analyze League of Legends match
!va username#tag [style]      # Analyze Valorant match
!test                        # Test workflow without audio
```

### User Management Commands
```bash
!register_riot username#tag   # Register your Riot ID
!unregister_riot             # Unregister your Riot ID
!check_presence [RiotID]     # Check user presence status
!online_players              # Show online players
!voice_players               # Show players in voice channels
```

### Monitoring Commands
```bash
!start_monitoring            # Start automatic game monitoring
!stop_monitoring             # Stop game monitoring
!monitoring_status           # Check monitoring status
```

### System Commands
```bash
!files                       # Show file statistics
!maintenance_status          # Check system health
```

## 🎨 Analysis Styles

The bot supports multiple commentator personalities:

| Style | Description | Voice |
|-------|-------------|-------|
| `default` | Casual, humorous | Default |
| `kfk_dp` | Professional esports analysis | Professional |
| `azi` | Virtual streamer personality | Azi |
| `dingzhen` | Professional commentator | Dingzhen |
| `taffy` | Casual, friendly analysis | Taffy |
| `lol_loveu` | Gentle, caring big brother | LoveU |
| `lol_keli` | Virtual streamer style | Keli |

## 🏗️ Project Structure

```
lolbot/
├── 📁 analysis/              # Generated match analysis files
├── 📁 audio/                 # Generated TTS audio files
├── 📁 audio_source/          # Voice cloning source files
├── 📁 bots/                  # Discord bot implementation
│   ├── discord_bot.py        # Main bot logic
│   └── commands_presence.py  # Presence management commands
├── 📁 data/                  # User data and configurations
├── 📁 prompts/               # AI prompt templates
│   ├── config.json           # Style configurations
│   └── *.txt                 # Prompt templates
├── 📁 services/              # Core service modules
│   ├── riot_checker.py       # League of Legends API
│   ├── valorant_checker.py   # Valorant API
│   ├── match_analyzer.py     # LOL analysis engine
│   ├── va_match_analyzer.py  # Valorant analysis engine
│   ├── voicv_tts.py          # Text-to-speech service
│   ├── presence_manager.py   # User presence tracking
│   └── game_monitor.py       # Automatic game monitoring
├── 📁 test/                  # Test files
├── main.py                   # Application entry point
├── health_check.py           # System health monitoring
└── requirements.txt           # Python dependencies
```

## 🔄 Workflow System

### Automatic Game Analysis
1. **User Detection**: Bot detects user in voice channel
2. **Game Monitoring**: Continuous monitoring of game status
3. **Game End Detection**: Automatic detection when game ends
4. **Data Retrieval**: Fetch match data from APIs
5. **AI Analysis**: Generate Chinese commentary
6. **Voice Synthesis**: Convert text to speech
7. **Audio Playback**: Play in Discord voice channel
8. **Cleanup**: Remove temporary files

### Manual Analysis
1. **Command Trigger**: User runs `!lol` or `!va` command
2. **Data Retrieval**: Fetch latest match data
3. **AI Analysis**: Generate analysis with selected style
4. **Voice Synthesis**: Create audio file
5. **Audio Playback**: Play in user's voice channel

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your keys

# Run the bot
python main.py
```

### Azure Deployment
For production deployment on Azure, see [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for detailed instructions.

```bash
# Quick Azure deployment
chmod +x deploy-azure.sh
./deploy-azure.sh container-apps
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t lolbot .
docker run -d --env-file .env lolbot
```

## 🔧 API Integration

### Riot Games API
- **Summoner Information**: Get player details and match history
- **Match Data**: Detailed match analysis and statistics
- **Champion Data**: Champion name translation and statistics

### Henrik API (Valorant)
- **Player Data**: Valorant player information and rank
- **Match History**: Recent matches and performance data
- **Region Support**: Multiple region support

### OpenAI Integration
- **GPT-4 Analysis**: Advanced game analysis and commentary
- **Style Customization**: Multiple personality styles
- **Chinese Language**: Natural Chinese commentary generation

### VoicV TTS
- **Voice Synthesis**: High-quality Chinese text-to-speech
- **Voice Cloning**: Custom voice personalities
- **Audio Optimization**: Optimized for Discord playback

## 🐛 Troubleshooting

### Common Issues

#### API Connection Problems
```bash
# Test API connections
python health_check.py
```

#### Discord Bot Issues
- Ensure bot has proper permissions
- Check if bot is in the correct voice channel
- Verify Discord token is valid

#### Audio Playback Issues
- Ensure FFmpeg is installed
- Check voice channel permissions
- Verify audio file generation

### Debug Commands
```bash
!test                        # Test complete workflow
!files                       # Check file system status
!maintenance_status          # Check system health
```

### Logs and Monitoring
```bash
# Check system health
python health_check.py --json

# View detailed logs
tail -f logs/bot.log
```

## 📊 Performance & Monitoring

### System Requirements
- **CPU**: 1 vCPU minimum
- **RAM**: 2GB minimum
- **Storage**: 10GB for audio files
- **Network**: Stable internet connection

### Monitoring
- **Health Checks**: Automatic system health monitoring
- **File Management**: Automatic cleanup of old files
- **API Rate Limiting**: Respectful API usage
- **Error Tracking**: Comprehensive error logging

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add type hints where possible
- Include docstrings for functions
- Write comprehensive tests

### Adding New Features
1. **New Games**: Add API integration in `services/`
2. **New Styles**: Add prompt templates in `prompts/`
3. **New Commands**: Add command handlers in `bots/`
4. **New Services**: Add service modules in `services/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Riot Games**: For the comprehensive League of Legends API
- **Henrik**: For the Valorant API service
- **OpenAI**: For the powerful GPT-4 analysis capabilities
- **VoicV**: For the high-quality Chinese TTS service
- **Discord.py**: For the excellent Discord bot framework

## 📞 Support

### Getting Help
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join community discussions
- **Documentation**: Check the detailed documentation in each module

### Resources
- [Riot Games API Documentation](https://developer.riotgames.com/)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [VoicV API Documentation](https://voicv.com/docs)

---

**Made with ❤️ for the gaming community**

*Transform your gaming experience with AI-powered analysis and commentary!*