# AI Real-time Subtitle Tool v1.0.0 Release Notes

## 🎉 First Release

We're excited to announce the official release of **AI Real-time Subtitle Tool v1.0.0**! This is a fully-featured, ready-to-use Windows desktop application that captures system audio in real-time and converts it to text subtitles using AI.

---

## ✨ Core Features

### 🎙️ Real-time Audio Capture
- Windows system audio capture support (WASAPI Loopback)
- Automatic audio device detection
- Stereo Mix and virtual audio device support
- Complete external speaker/headphone support

### 🤖 Multiple AI Services
- **OpenAI Whisper API** - High-precision speech recognition
- **Azure Speech Service** - Microsoft speech service
- **Aliyun Bailian** - Optimized for China, low latency (Recommended)
- **Local Whisper Model** - Offline usage, privacy protection

### 💬 Real-time Subtitle Display
- Beautiful floating subtitle window
- Window dragging and resizing support
- Adjustable transparency
- Customizable font size and color
- Modern UI design

### ⚙️ GUI Configuration
- Intuitive visual configuration interface
- No manual config file editing required
- Real-time preview
- One-click save

### 🔌 Runtime Local Model Installation
- Standard version supports on-demand local Whisper model installation
- Graphical installation interface
- Real-time progress display
- No repackaging required

### 📦 One-Click Build
- Package as standalone exe
- Portable version support
- Setup wizard
- Ready to use out of the box

---

## 🚀 Quick Start

### Download and Install

1. **Download Portable Version**
   - Download `AI_Subtitle_v1.0.0_Portable.zip`
   - Extract to any directory

2. **Run Setup Wizard**
   - Double-click `Setup_Wizard.bat`
   - Follow prompts to select AI service
   - Enter API key

3. **Launch Application**
   - Double-click `AI_Subtitle.exe`
   - Click "▶ Start" button
   - Start using

### System Requirements

- **OS**: Windows 10/11
- **RAM**: At least 2GB available memory
- **Disk**: At least 500MB available space
- **Network**: Internet connection required for cloud APIs

---

## 📋 Key Features

### 1. Multiple AI Service Support

Supports 4 AI services for different needs:

| Service | Features | Use Case |
|---------|----------|----------|
| **Aliyun Bailian** | Chinese optimized, low latency | Recommended for China |
| **OpenAI Whisper** | High accuracy, multilingual | International users |
| **Azure Speech** | Real-time streaming, stable | Enterprise users |
| **Local Whisper** | Offline, privacy | Offline scenarios |

### 2. Comprehensive Audio Support

- ✅ Automatic audio device detection
- ✅ Stereo Mix support
- ✅ Virtual audio device support (VB-Cable, Voicemeeter)
- ✅ Perfect external speaker/headphone support
- ✅ Detailed audio configuration guides

### 3. GUI Configuration Interface

- ✅ AI service selection and configuration
- ✅ Audio device settings
- ✅ Interface customization
- ✅ Real-time preview
- ✅ One-click save

### 4. Runtime Local Model Installation

**Innovative Feature**: Standard version supports on-demand local Whisper model installation

- ✅ Reduced package size (50-200MB)
- ✅ User choice on-demand
- ✅ Graphical installation interface
- ✅ Real-time progress display
- ✅ Automatic installation verification

### 5. Portable Version Support

- ✅ No installation required
- ✅ Setup wizard
- ✅ Ready to use
- ✅ Green software

---

## 📦 Downloads

### Standard Version (Recommended)

**File**: `AI_Subtitle_v1.0.0_Standard.zip`

**Size**: ~50-200MB

**Features**:
- ✅ Supports all cloud AI services
- ✅ Runtime local model installation support
- ✅ Small size, fast download
- ✅ Recommended for most users

### Local Model Version (Optional)

**File**: `AI_Subtitle_v1.0.0_LocalModel.zip`

**Size**: ~1-2GB

**Features**:
- ✅ Pre-installed local Whisper model
- ✅ Fully offline usage support
- ✅ Suitable for offline scenarios
- ✅ No download required on first use

---

## 📚 Documentation

### User Guides
- [Installation Guide](docs/INSTALL.md) - Dependency installation
- [Quick Start](docs/QUICKSTART_ALIYUN.md) - 5-minute setup
- [Audio Setup](docs/AUDIO_SETUP.md) - Audio configuration
- [External Device Setup](docs/EXTERNAL_AUDIO_SETUP.md) - External audio devices
- [GUI Configuration](docs/SETTINGS_GUIDE.md) - Visual configuration
- [User Manual](docs/USER_GUIDE.md) - Complete usage guide

### Developer Guides
- [Build Guide](docs/BUILD_GUIDE.md) - Complete build instructions
- [Build Options](docs/BUILD_OPTIONS.md) - Standard vs Local Model
- [Build Troubleshooting](docs/BUILD_TROUBLESHOOTING.md) - Common issues
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Code organization

### Advanced Topics
- [Runtime Installation](docs/RUNTIME_INSTALL_GUIDE.md) - Install local model on-demand
- [Local Whisper Guide](docs/WHISPER_LOCAL_GUIDE.md) - Local model details
- [Aliyun API Setup](docs/aliyun_setup.md) - Aliyun configuration

---

## 🔧 Tech Stack

- **PyQt5** - Modern GUI framework
- **sounddevice** - Cross-platform audio I/O
- **OpenAI Whisper API** - Speech recognition
- **Azure Speech SDK** - Microsoft speech service
- **Aliyun DashScope** - Alibaba Cloud AI service
- **NumPy** - Audio data processing
- **PyInstaller** - Application packaging

---

## 🐛 Known Issues

### 1. Audio Capture Issues

**Issue**: Some users may encounter "No speech detected"

**Solution**: 
- See [Audio Setup Guide](docs/AUDIO_SETUP.md)
- Enable Stereo Mix
- Use virtual audio devices

### 2. External Device Support

**Issue**: Cannot capture audio when using external speakers/headphones

**Solution**:
- See [External Device Setup Guide](docs/EXTERNAL_AUDIO_SETUP.md)
- Use VB-Cable or Voicemeeter

### 3. Slow First Launch

**Issue**: Slow startup on first launch

**Reason**: 
- Loading dependencies
- Detecting audio devices
- Initializing UI

**Note**: Normal behavior, subsequent launches will be faster

---

## 🔄 Roadmap

### v1.1.0 (Planned)

- [ ] Multi-language recognition switching
- [ ] Subtitle history
- [ ] Subtitle export functionality
- [ ] More UI themes
- [ ] Custom hotkeys

### v1.2.0 (Planned)

- [ ] Voice Activity Detection (VAD)
- [ ] Audio processing optimization
- [ ] GPU acceleration support
- [ ] Batch processing functionality

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

### How to Contribute

1. Fork this project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Thanks to the following open source projects and services:

- **OpenAI Whisper** - Powerful speech recognition model
- **Azure Speech Service** - Microsoft speech service
- **Aliyun Bailian** - AI service optimized for China
- **PyQt5** - Excellent GUI framework
- **PyInstaller** - Application packaging tool

---

## 📞 Support

### Get Help

- 📖 View [Complete Documentation](docs/COMPLETE_GUIDE.md)
- 🐛 Submit [Issue](https://github.com/fz00x0fz/AI-Real-Time-Subtitle-Tool/issues)
- 💬 Join [Discussion](https://github.com/fz00x0fz/AI-Real-Time-Subtitle-Tool/discussions)

### FAQ

See [FAQ](docs/COMPLETE_GUIDE.md#faq) for common questions and answers.

---

## ⚠️ Important Notes

1. **API Costs**: Using cloud AI services may incur costs, please monitor usage
2. **Privacy**: Local model doesn't upload audio data, cloud services upload audio for recognition
3. **Network**: Cloud services require stable internet connection
4. **System Requirements**: Ensure system meets minimum requirements

---

**Enjoy using the tool!** 🎉

Feel free to provide feedback or suggestions anytime!

---

**Release Date**: November 15, 2024  
**Version**: v1.0.0  
**Author**: fz00x0fz

---

**Language**: [中文](RELEASE_v1.0.0_CN.md) | English
