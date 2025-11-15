# AI Real-time Subtitle Tool

---

**语言**: 中文 | [English](README_EN.md)

---

A desktop AI floating window tool for Windows that can capture system audio in real-time and convert it to text subtitles using AI models.

## 🔗 Quick Navigation

- 📦 **[Download Packaged Version](#getting-the-app)** - No Python required
- 💿 **[Installation Guide](docs/INSTALL.md)** - Dependency installation
- 🎤 **[Audio Setup](docs/AUDIO_SETUP.md)** - Fix "No speech detected" issues
- 🎧 **[External Device Setup](docs/EXTERNAL_AUDIO_SETUP.md)** - For external speakers/headphones
- ⚙️ **[GUI Configuration](docs/SETTINGS_GUIDE.md)** - Visual configuration interface
- 🚀 **[5-Minute Quick Start](docs/QUICKSTART_ALIYUN.md)** - Aliyun configuration
- 🔧 **[How to Build](docs/HOW_TO_BUILD.md)** - Build in 3 steps
- 📦 **[Build Options](docs/BUILD_OPTIONS.md)** - Standard vs Local Model
- 🔌 **[Runtime Installation](docs/RUNTIME_INSTALL_GUIDE.md)** - Install local model on-demand (Recommended)
- 📚 **[Complete Guide](docs/COMPLETE_GUIDE.md)** - All documentation

## ✨ Features

- 🎙️ **Real-time Audio Capture**: Capture Windows system audio (WASAPI Loopback)
- 🤖 **AI Speech Recognition**: Support multiple AI services (OpenAI Whisper, Azure Speech, Aliyun Bailian, Local Whisper)
- 💬 **Real-time Subtitle Display**: Beautiful floating subtitle window with drag and transparency support
- ⚙️ **GUI Configuration**: Visual configuration interface, no manual file editing required
- 🎨 **Modern UI**: Modern interface design based on PyQt5
- 📦 **One-Click Build**: Package as standalone exe, ready to use

## 📋 System Requirements

- Windows 10/11
- Python 3.8+ (for development)
- Microphone or system audio output device

## 📦 Getting the App

### Option 1: Download Packaged Version (Recommended)

Download the pre-packaged Windows executable, no Python installation required.

**Usage Steps**:
1. Download and extract `AI_Subtitle_Portable.zip`
2. Run `Setup_Wizard.bat` for quick configuration
3. Double-click `AI_Subtitle.exe` to launch

### Option 2: Run from Source

For developers or users who need customization.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ai_subtitle_tool
pip install -r requirements.txt
```

**If you encounter installation issues**, check the detailed **[Installation Guide](docs/INSTALL.md)**

**Quick install core dependencies**:
```bash
# Install only required core dependencies
pip install -r requirements-minimal.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit the `.env` file, choose an AI service and configure the API key:

#### Using OpenAI Whisper API (Recommended)

```env
AI_SERVICE=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=whisper-1
```

#### Using Azure Speech Service

```env
AI_SERVICE=azure
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus
```

#### Using Aliyun Bailian (Recommended for China)

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=your_aliyun_api_key_here
ALIYUN_MODEL=paraformer-realtime-v2
```

For detailed configuration, see: [Aliyun Bailian Setup Guide](docs/aliyun_setup.md)

#### Using Local Whisper Model

```env
AI_SERVICE=local_whisper
```

Additional installation required:
```bash
pip install openai-whisper
```

### 3. Enable Windows Audio Loopback

To capture system audio, enable "Stereo Mix":

1. Right-click the volume icon in the taskbar
2. Select "Sound settings" → "Sound Control Panel"
3. Switch to "Recording" tab
4. Right-click empty space, check "Show Disabled Devices"
5. Find "Stereo Mix", right-click to enable
6. Set as default recording device (optional)

### 4. Run the Application

```bash
python main.py
```

## 🎮 Usage Instructions

1. **Launch App**: Run `python main.py` to display the floating subtitle window
2. **Open Settings**: Click the "⚙" button on the window to open configuration
3. **Configure Service**: Select AI service and enter API key in the configuration interface
4. **Save Config**: Click "Save" button, configuration will be saved to .env file
5. **Start Capture**: Click "▶ Start" button to begin audio capture
6. **View Subtitles**: Real-time transcribed text will be displayed in the window
7. **Stop Capture**: Click "■ Stop" button to stop capture
8. **Move Window**: Left-click and drag to move the window
9. **Close App**: Click "✕" button in the top-right corner to close

## ⚙️ Configuration

### GUI Configuration (Recommended)

Click the "⚙" button on the main window to open configuration interface, where you can:
- Select AI service type
- Enter API keys
- Adjust audio parameters
- Customize interface settings
- Preview effects in real-time

For details, see: [GUI Configuration Guide](docs/SETTINGS_GUIDE.md)

### Manual Configuration

### Audio Settings

```env
SAMPLE_RATE=16000          # Sample rate (Hz)
CHUNK_DURATION=3           # Audio chunk duration (seconds)
AUDIO_DEVICE_INDEX=-1      # Audio device index (-1 for auto)
```

### UI Settings

```env
WINDOW_WIDTH=800           # Window width
WINDOW_HEIGHT=120          # Window height
WINDOW_OPACITY=0.85        # Window opacity (0.0-1.0)
FONT_SIZE=24               # Font size
```

## 🔧 Troubleshooting

### Issue 1: Cannot Capture Audio

**Solution**:
- Ensure "Stereo Mix" device is enabled
- Check console output for device list after running
- Manually specify `AUDIO_DEVICE_INDEX` in `.env`

### Issue 2: PyAudio Installation Failed

**Solution**:
```bash
# Windows users can use pipwin
pip install pipwin
pipwin install pyaudio

# Or download pre-compiled wheel file
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

### Issue 3: OpenAI API Call Failed

**Solution**:
- Check if API key is correct
- Confirm account has sufficient credits
- Check network connection
- Can set `OPENAI_BASE_URL` to use proxy or other compatible endpoints

### Issue 4: High Transcription Latency

**Solution**:
- Reduce `CHUNK_DURATION` (but increases API call frequency)
- Use local Whisper model (requires good GPU)
- Use Azure Speech Service's real-time streaming recognition

## 📁 Project Structure

```
ai_subtitle_tool/
├── main.py                    # Main entry point
├── config.py                  # Configuration management
├── audio_capture.py           # Audio capture module
├── transcription_service.py   # AI transcription service
├── subtitle_window.py         # Subtitle window UI
├── settings_window.py         # Settings window UI (new)
├── whisper_installer.py       # Local model installer (new)
├── requirements.txt           # Runtime dependencies
├── build_requirements.txt     # Build dependencies
├── .env.example              # Environment variable example
├── build.bat                 # Build script
├── ai_subtitle.spec          # PyInstaller config
├── docs/                     # Documentation
└── README.md                 # Documentation
```

## 🛠️ Tech Stack

- **PyQt5**: Modern GUI framework
- **sounddevice**: Cross-platform audio I/O library
- **OpenAI Whisper API**: Speech recognition service
- **Azure Speech Service**: Microsoft speech service
- **Aliyun Bailian**: Alibaba Cloud AI service
- **NumPy**: Audio data processing

## 📝 Development Roadmap

- [x] Support Aliyun Bailian API
- [x] Windows application packaging and distribution
- [x] GUI configuration interface
- [x] Runtime local model installation
- [ ] Multi-language recognition switching
- [ ] Subtitle history
- [ ] Subtitle export functionality
- [ ] More UI themes
- [ ] Custom hotkeys
- [ ] Audio processing performance optimization
- [ ] Voice Activity Detection (VAD)

## 📦 Building and Distribution

### Developer Build

```bash
# Install build dependencies
pip install -r build_requirements.txt

# Run build script
build.bat

# Create portable version
build_portable.bat
```

**Detailed Documentation**:
- [Build Quick Guide](docs/PACKAGE_QUICKSTART.md)
- [Complete Build Documentation](docs/BUILD_GUIDE.md)
- [Build Options](docs/BUILD_OPTIONS.md)

### Distribution to Users

1. Run `build_portable.bat` to create portable version
2. Generate `AI_Subtitle_Portable.zip`
3. Distribute ZIP file
4. Users extract and run `Setup_Wizard.bat`

**Advantages**:
- ✅ No Python installation required
- ✅ All dependencies packaged
- ✅ Ready to use out of the box
- ✅ Offline usage support

## 🌟 Key Features

### Runtime Local Model Installation

The standard version now supports **on-demand installation of local Whisper model**, no repackaging required!

**Benefits**:
- Small package size (50-200MB)
- Install local model when needed (~224MB)
- One-click installation via GUI
- Flexible and user-friendly

**Usage**:
1. Open settings (⚙ button)
2. Click "Install Local Model"
3. Wait 3-5 minutes
4. Restart application

For details, see: [Runtime Installation Guide](docs/RUNTIME_INSTALL_GUIDE.md)

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 🙏 Acknowledgments

- OpenAI Whisper
- Azure Speech Service
- Aliyun Bailian
- PyQt5 Community
- PyInstaller

---

**Note**: Using AI services may incur costs. Please monitor your usage. It's recommended to test with small quotas first.

## 📚 Documentation

### User Guides
- [Installation Guide](docs/INSTALL.md) - Dependency installation
- [Audio Setup](docs/AUDIO_SETUP.md) - Audio configuration
- [External Device Setup](docs/EXTERNAL_AUDIO_SETUP.md) - External audio devices
- [GUI Configuration](docs/SETTINGS_GUIDE.md) - Visual configuration
- [Quick Start](docs/QUICKSTART_ALIYUN.md) - 5-minute setup

### Developer Guides
- [Build Guide](docs/BUILD_GUIDE.md) - Complete build instructions
- [Build Options](docs/BUILD_OPTIONS.md) - Standard vs Local Model
- [Build Troubleshooting](docs/BUILD_TROUBLESHOOTING.md) - Common issues
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Code organization

### Advanced Topics
- [Runtime Installation](docs/RUNTIME_INSTALL_GUIDE.md) - Install local model on-demand
- [Local Whisper Guide](docs/WHISPER_LOCAL_GUIDE.md) - Local model details
- [Aliyun API Fix](docs/ALIYUN_API_FIX.md) - API troubleshooting

---

**Language**: [中文](README.md) | English
