# 📝 AI Prompts Directory

This directory contains all AI prompt templates and configuration files used by the LOLBOT system for generating Chinese game analysis. Each prompt file defines a unique personality and analysis style.

## 📁 File Structure

```
prompts/
├── config.json          # Prompt configuration and voice mapping
├── default.txt          # Default analysis prompt
├── azi.txt              # Azi's analysis style
├── dingzhen.txt         # Dingzhen's analysis style
├── kfk.txt              # KFK's analysis style
├── kfk_dp.txt           # KFK DP's analysis style
├── taffy.txt            # Taffy's analysis style
├── va_azi.txt           # Azi's Valorant analysis style
├── va_kfk.txt           # KFK's Valorant analysis style
├── va_kfk_dp.txt        # KFK DP's Valorant analysis style
├── lol_loveu.txt        # Loveu's LOL analysis style
├── README.md            # This documentation
└── (existing README.md) # Previous documentation
```

## 🎯 Prompt System Overview

### **Style-Based Analysis**
Each prompt file defines a unique personality and analysis approach:

- **`default.txt`** - Standard professional analysis
- **`azi.txt`** - Azi's analytical and professional style
- **`dingzhen.txt`** - Dingzhen's energetic and enthusiastic style
- **`kfk.txt`** - KFK's calm and methodical approach
- **`kfk_dp.txt`** - KFK DP's detailed and technical style
- **`taffy.txt`** - Taffy's playful and engaging personality
- **`lol_loveu.txt`** - Loveu's warm and encouraging LOL style

### **Game-Specific Prompts**
- **LOL Prompts**: `azi.txt`, `kfk.txt`, `kfk_dp.txt`, `taffy.txt`, `lol_loveu.txt`
- **Valorant Prompts**: `va_azi.txt`, `va_kfk.txt`, `va_kfk_dp.txt`

## 🔧 Configuration System

### **`config.json`** - Central Configuration
```json
{
  "prompts": {
    "default": {
      "file": "default.txt",
      "voice_id": "default_voice",
      "description": "Default analysis style"
    },
    "azi": {
      "file": "azi.txt",
      "voice_id": "voice_id_azi",
      "description": "Azi's analytical style"
    },
    "dingzhen": {
      "file": "dingzhen.txt",
      "voice_id": "voice_id_dingzhen",
      "description": "Dingzhen's energetic style"
    }
  },
  "voice_mapping": {
    "azi": "voice_id_azi",
    "dingzhen": "voice_id_dingzhen",
    "kfk": "voice_id_kfk",
    "kfk_dp": "voice_id_kfk_dp",
    "taffy": "voice_id_taffy",
    "loveu": "voice_id_loveu"
  }
}
```

## 📝 Prompt Templates

### **Default Prompt Structure**
Each prompt file follows a consistent structure:

```
你是一个专业的游戏分析师，请分析以下游戏数据：

游戏信息：
- 游戏类型：{game_type}
- 比赛ID：{match_id}
- 游戏时长：{game_duration}
- 游戏模式：{game_mode}

玩家信息：
- 召唤师名称：{summoner_name}
- 英雄：{champion_name}
- 位置：{position}

表现数据：
- KDA：{kda}
- 击杀：{kills}
- 死亡：{deaths}
- 助攻：{assists}
- 补刀：{cs}
- 经济：{gold_earned}
- 伤害：{damage_dealt}

请用{personality_style}的风格分析这场比赛，包括：
1. 整体表现评价
2. 具体数据解读
3. 改进建议
4. 鼓励性总结

分析要求：
- 使用中文
- 语气{personality_tone}
- 长度适中（200-300字）
- 专业且易懂
```

## 🎨 Personality Styles

### **Azi Style** (`azi.txt`)
- **Personality**: Analytical, professional, data-driven
- **Tone**: Serious, methodical, insightful
- **Focus**: Technical analysis, performance metrics
- **Language**: Professional Chinese with technical terms

### **Dingzhen Style** (`dingzhen.txt`)
- **Personality**: Energetic, enthusiastic, motivating
- **Tone**: Excited, encouraging, upbeat
- **Focus**: Positive reinforcement, motivation
- **Language**: Energetic Chinese with encouraging phrases

### **KFK Style** (`kfk.txt`)
- **Personality**: Calm, methodical, balanced
- **Tone**: Peaceful, thoughtful, measured
- **Focus**: Balanced analysis, constructive feedback
- **Language**: Calm Chinese with balanced perspective

### **KFK DP Style** (`kfk_dp.txt`)
- **Personality**: Detailed, technical, comprehensive
- **Tone**: Thorough, analytical, precise
- **Focus**: Detailed technical analysis
- **Language**: Technical Chinese with detailed explanations

### **Taffy Style** (`taffy.txt`)
- **Personality**: Playful, engaging, fun
- **Tone**: Light-hearted, humorous, entertaining
- **Focus**: Fun analysis, engaging commentary
- **Language**: Playful Chinese with humor

### **Loveu Style** (`lol_loveu.txt`)
- **Personality**: Warm, encouraging, supportive
- **Tone**: Caring, supportive, loving
- **Focus**: Emotional support, encouragement
- **Language**: Warm Chinese with caring phrases

## 🔄 Prompt Management

### **Dynamic Prompt Loading**
```python
from services.prompts import prompt_manager

# Get available styles
styles = prompt_manager.get_available_styles()

# Load specific prompt
prompt = prompt_manager.get_prompt("azi")

# Get voice ID for style
voice_id = prompt_manager.get_voice_id("azi")
```

### **Style Selection**
```python
# Select prompt based on user preference
def select_prompt_style(user_preference, game_type):
    if game_type == "LOL":
        if user_preference == "analytical":
            return "azi"
        elif user_preference == "energetic":
            return "dingzhen"
        elif user_preference == "calm":
            return "kfk"
        else:
            return "default"
    elif game_type == "VALORANT":
        return f"va_{user_preference}"
    else:
        return "default"
```

## 🎯 Usage Examples

### **Basic Prompt Usage**
```python
# Load and use prompt
from services.prompts import prompt_manager

# Get prompt for specific style
prompt = prompt_manager.get_prompt("azi")

# Generate analysis
analysis = await generate_analysis(
    match_data=match_data,
    prompt=prompt,
    style="azi"
)
```

### **Style-Based Analysis**
```python
# Analyze with specific style
def analyze_with_style(match_data, style="default"):
    # Load prompt
    prompt = prompt_manager.get_prompt(style)
    
    # Get voice ID
    voice_id = prompt_manager.get_voice_id(style)
    
    # Generate analysis
    analysis = generate_analysis(match_data, prompt)
    
    # Generate audio with specific voice
    audio_file = generate_tts_audio(analysis, voice_id=voice_id)
    
    return analysis, audio_file
```

## 🔧 Configuration Management

### **Adding New Styles**
1. **Create Prompt File**: Add new `.txt` file with prompt template
2. **Update Config**: Add entry to `config.json`
3. **Add Voice Mapping**: Map style to voice ID
4. **Test Integration**: Test new style with system

### **Modifying Existing Styles**
1. **Edit Prompt File**: Modify prompt template
2. **Update Description**: Update config description
3. **Test Changes**: Verify style changes work
4. **Deploy**: Deploy updated prompts

## 📊 Style Characteristics

### **Analysis Focus**
- **Technical**: Data-driven analysis (Azi, KFK DP)
- **Emotional**: Encouraging and supportive (Loveu, Dingzhen)
- **Balanced**: Comprehensive analysis (KFK, Default)
- **Entertaining**: Fun and engaging (Taffy)

### **Language Style**
- **Professional**: Formal, technical language
- **Casual**: Informal, friendly language
- **Encouraging**: Positive, supportive language
- **Humorous**: Light-hearted, entertaining language

## 🎵 Voice Integration

### **Voice-Style Mapping**
```python
# Voice ID mapping for each style
VOICE_STYLE_MAPPING = {
    "azi": "voice_id_azi",
    "dingzhen": "voice_id_dingzhen",
    "kfk": "voice_id_kfk",
    "kfk_dp": "voice_id_kfk_dp",
    "taffy": "voice_id_taffy",
    "loveu": "voice_id_loveu"
}
```

### **TTS Integration**
```python
# Generate audio with style-specific voice
def generate_style_audio(analysis, style):
    voice_id = prompt_manager.get_voice_id(style)
    audio_file = generate_tts_audio(
        text=analysis,
        voice_id=voice_id,
        output_path=f"audio/analysis_{style}.mp3"
    )
    return audio_file
```

## 🧪 Testing and Validation

### **Prompt Testing**
```python
def test_prompt_style(style, test_data):
    """Test prompt style with sample data"""
    prompt = prompt_manager.get_prompt(style)
    
    # Generate test analysis
    analysis = generate_analysis(test_data, prompt)
    
    # Validate analysis
    if len(analysis) < 100:
        return False, "Analysis too short"
    
    if "游戏" not in analysis:
        return False, "Missing game content"
    
    return True, "Valid analysis"
```

### **Style Validation**
- **Content Quality**: Ensure analysis quality
- **Language Check**: Verify Chinese language usage
- **Length Validation**: Check appropriate length
- **Style Consistency**: Verify style characteristics

## 🔄 Maintenance

### **Regular Maintenance**
- **Prompt Updates**: Regular prompt improvements
- **Style Refinement**: Enhance style characteristics
- **Config Updates**: Update configuration as needed
- **Testing**: Regular style testing

### **Version Control**
- **Change Tracking**: Track prompt changes
- **Backup Strategy**: Backup prompt files
- **Rollback Plan**: Ability to rollback changes
- **Documentation**: Document style changes

## 📈 Performance Optimization

### **Prompt Optimization**
- **Length Optimization**: Balance detail and length
- **Language Efficiency**: Optimize Chinese language usage
- **Style Consistency**: Maintain style characteristics
- **Quality Control**: Ensure analysis quality

### **System Integration**
- **Fast Loading**: Quick prompt loading
- **Memory Efficiency**: Efficient prompt storage
- **Caching**: Cache frequently used prompts
- **Error Handling**: Robust prompt handling

## 🎯 Customization

### **User Preferences**
```python
# Set user style preference
def set_user_style(user_id, style):
    user_preferences[user_id] = style
    save_user_preferences()

# Get user style
def get_user_style(user_id):
    return user_preferences.get(user_id, "default")
```

### **Dynamic Style Selection**
```python
# Select style based on context
def select_contextual_style(game_performance, user_mood):
    if game_performance["kda"] > 3.0:
        return "dingzhen"  # Energetic for good performance
    elif game_performance["kda"] < 1.0:
        return "loveu"     # Encouraging for poor performance
    else:
        return "kfk"       # Balanced for average performance
```

---

*This directory contains the AI prompt system that powers the LOLBOT analysis generation. Each prompt file defines a unique personality and analysis style for different user preferences and game contexts.*