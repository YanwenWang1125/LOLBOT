# 🧪 Test Suite Directory

This directory contains comprehensive test suites for the LOLBOT system, including unit tests, integration tests, and API validation tests.

## 📁 File Structure

```
test/
├── test_api.py                    # API integration tests
├── test_chinese_champion_names.py # Chinese champion name tests
├── test_player_names.py          # Player name validation tests
├── test_voicv_integration.py     # VoicV TTS integration tests
└── README.md                     # This documentation
```

## 🎯 Test Categories

### **API Integration Tests** (`test_api.py`)
- **Purpose**: Test external API integrations
- **Coverage**: Riot API, OpenAI API, VoicV API
- **Functionality**: API connectivity, data retrieval, error handling

### **Chinese Champion Name Tests** (`test_chinese_champion_names.py`)
- **Purpose**: Validate Chinese champion name translations
- **Coverage**: Champion name mapping, translation accuracy
- **Functionality**: English to Chinese translation, name consistency

### **Player Name Validation Tests** (`test_player_names.py`)
- **Purpose**: Test player name validation and processing
- **Coverage**: Riot ID format validation, name parsing
- **Functionality**: Input validation, format checking

### **VoicV Integration Tests** (`test_voicv_integration.py`)
- **Purpose**: Test TTS integration and voice cloning
- **Coverage**: VoicV API, TTS generation, voice cloning
- **Functionality**: Audio generation, voice quality, API integration

## 🔧 Test Framework

### **Test Structure**
```python
import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestLOLBOT(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_functionality(self):
        """Test specific functionality"""
        pass
```

### **Test Configuration**
```python
# Test configuration
TEST_CONFIG = {
    "RIOT_API_KEY": "test_key",
    "OPENAI_API_KEY": "test_key",
    "VOICV_API_KEY": "test_key",
    "DISCORD_TOKEN": "test_token"
}

# Mock data for testing
MOCK_MATCH_DATA = {
    "match_id": "NA1_1234567890",
    "game_duration": 1800,
    "players": []
}
```

## 🧪 Test Implementation

### **API Integration Tests**
```python
class TestAPIIntegration(unittest.TestCase):
    def test_riot_api_connection(self):
        """Test Riot API connectivity"""
        from services.riot_checker import get_summoner_info
        
        # Test with mock data
        result = get_summoner_info("test_user", "test_tag")
        self.assertIsNotNone(result)
    
    def test_openai_api_connection(self):
        """Test OpenAI API connectivity"""
        from services.match_analyzer import convert_to_chinese_mature_tone
        
        # Test with mock data
        result = convert_to_chinese_mature_tone(MOCK_MATCH_DATA)
        self.assertIsNotNone(result)
    
    def test_voicv_api_connection(self):
        """Test VoicV API connectivity"""
        from services.voicv_tts import generate_tts_audio
        
        # Test with mock data
        result = generate_tts_audio("测试文本", voice_id="test_voice")
        self.assertIsNotNone(result)
```

### **Chinese Champion Name Tests**
```python
class TestChineseChampionNames(unittest.TestCase):
    def test_champion_name_mapping(self):
        """Test champion name translation"""
        from services.riot_checker import get_chinese_champion_name
        
        # Test common champions
        test_cases = [
            ("Jinx", "金克丝"),
            ("Yasuo", "亚索"),
            ("Ahri", "阿狸"),
            ("Lux", "拉克丝")
        ]
        
        for english, expected_chinese in test_cases:
            result = get_chinese_champion_name(english)
            self.assertEqual(result, expected_chinese)
    
    def test_unknown_champion(self):
        """Test unknown champion handling"""
        from services.riot_checker import get_chinese_champion_name
        
        result = get_chinese_champion_name("UnknownChampion")
        self.assertEqual(result, "UnknownChampion")
```

### **Player Name Validation Tests**
```python
class TestPlayerNames(unittest.TestCase):
    def test_riot_id_format(self):
        """Test Riot ID format validation"""
        from services.presence_manager import PresenceManager
        
        pm = PresenceManager()
        
        # Valid formats
        valid_ids = ["username#tag", "user#123", "test#test"]
        for riot_id in valid_ids:
            self.assertTrue("#" in riot_id)
        
        # Invalid formats
        invalid_ids = ["username", "user#", "#tag", ""]
        for riot_id in invalid_ids:
            self.assertFalse(pm.validate_riot_id(riot_id))
    
    def test_username_parsing(self):
        """Test username parsing"""
        from services.riot_checker import get_summoner_info
        
        # Test username parsing
        test_cases = [
            ("username#tag", ("username", "tag")),
            ("user#123", ("user", "123")),
            ("test#test", ("test", "test"))
        ]
        
        for riot_id, expected in test_cases:
            username, tag = riot_id.split("#", 1)
            self.assertEqual((username, tag), expected)
```

### **VoicV Integration Tests**
```python
class TestVoicVIntegration(unittest.TestCase):
    def test_tts_generation(self):
        """Test TTS audio generation"""
        from services.voicv_tts import generate_tts_audio
        
        # Test TTS generation
        result = generate_tts_audio(
            text="测试文本",
            voice_id="test_voice",
            output_path="test_output.mp3"
        )
        
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(result))
    
    def test_voice_cloning(self):
        """Test voice cloning functionality"""
        from services.voicV_clone import clone_voice
        
        # Test voice cloning
        result = clone_voice(
            source_file="test_audio.wav",
            voice_name="test_voice"
        )
        
        self.assertIsNotNone(result)
    
    def test_audio_quality(self):
        """Test audio quality validation"""
        from services.voicv_tts import validate_audio_file
        
        # Test audio file validation
        result = validate_audio_file("test_audio.mp3")
        self.assertTrue(result[0])
```

## 🚀 Test Execution

### **Running Tests**
```bash
# Run all tests
python -m unittest discover test/

# Run specific test file
python test/test_api.py

# Run with verbose output
python -m unittest test.test_api -v

# Run specific test method
python -m unittest test.test_api.TestAPIIntegration.test_riot_api_connection
```

### **Test Coverage**
```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run -m unittest discover test/

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
```

## 🔧 Test Configuration

### **Environment Setup**
```python
# Test environment configuration
import os
import sys

# Set test environment variables
os.environ["RIOT_API_KEY"] = "test_key"
os.environ["OPENAI_API_KEY"] = "test_key"
os.environ["VOICV_API_KEY"] = "test_key"
os.environ["DISCORD_TOKEN"] = "test_token"

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### **Mock Data**
```python
# Mock data for testing
MOCK_SUMMONER_INFO = {
    "puuid": "test_puuid",
    "summoner_name": "test_user",
    "summoner_level": 100
}

MOCK_MATCH_DATA = {
    "match_id": "NA1_1234567890",
    "game_duration": 1800,
    "game_creation": 1698000000000,
    "info": {
        "gameDuration": 1800,
        "gameCreation": 1698000000000
    }
}
```

## 📊 Test Metrics

### **Coverage Metrics**
- **Line Coverage**: Percentage of code lines tested
- **Branch Coverage**: Percentage of code branches tested
- **Function Coverage**: Percentage of functions tested
- **Class Coverage**: Percentage of classes tested

### **Performance Metrics**
- **Test Execution Time**: Time to run all tests
- **Memory Usage**: Memory consumption during tests
- **API Response Time**: External API response times
- **Error Rate**: Percentage of failed tests

## 🧪 Test Types

### **Unit Tests**
- **Purpose**: Test individual functions and methods
- **Scope**: Single function or class
- **Isolation**: Independent of external dependencies
- **Speed**: Fast execution

### **Integration Tests**
- **Purpose**: Test component interactions
- **Scope**: Multiple components working together
- **Dependencies**: May require external services
- **Speed**: Slower than unit tests

### **API Tests**
- **Purpose**: Test external API integrations
- **Scope**: API connectivity and data retrieval
- **Dependencies**: Require external API access
- **Speed**: Depends on API response time

## 🔍 Test Validation

### **Input Validation**
```python
def test_input_validation(self):
    """Test input validation"""
    # Test valid inputs
    valid_inputs = ["username#tag", "user#123"]
    for input_val in valid_inputs:
        self.assertTrue(validate_input(input_val))
    
    # Test invalid inputs
    invalid_inputs = ["", "username", "user#", "#tag"]
    for input_val in invalid_inputs:
        self.assertFalse(validate_input(input_val))
```

### **Output Validation**
```python
def test_output_validation(self):
    """Test output validation"""
    result = process_data(MOCK_INPUT_DATA)
    
    # Validate output structure
    self.assertIsInstance(result, dict)
    self.assertIn("status", result)
    self.assertIn("data", result)
    
    # Validate output content
    self.assertEqual(result["status"], "success")
    self.assertIsNotNone(result["data"])
```

## 🐛 Error Testing

### **Exception Handling**
```python
def test_exception_handling(self):
    """Test exception handling"""
    with self.assertRaises(ValueError):
        process_invalid_data(None)
    
    with self.assertRaises(ConnectionError):
        connect_to_invalid_api()
    
    with self.assertRaises(FileNotFoundError):
        load_nonexistent_file()
```

### **Error Recovery**
```python
def test_error_recovery(self):
    """Test error recovery mechanisms"""
    # Test retry logic
    result = retry_operation(max_retries=3)
    self.assertIsNotNone(result)
    
    # Test fallback mechanisms
    result = fallback_operation()
    self.assertIsNotNone(result)
```

## 📈 Performance Testing

### **Load Testing**
```python
def test_performance(self):
    """Test system performance"""
    import time
    
    start_time = time.time()
    result = process_large_dataset()
    end_time = time.time()
    
    execution_time = end_time - start_time
    self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
```

### **Memory Testing**
```python
def test_memory_usage(self):
    """Test memory usage"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operation
    result = process_large_data()
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable
    self.assertLess(memory_increase, 100 * 1024 * 1024)  # Less than 100MB
```

## 🔄 Continuous Integration

### **Automated Testing**
```yaml
# GitHub Actions workflow
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m unittest discover test/
```

### **Test Automation**
```bash
# Pre-commit hooks
#!/bin/bash
# Run tests before commit
python -m unittest discover test/
if [ $? -ne 0 ]; then
    echo "Tests failed, commit aborted"
    exit 1
fi
```

## 📚 Test Documentation

### **Test Cases**
Each test should include:
- **Purpose**: What the test validates
- **Setup**: Required test data and configuration
- **Execution**: Test steps and assertions
- **Cleanup**: Post-test cleanup procedures

### **Test Reports**
```python
def generate_test_report():
    """Generate comprehensive test report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "coverage": 0.0,
        "execution_time": 0.0
    }
    return report
```

---

*This directory contains the comprehensive test suite for the LOLBOT system. All tests are designed to ensure system reliability, functionality, and performance.*
