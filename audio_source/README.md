# 🎤 Audio Source Files

This directory contains the original audio source files used for voice cloning and TTS training in the LOLBOT system. These files serve as the foundation for creating personalized voice models.

## 📁 File Structure

```
audio_source/
├── azi.mp3              # Azi voice sample
├── dingzhen_3.wav      # Dingzhen voice sample
├── dp.mp3              # DP voice sample
├── keli.mp4            # Keli voice sample (video format)
├── laotai.mp3          # Laotai voice sample
├── loveu.mp3           # Loveu voice sample
├── Noah.wav            # Noah voice sample
├── taffy.wav           # Taffy voice sample
└── README.md           # This documentation
```

## 🎵 Voice Samples Overview

### **Voice Characteristics**
Each voice sample represents a unique personality and speaking style:

- **`azi.mp3`** - Azi's voice sample
- **`dingzhen_3.wav`** - Dingzhen's voice sample
- **`dp.mp3`** - DP's voice sample
- **`keli.mp4`** - Keli's voice sample (video format)
- **`laotai.mp3`** - Laotai's voice sample
- **`loveu.mp3`** - Loveu's voice sample
- **`Noah.wav`** - Noah's voice sample
- **`taffy.wav`** - Taffy's voice sample

## 🎯 Voice Cloning Process

### **Training Workflow**
1. **Source Audio** → High-quality voice samples
2. **Voice Analysis** → Extract voice characteristics
3. **Model Training** → Train voice cloning model
4. **Voice ID Generation** → Create unique voice identifier
5. **TTS Integration** → Integrate with TTS system
6. **Quality Validation** → Test voice quality

### **Technical Requirements**
- **Audio Quality**: High-quality source audio (44.1kHz+)
- **Duration**: Minimum 10-30 seconds per sample
- **Clarity**: Clear speech without background noise
- **Consistency**: Consistent speaking style and tone
- **Format Support**: MP3, WAV, MP4 formats supported

## 🔧 Voice Model Management

### **Voice ID System**
```python
# Voice ID mapping
VOICE_IDS = {
    "azi": "voice_id_azi",
    "dingzhen": "voice_id_dingzhen", 
    "dp": "voice_id_dp",
    "keli": "voice_id_keli",
    "laotai": "voice_id_laotai",
    "loveu": "voice_id_loveu",
    "noah": "voice_id_noah",
    "taffy": "voice_id_taffy"
}
```

### **Voice Selection**
```python
# Select voice based on style
def get_voice_id(style):
    voice_mapping = {
        "azi": "voice_id_azi",
        "dingzhen": "voice_id_dingzhen",
        "dp": "voice_id_dp",
        "keli": "voice_id_keli",
        "laotai": "voice_id_laotai",
        "loveu": "voice_id_loveu",
        "noah": "voice_id_noah",
        "taffy": "voice_id_taffy"
    }
    return voice_mapping.get(style, "default")
```

## 🎵 Audio Quality Standards

### **Technical Specifications**
- **Sample Rate**: 44.1kHz or higher
- **Bit Depth**: 16-bit or higher
- **Channels**: Mono or Stereo
- **Format**: MP3, WAV, MP4
- **Duration**: 10-60 seconds optimal

### **Quality Requirements**
- **Clarity**: Clear, undistorted audio
- **Consistency**: Uniform speaking style
- **Background**: Minimal background noise
- **Pronunciation**: Clear pronunciation
- **Emotion**: Appropriate emotional tone

## 🔄 Voice Cloning Integration

### **VoicV API Integration**
```python
from services.voicV_clone import clone_voice

# Clone voice from source file
voice_id = await clone_voice(
    source_file="audio_source/azi.mp3",
    voice_name="azi",
    description="Azi's voice for gaming analysis"
)
```

### **TTS Generation**
```python
from services.voicv_tts import generate_tts_audio

# Generate TTS with cloned voice
audio_file = generate_tts_audio(
    text="游戏分析内容",
    voice_id="voice_id_azi",
    output_path="audio/analysis.mp3"
)
```

## 🎯 Voice Personality Mapping

### **Voice Characteristics**
Each voice sample has unique characteristics:

- **Azi**: Professional, analytical tone
- **Dingzhen**: Energetic, enthusiastic style
- **DP**: Calm, methodical approach
- **Keli**: Friendly, supportive voice
- **Laotai**: Experienced, authoritative tone
- **Loveu**: Warm, encouraging style
- **Noah**: Confident, assertive voice
- **Taffy**: Playful, engaging personality

### **Style Selection**
```python
# Voice style mapping
STYLE_VOICE_MAPPING = {
    "professional": "azi",
    "energetic": "dingzhen",
    "calm": "dp",
    "friendly": "keli",
    "authoritative": "laotai",
    "encouraging": "loveu",
    "confident": "noah",
    "playful": "taffy"
}
```

## 🔧 File Management

### **Source File Organization**
```
audio_source/
├── Individual voice samples
├── Quality validation
├── Format standardization
└── Backup and versioning
```

### **File Validation**
```python
def validate_audio_file(file_path):
    """Validate audio file quality and format"""
    import librosa
    
    try:
        # Load audio file
        audio, sr = librosa.load(file_path)
        
        # Check sample rate
        if sr < 22050:
            return False, "Sample rate too low"
        
        # Check duration
        duration = len(audio) / sr
        if duration < 10:
            return False, "Duration too short"
        
        return True, "Valid audio file"
    except Exception as e:
        return False, f"Error: {e}"
```

## 📊 Voice Quality Metrics

### **Quality Assessment**
- **Clarity Score**: Audio clarity measurement
- **Consistency**: Voice consistency across samples
- **Emotional Range**: Appropriate emotional expression
- **Pronunciation**: Clear pronunciation quality
- **Background Noise**: Noise level assessment

### **Performance Metrics**
- **Training Time**: Voice model training duration
- **Success Rate**: Successful voice cloning percentage
- **Quality Score**: Overall voice quality rating
- **User Satisfaction**: User feedback on voice quality

## 🎵 Audio Processing

### **Preprocessing**
```python
def preprocess_audio(file_path):
    """Preprocess audio file for voice cloning"""
    import librosa
    import soundfile as sf
    
    # Load audio
    audio, sr = librosa.load(file_path)
    
    # Normalize audio
    audio = librosa.util.normalize(audio)
    
    # Remove silence
    audio, _ = librosa.effects.trim(audio)
    
    # Resample if needed
    if sr != 22050:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=22050)
    
    return audio, 22050
```

### **Quality Enhancement**
- **Noise Reduction**: Remove background noise
- **Normalization**: Standardize audio levels
- **Format Conversion**: Convert to optimal format
- **Duration Optimization**: Trim to optimal length

## 🔒 Data Security

### **Privacy Considerations**
- **Voice Data**: Contains personal voice characteristics
- **Access Control**: Restricted access to voice samples
- **Data Protection**: Secure storage of voice data
- **Usage Rights**: Proper authorization for voice use

### **Data Protection**
- **File Permissions**: Secure file system permissions
- **Backup Strategy**: Regular backup of voice samples
- **Access Logging**: Monitor access to voice files
- **Secure Storage**: Encrypted storage for sensitive data

## 🧪 Testing and Validation

### **Voice Quality Testing**
```python
def test_voice_quality(voice_id, test_text):
    """Test voice quality with sample text"""
    from services.voicv_tts import generate_tts_audio
    
    # Generate test audio
    audio_file = generate_tts_audio(
        text=test_text,
        voice_id=voice_id,
        output_path="test_audio.mp3"
    )
    
    # Validate audio quality
    return validate_audio_file(audio_file)
```

### **Quality Assurance**
- **Audio Validation**: Verify audio file integrity
- **Voice Testing**: Test voice cloning quality
- **Performance Testing**: Validate TTS performance
- **User Testing**: Gather user feedback

## 📚 Integration Examples

### **Voice Cloning Workflow**
```python
# Complete voice cloning workflow
async def clone_voice_workflow(source_file, voice_name):
    # 1. Validate source file
    is_valid, message = validate_audio_file(source_file)
    if not is_valid:
        raise ValueError(f"Invalid audio file: {message}")
    
    # 2. Preprocess audio
    audio, sr = preprocess_audio(source_file)
    
    # 3. Clone voice
    voice_id = await clone_voice(
        source_file=source_file,
        voice_name=voice_name
    )
    
    # 4. Test voice quality
    quality_score = test_voice_quality(voice_id, "测试文本")
    
    return voice_id, quality_score
```

### **Voice Selection Logic**
```python
def select_voice_for_analysis(game_type, performance):
    """Select appropriate voice based on context"""
    if game_type == "LOL":
        if performance["kda"] > 3.0:
            return "noah"  # Confident voice for good performance
        else:
            return "loveu"  # Encouraging voice for improvement
    elif game_type == "VALORANT":
        return "azi"  # Professional voice for Valorant
    else:
        return "default"
```

## 🔄 Maintenance

### **Regular Maintenance**
- **File Validation**: Regular audio file quality checks
- **Voice Testing**: Periodic voice quality testing
- **Backup Management**: Regular backup of voice samples
- **Performance Monitoring**: Monitor voice cloning performance

### **Troubleshooting**
- **File Corruption**: Check audio file integrity
- **Voice Quality**: Validate voice cloning quality
- **Format Issues**: Verify audio format compatibility
- **Performance Issues**: Monitor voice cloning performance

## 📈 Performance Optimization

### **Voice Cloning Optimization**
- **Training Efficiency**: Optimize voice model training
- **Quality Balance**: Balance quality and speed
- **Resource Management**: Efficient resource usage
- **Error Handling**: Robust error handling

### **Storage Optimization**
- **File Compression**: Optimize audio file storage
- **Format Selection**: Choose optimal audio formats
- **Access Patterns**: Optimize file access
- **Memory Usage**: Efficient memory management

---

*This directory contains the source audio files that form the foundation of the LOLBOT voice cloning system. These files are used to create personalized voice models for different analysis styles and personalities.*
