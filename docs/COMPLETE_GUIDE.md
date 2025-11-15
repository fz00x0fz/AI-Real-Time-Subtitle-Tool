# AI实时字幕工具 - 完整指南

> 从开发到打包分发的完整流程

## 📚 文档导航

### 快速开始
- **[README.md](README.md)** - 项目主文档
- **[QUICKSTART_ALIYUN.md](QUICKSTART_ALIYUN.md)** - 阿里云5分钟快速配置

### 开发文档
- **[setup_guide.md](setup_guide.md)** - 详细安装配置指南
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - 项目结构说明
- **[docs/aliyun_setup.md](docs/aliyun_setup.md)** - 阿里云详细配置

### 打包分发
- **[PACKAGE_QUICKSTART.md](PACKAGE_QUICKSTART.md)** - 打包快速指南
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - 完整打包文档
- **[PACKAGE_UPDATE.md](PACKAGE_UPDATE.md)** - 打包功能说明

### 更新日志
- **[CHANGELOG_ALIYUN.md](CHANGELOG_ALIYUN.md)** - 阿里云集成更新
- **[UPDATE_SUMMARY.md](UPDATE_SUMMARY.md)** - 阿里云更新总结

## 🎯 使用场景指南

### 场景1: 普通用户使用

**目标**: 快速使用应用，无需了解技术细节

**步骤**:
1. 下载 `AI实时字幕_便携版.zip`
2. 解压到任意目录
3. 运行 `配置向导.bat`
4. 按提示配置API密钥
5. 双击 `AI实时字幕.exe` 启动

**推荐文档**:
- 使用说明.txt（打包版中包含）
- README_便携版.txt

### 场景2: 开发者运行

**目标**: 从源码运行，进行开发和调试

**步骤**:
```bash
# 1. 克隆项目
git clone <repository>
cd ai_subtitle_tool

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境
copy .env.example .env
notepad .env

# 4. 运行
python main.py
```

**推荐文档**:
- [README.md](README.md) - 第2节"从源码运行"
- [setup_guide.md](setup_guide.md)

### 场景3: 打包分发

**目标**: 将应用打包为可执行文件分发

**步骤**:
```bash
# 1. 安装打包依赖
pip install -r build_requirements.txt

# 2. 生成图标（可选）
python create_icon.py

# 3. 打包应用
build.bat

# 4. 创建便携版
build_portable.bat

# 5. 分发ZIP文件
AI实时字幕_便携版.zip
```

**推荐文档**:
- [PACKAGE_QUICKSTART.md](PACKAGE_QUICKSTART.md)
- [BUILD_GUIDE.md](BUILD_GUIDE.md)

### 场景4: 配置阿里云

**目标**: 使用阿里云百炼API进行语音识别

**步骤**:
```bash
# 1. 获取API密钥
# 访问 https://dashscope.aliyun.com/

# 2. 使用阿里云配置模板
copy .env.aliyun.example .env

# 3. 编辑配置
notepad .env
# 填入: ALIYUN_API_KEY=sk-your-key

# 4. 测试配置
python test_aliyun.py

# 5. 运行应用
python main.py
```

**推荐文档**:
- [QUICKSTART_ALIYUN.md](QUICKSTART_ALIYUN.md)
- [docs/aliyun_setup.md](docs/aliyun_setup.md)

## 🔧 功能配置指南

### 音频捕获配置

**启用立体声混音**:
1. 右键任务栏音量图标
2. 声音设置 → 声音控制面板
3. 录制选项卡 → 显示已禁用的设备
4. 启用"立体声混音"

**配置参数**:
```env
SAMPLE_RATE=16000        # 采样率
CHUNK_DURATION=3         # 音频块时长
AUDIO_DEVICE_INDEX=-1    # 设备索引
```

### AI服务配置

**OpenAI Whisper**:
```env
AI_SERVICE=openai
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=whisper-1
```

**Azure Speech**:
```env
AI_SERVICE=azure
AZURE_SPEECH_KEY=your-key
AZURE_SPEECH_REGION=eastus
```

**阿里云百炼**:
```env
AI_SERVICE=aliyun
ALIYUN_API_KEY=sk-your-key
ALIYUN_MODEL=paraformer-realtime-v2
```

**本地Whisper**:
```env
AI_SERVICE=local_whisper
```

### UI配置

```env
WINDOW_WIDTH=800         # 窗口宽度
WINDOW_HEIGHT=120        # 窗口高度
WINDOW_OPACITY=0.85      # 透明度
FONT_SIZE=24             # 字体大小
```

## 🚀 快速命令参考

### 开发命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py

# 测试阿里云配置
python test_aliyun.py

# 列出音频设备
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### 打包命令

```bash
# 安装打包依赖
pip install -r build_requirements.txt

# 生成图标
python create_icon.py

# 标准打包
build.bat

# 便携版打包
build_portable.bat

# 清理构建文件
rmdir /s /q build dist
```

### 测试命令

```bash
# 测试配置
python -c "from config import Config; Config.validate()"

# 测试音频捕获
python -c "from audio_capture import AudioCapture; ac = AudioCapture(); ac.list_devices()"

# 测试AI服务
python test_aliyun.py
```

## 📊 性能优化指南

### 降低延迟

```env
# 减小音频块时长
CHUNK_DURATION=2

# 使用实时模型
ALIYUN_MODEL=paraformer-realtime-v2
```

### 提高准确率

```env
# 增加音频块时长
CHUNK_DURATION=4

# 使用高精度模型
ALIYUN_MODEL=paraformer-v2
```

### 降低成本

```env
# 使用本地模型（免费）
AI_SERVICE=local_whisper

# 或增加音频块时长减少API调用
CHUNK_DURATION=5
```

### 优化打包大小

```bash
# 使用虚拟环境
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
build.bat
```

## 🔍 故障排除索引

### 安装问题

| 问题 | 解决方案 | 文档 |
|------|---------|------|
| PyAudio安装失败 | 使用pipwin | [setup_guide.md](setup_guide.md) |
| 依赖冲突 | 使用虚拟环境 | [README.md](README.md) |

### 配置问题

| 问题 | 解决方案 | 文档 |
|------|---------|------|
| API密钥错误 | 检查.env配置 | [QUICKSTART_ALIYUN.md](QUICKSTART_ALIYUN.md) |
| 配置验证失败 | 运行test_aliyun.py | [docs/aliyun_setup.md](docs/aliyun_setup.md) |

### 音频问题

| 问题 | 解决方案 | 文档 |
|------|---------|------|
| 无法捕获音频 | 启用立体声混音 | [README.md](README.md) |
| 设备未找到 | 检查设备索引 | [setup_guide.md](setup_guide.md) |

### 打包问题

| 问题 | 解决方案 | 文档 |
|------|---------|------|
| 打包失败 | 检查依赖 | [BUILD_GUIDE.md](BUILD_GUIDE.md) |
| 文件太大 | 使用虚拟环境 | [PACKAGE_QUICKSTART.md](PACKAGE_QUICKSTART.md) |
| 杀毒报毒 | 添加白名单 | [BUILD_GUIDE.md](BUILD_GUIDE.md) |

## 📦 文件清单

### 核心程序文件
- `main.py` - 主程序
- `config.py` - 配置管理
- `audio_capture.py` - 音频捕获
- `transcription_service.py` - AI转录
- `subtitle_window.py` - UI界面

### 配置文件
- `.env.example` - 通用配置模板
- `.env.aliyun.example` - 阿里云配置模板
- `requirements.txt` - 运行依赖
- `build_requirements.txt` - 打包依赖

### 打包文件
- `ai_subtitle.spec` - PyInstaller配置
- `build.bat` - 打包脚本
- `build_portable.bat` - 便携版脚本
- `create_icon.py` - 图标生成

### 测试文件
- `test_aliyun.py` - 阿里云测试
- `run.bat` - 快速启动

### 文档文件
- `README.md` - 主文档
- `setup_guide.md` - 安装指南
- `BUILD_GUIDE.md` - 打包指南
- `PACKAGE_QUICKSTART.md` - 打包快速指南
- `QUICKSTART_ALIYUN.md` - 阿里云快速指南
- `PROJECT_STRUCTURE.md` - 项目结构
- `CHANGELOG_ALIYUN.md` - 阿里云更新日志
- `UPDATE_SUMMARY.md` - 更新总结
- `PACKAGE_UPDATE.md` - 打包更新说明
- `COMPLETE_GUIDE.md` - 本文件

## 🎓 学习路径

### 初学者路径

1. **了解项目** → [README.md](README.md)
2. **快速配置** → [QUICKSTART_ALIYUN.md](QUICKSTART_ALIYUN.md)
3. **使用应用** → 下载便携版
4. **遇到问题** → [setup_guide.md](setup_guide.md) 故障排除

### 开发者路径

1. **项目结构** → [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. **环境配置** → [setup_guide.md](setup_guide.md)
3. **运行调试** → [README.md](README.md)
4. **阿里云集成** → [docs/aliyun_setup.md](docs/aliyun_setup.md)

### 打包分发路径

1. **快速打包** → [PACKAGE_QUICKSTART.md](PACKAGE_QUICKSTART.md)
2. **详细配置** → [BUILD_GUIDE.md](BUILD_GUIDE.md)
3. **创建便携版** → `build_portable.bat`
4. **分发给用户** → ZIP文件

## 🆘 获取帮助

### 文档资源
- 查看对应场景的推荐文档
- 使用文档内的搜索功能
- 查看故障排除章节

### 在线资源
- **PyInstaller**: https://pyinstaller.org/
- **PyQt5**: https://www.riverbankcomputing.com/software/pyqt/
- **阿里云百炼**: https://dashscope.aliyun.com/

### 社区支持
- 提交GitHub Issue
- 查看已有问题和解决方案
- 参与讨论和改进

## 📝 最佳实践

### 开发最佳实践
1. 使用虚拟环境
2. 定期更新依赖
3. 遵循代码规范
4. 编写测试代码
5. 记录变更日志

### 打包最佳实践
1. 在干净环境中打包
2. 测试打包结果
3. 提供完整文档
4. 版本号管理
5. 保留构建日志

### 分发最佳实践
1. 提供配置向导
2. 包含使用说明
3. 测试用户体验
4. 收集用户反馈
5. 及时更新版本

## 🎉 总结

本项目提供了完整的文档体系，涵盖：

- ✅ **快速开始** - 5分钟上手
- ✅ **详细配置** - 深入了解
- ✅ **打包分发** - 一键完成
- ✅ **故障排除** - 快速解决
- ✅ **最佳实践** - 专业指导

**选择适合你的文档，开始使用吧！**

---

**维护**: AI Subtitle Tool Team  
**版本**: v1.2.0  
**更新**: 2024-11
