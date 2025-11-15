# AI实时字幕工具 (AI Real-time Subtitle Tool)

一个支持在Windows上运行的桌面AI浮窗工具，可以实时捕获系统音频并通过AI大模型转换为文字字幕显示在桌面上。

## 🔗 快速导航

- 📦 **[下载打包版本](#获取应用)** - 无需Python环境
- 💿 **[安装指南](INSTALL.md)** - 依赖安装详解
- 🎤 **[音频设置](AUDIO_SETUP.md)** - 解决"检测不到语音"问题
- 🎧 **[外接设备配置](EXTERNAL_AUDIO_SETUP.md)** - 外接音箱/耳机用户必读
- ⚙️ **[图形化配置](SETTINGS_GUIDE.md)** - 可视化配置界面
- 🚀 **[5分钟快速开始](QUICKSTART_ALIYUN.md)** - 阿里云配置
- 🔧 **[如何打包](HOW_TO_BUILD.md)** - 3步完成打包
- 📦 **[打包选项](BUILD_OPTIONS.md)** - 标准版 vs 本地模型版
- 🔌 **[运行时安装](RUNTIME_INSTALL_GUIDE.md)** - 按需安装本地模型（推荐）
- 📚 **[完整指南](COMPLETE_GUIDE.md)** - 所有文档导航

## ✨ 功能特性

- 🎙️ **实时音频捕获**: 支持捕获Windows系统播放的音频（WASAPI Loopback）
- 🤖 **AI语音识别**: 支持多种AI服务（OpenAI Whisper、Azure Speech、阿里云百炼、本地Whisper）
- 💬 **实时字幕显示**: 美观的浮动字幕窗口，支持拖拽和透明度调节
- ⚙️ **图形化配置**: 可视化配置界面，无需手动编辑文件
- 🎨 **现代UI**: 基于PyQt5的现代化界面设计
- 📦 **一键打包**: 支持打包为独立exe，开箱即用

## 📋 系统要求

- Windows 10/11
- Python 3.8+ (开发运行)
- 麦克风或系统音频输出设备

## 📦 获取应用

### 方式1: 下载打包版本（推荐）

直接下载已打包的Windows可执行文件，无需安装Python环境。

**使用步骤**:
1. 下载并解压 `AI实时字幕_便携版.zip`
2. 运行 `配置向导.bat` 进行快速配置
3. 双击 `AI实时字幕.exe` 启动应用

### 方式2: 从源码运行

适合开发者或需要自定义的用户。

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ai_subtitle_tool
pip install -r requirements.txt
```

**如果遇到安装问题**，请查看详细的 **[安装指南](INSTALL.md)**

**快速安装核心依赖**:
```bash
# 仅安装必需的核心依赖
pip install -r requirements-minimal.txt
```

### 2. 配置环境变量

复制`.env.example`为`.env`并配置：

```bash
cp .env.example .env
```

编辑`.env`文件，选择一个AI服务并配置相应的API密钥：

#### 使用OpenAI Whisper API (推荐)

```env
AI_SERVICE=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=whisper-1
```

#### 使用Azure Speech Service

```env
AI_SERVICE=azure
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=eastus
```

#### 使用阿里云百炼 (国内推荐)

```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=your_aliyun_api_key_here
ALIYUN_MODEL=paraformer-realtime-v2
```

详细配置请参考：[阿里云百炼配置指南](docs/aliyun_setup.md)

#### 使用本地Whisper模型

```env
AI_SERVICE=local_whisper
```

需要额外安装：
```bash
pip install openai-whisper
```

### 3. 启用Windows音频回环

为了捕获系统播放的音频，需要启用"立体声混音"：

1. 右键点击任务栏的音量图标
2. 选择"声音设置" → "声音控制面板"
3. 切换到"录制"选项卡
4. 右键空白处，勾选"显示已禁用的设备"
5. 找到"立体声混音"或"Stereo Mix"，右键启用
6. 设置为默认录音设备（可选）

### 4. 运行应用

```bash
python main.py
```

## 🎮 使用说明

1. **启动应用**: 运行`python main.py`后会显示浮动字幕窗口
2. **打开设置**: 点击窗口上的"⚙"按钮打开配置界面
3. **配置服务**: 在配置界面中选择AI服务并填写API密钥
4. **保存配置**: 点击"保存"按钮，配置会自动保存到.env文件
5. **开始捕获**: 点击"▶ 开始"按钮开始捕获音频
6. **查看字幕**: 实时转录的文字会显示在窗口中
7. **停止捕获**: 点击"■ 停止"按钮停止捕获
8. **拖动窗口**: 鼠标左键拖动窗口可以移动位置
9. **关闭应用**: 点击右上角"✕"按钮关闭

## ⚙️ 配置说明

### 图形化配置（推荐）

点击主窗口的"⚙"按钮打开配置界面，可以：
- 选择AI服务类型
- 填写API密钥
- 调整音频参数
- 自定义界面设置
- 实时预览效果

详细说明请查看：[图形化配置指南](SETTINGS_GUIDE.md)

### 手动配置

### 音频设置

```env
SAMPLE_RATE=16000          # 采样率 (Hz)
CHUNK_DURATION=3           # 音频块时长 (秒)
AUDIO_DEVICE_INDEX=-1      # 音频设备索引 (-1为自动选择)
```

### UI设置

```env
WINDOW_WIDTH=800           # 窗口宽度
WINDOW_HEIGHT=120          # 窗口高度
WINDOW_OPACITY=0.85        # 窗口透明度 (0.0-1.0)
FONT_SIZE=24               # 字体大小
```

## 🔧 故障排除

### 问题1: 无法捕获音频

**解决方案**:
- 确保已启用"立体声混音"设备
- 运行程序后查看控制台输出的设备列表
- 在`.env`中手动指定`AUDIO_DEVICE_INDEX`

### 问题2: PyAudio安装失败

**解决方案**:
```bash
# Windows用户可以使用pipwin
pip install pipwin
pipwin install pyaudio

# 或者下载预编译的wheel文件
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

### 问题3: OpenAI API调用失败

**解决方案**:
- 检查API密钥是否正确
- 确认账户有足够的额度
- 检查网络连接
- 可以设置`OPENAI_BASE_URL`使用代理或其他兼容端点

### 问题4: 转录延迟较高

**解决方案**:
- 减小`CHUNK_DURATION`（但会增加API调用频率）
- 使用本地Whisper模型（需要较好的GPU）
- 使用Azure Speech Service的实时流式识别

## 📁 项目结构

```
ai_subtitle_tool/
├── main.py                    # 主程序入口
├── config.py                  # 配置管理
├── audio_capture.py           # 音频捕获模块
├── transcription_service.py   # AI转录服务
├── subtitle_window.py         # 字幕窗口UI
├── settings_window.py         # 配置窗口UI (新增)
├── requirements.txt           # 运行依赖
├── build_requirements.txt     # 打包依赖
├── .env.example              # 环境变量示例
├── build.bat                 # 打包脚本
├── ai_subtitle.spec          # PyInstaller配置
└── README.md                 # 说明文档
```

## 🛠️ 技术栈

- **PyQt5**: 现代化GUI框架
- **sounddevice**: 跨平台音频I/O库
- **OpenAI Whisper API**: 语音识别服务
- **Azure Speech Service**: 微软语音服务
- **NumPy**: 音频数据处理

## 📝 开发计划

- [x] 支持阿里云百炼API
- [x] Windows应用打包和分发
- [ ] 支持多语言识别切换
- [ ] 添加字幕历史记录
- [ ] 支持字幕导出功能
- [ ] 添加更多UI主题
- [ ] 支持自定义快捷键
- [ ] 优化音频处理性能
- [ ] 添加语音活动检测(VAD)

## 📦 打包和分发

### 开发者打包

```bash
# 安装打包依赖
pip install -r build_requirements.txt

# 运行打包脚本
build.bat

# 创建便携版
build_portable.bat
```

**详细文档**:
- [打包快速指南](PACKAGE_QUICKSTART.md)
- [完整打包文档](BUILD_GUIDE.md)

### 分发给用户

1. 运行 `build_portable.bat` 创建便携版
2. 生成 `AI实时字幕_便携版.zip`
3. 分发ZIP文件
4. 用户解压后运行 `配置向导.bat`

**优势**:
- ✅ 无需安装Python环境
- ✅ 所有依赖已打包
- ✅ 开箱即用
- ✅ 支持离线使用

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- OpenAI Whisper
- Azure Speech Service
- 阿里云百炼
- PyQt5 Community
- PyInstaller

## 📚 文档导航

### 用户指南
- [安装指南](docs/INSTALL.md) - 依赖安装详解
- [音频设置](docs/AUDIO_SETUP.md) - 音频配置说明
- [外接设备配置](docs/EXTERNAL_AUDIO_SETUP.md) - 外接音频设备
- [图形化配置](docs/SETTINGS_GUIDE.md) - 可视化配置
- [快速开始](docs/QUICKSTART_ALIYUN.md) - 5分钟上手

### 开发者指南
- [打包指南](docs/BUILD_GUIDE.md) - 完整打包说明
- [打包选项](docs/BUILD_OPTIONS.md) - 标准版 vs 本地模型版
- [打包故障排除](docs/BUILD_TROUBLESHOOTING.md) - 常见问题
- [项目结构](docs/PROJECT_STRUCTURE.md) - 代码组织

### 高级主题
- [运行时安装](docs/RUNTIME_INSTALL_GUIDE.md) - 按需安装本地模型
- [本地Whisper指南](docs/WHISPER_LOCAL_GUIDE.md) - 本地模型详解
- [阿里云API修复](docs/ALIYUN_API_FIX.md) - API故障排除

---

**注意**: 使用AI服务可能会产生费用，请注意控制使用量。建议先使用小额度测试。

---

**语言**: 中文 | [English](README_EN.md)
