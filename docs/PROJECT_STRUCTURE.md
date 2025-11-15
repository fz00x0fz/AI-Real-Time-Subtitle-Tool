# 项目结构说明

## 📁 目录结构

```
ai_subtitle_tool/
│
├── 📄 核心程序文件
│   ├── main.py                      # 主程序入口，应用启动
│   ├── config.py                    # 配置管理，环境变量加载
│   ├── audio_capture.py             # 音频捕获模块（Windows WASAPI）
│   ├── transcription_service.py     # AI转录服务（支持4种服务）
│   └── subtitle_window.py           # PyQt5字幕窗口UI
│
├── 📋 配置文件
│   ├── .env.example                 # 通用配置模板
│   ├── .env.aliyun.example          # 阿里云专用配置模板
│   ├── .env                         # 实际配置（需自行创建）
│   └── requirements.txt             # Python依赖列表
│
├── 🚀 启动和测试
│   ├── run.bat                      # Windows一键启动脚本
│   └── test_aliyun.py               # 阿里云配置测试工具
│
├── 📚 文档
│   ├── README.md                    # 项目主文档
│   ├── setup_guide.md               # 详细安装指南
│   ├── QUICKSTART_ALIYUN.md         # 阿里云快速启动指南
│   ├── CHANGELOG_ALIYUN.md          # 阿里云集成更新日志
│   ├── UPDATE_SUMMARY.md            # 更新总结
│   ├── PROJECT_STRUCTURE.md         # 本文件
│   └── docs/
│       └── aliyun_setup.md          # 阿里云详细配置文档
│
└── 🔧 其他
    └── .gitignore                   # Git忽略文件配置
```

## 📄 文件详细说明

### 核心程序文件

#### `main.py`
**功能**: 应用程序主入口
- 初始化所有服务
- 创建UI窗口
- 管理应用生命周期
- 协调音频捕获和转录

**关键类**:
- `AISubtitleApp`: 主应用类
- `TranscriptionWorker`: 转录工作线程

#### `config.py`
**功能**: 配置管理
- 加载环境变量
- 提供配置访问接口
- 配置验证

**配置项**:
- AI服务选择
- OpenAI配置
- Azure配置
- 阿里云配置
- 音频设置
- UI设置

#### `audio_capture.py`
**功能**: 音频捕获
- Windows WASAPI音频捕获
- 音频设备管理
- 音频流处理
- 缓冲区管理

**关键类**:
- `AudioCapture`: 音频捕获主类

**特性**:
- 支持立体声混音
- 实时音频流
- 自动设备检测

#### `transcription_service.py`
**功能**: AI转录服务
- 抽象转录服务接口
- 多种AI服务实现
- 音频格式转换

**支持的服务**:
1. `OpenAITranscriptionService` - OpenAI Whisper API
2. `AzureTranscriptionService` - Azure Speech Service
3. `AliyunTranscriptionService` - 阿里云百炼 🆕
4. `LocalWhisperService` - 本地Whisper模型

**工厂函数**:
- `create_transcription_service()`: 根据配置创建服务

#### `subtitle_window.py`
**功能**: 字幕窗口UI
- PyQt5浮动窗口
- 现代化界面设计
- 拖拽支持
- 透明度控制

**特性**:
- 始终置顶
- 无边框设计
- 实时字幕更新
- 控制按钮（开始/停止）

### 配置文件

#### `.env.example`
**用途**: 通用配置模板
- 包含所有服务的配置示例
- 新用户参考模板

#### `.env.aliyun.example`
**用途**: 阿里云专用配置模板
- 预配置阿里云参数
- 详细的参数说明
- 推荐配置值

#### `requirements.txt`
**用途**: Python依赖管理
```
PyQt5==5.15.10              # UI框架
pyaudio==0.2.14             # 音频I/O
sounddevice==0.4.6          # 跨平台音频
numpy==1.24.3               # 数值计算
openai==1.12.0              # OpenAI API
azure-cognitiveservices-speech==1.34.1  # Azure API
requests==2.31.0            # HTTP请求（阿里云）
python-dotenv==1.0.0        # 环境变量
pydub==0.25.1               # 音频处理
```

### 启动和测试

#### `run.bat`
**功能**: Windows一键启动
- 检查Python环境
- 检查配置文件
- 自动安装依赖
- 启动应用

#### `test_aliyun.py`
**功能**: 阿里云配置测试
- 验证配置正确性
- 测试API连接
- 诊断常见问题
- 提供修复建议

### 文档文件

#### `README.md`
**内容**:
- 项目简介
- 功能特性
- 快速开始
- 配置说明
- 故障排除

#### `setup_guide.md`
**内容**:
- 详细安装步骤
- 环境配置
- API密钥获取
- 常见问题
- 性能优化

#### `QUICKSTART_ALIYUN.md`
**内容**:
- 5分钟快速配置
- 简化步骤
- 快速故障排除

#### `docs/aliyun_setup.md`
**内容**:
- 阿里云详细配置
- 模型选择指南
- 性能优化
- 费用说明
- 高级配置

## 🔄 数据流程

```
┌─────────────────┐
│  系统音频输出    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AudioCapture    │ ← audio_capture.py
│ (WASAPI捕获)    │
└────────┬────────┘
         │ 音频数据流
         ▼
┌─────────────────┐
│ 音频缓冲队列     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│TranscriptionWorker│ ← main.py
│ (工作线程)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│TranscriptionService│ ← transcription_service.py
│ ├─ OpenAI       │
│ ├─ Azure        │
│ ├─ Aliyun 🆕    │
│ └─ Local        │
└────────┬────────┘
         │ 识别文本
         ▼
┌─────────────────┐
│ SubtitleWindow  │ ← subtitle_window.py
│ (显示字幕)       │
└─────────────────┘
```

## 🎯 模块依赖关系

```
main.py
  ├─ config.py
  ├─ audio_capture.py
  │   └─ config.py
  ├─ transcription_service.py
  │   └─ config.py
  └─ subtitle_window.py
      └─ config.py

test_aliyun.py
  ├─ config.py
  └─ transcription_service.py
```

## 🔧 配置层级

```
环境变量 (.env)
    ↓
Config类 (config.py)
    ↓
各模块读取配置
    ├─ AudioCapture
    ├─ TranscriptionService
    └─ SubtitleWindow
```

## 📊 代码统计

| 文件 | 行数 | 功能 |
|------|------|------|
| main.py | ~200 | 主程序逻辑 |
| config.py | ~50 | 配置管理 |
| audio_capture.py | ~150 | 音频捕获 |
| transcription_service.py | ~280 | AI转录 |
| subtitle_window.py | ~200 | UI界面 |
| **总计** | **~880** | **核心代码** |

## 🎨 UI组件结构

```
SubtitleWindow (主窗口)
├─ 控制栏
│  ├─ 标题标签 "🎙️ AI实时字幕"
│  ├─ 状态指示器 "● 待机/录音中"
│  ├─ 开始按钮 "▶ 开始"
│  ├─ 停止按钮 "■ 停止"
│  └─ 关闭按钮 "✕"
└─ 字幕显示区
   └─ 字幕标签 (实时更新)
```

## 🔐 配置安全

```
.env (本地配置)
├─ 包含敏感信息（API密钥）
├─ 不提交到Git (.gitignore)
└─ 从模板创建

.env.example (模板)
├─ 不包含真实密钥
├─ 提交到Git
└─ 供用户参考
```

## 📦 依赖关系图

```
应用程序
├─ PyQt5 (UI框架)
├─ sounddevice (音频捕获)
│   └─ numpy (数值计算)
├─ requests (HTTP请求)
│   └─ 阿里云API调用
├─ openai (OpenAI API)
├─ azure-cognitiveservices-speech (Azure API)
└─ python-dotenv (环境变量)
```

## 🚀 启动流程

```
1. run.bat 或 python main.py
   ↓
2. 加载配置 (config.py)
   ↓
3. 验证配置
   ↓
4. 初始化服务
   ├─ AudioCapture
   ├─ TranscriptionService
   └─ TranscriptionWorker
   ↓
5. 创建UI窗口
   ↓
6. 显示窗口
   ↓
7. 等待用户操作
   ├─ 点击"开始" → 启动捕获和转录
   └─ 点击"停止" → 停止服务
```

## 💡 扩展指南

### 添加新的AI服务

1. 在 `transcription_service.py` 中创建新类：
```python
class NewAIService(TranscriptionService):
    def transcribe(self, audio_data, sample_rate):
        # 实现转录逻辑
        pass
```

2. 在 `config.py` 中添加配置：
```python
NEW_AI_API_KEY = os.getenv('NEW_AI_API_KEY', '')
```

3. 更新工厂函数：
```python
elif service_type == 'new_ai':
    return NewAIService()
```

### 自定义UI主题

修改 `subtitle_window.py` 中的样式表：
```python
self.setStyleSheet("""
    QWidget {
        background-color: #your_color;
    }
""")
```

## 📝 开发建议

### 代码规范
- 使用类型提示
- 添加文档字符串
- 遵循PEP 8

### 错误处理
- 使用try-except捕获异常
- 记录详细错误信息
- 提供用户友好的错误提示

### 测试
- 单元测试各模块
- 集成测试完整流程
- 使用 `test_aliyun.py` 作为参考

---

**维护者**: AI Subtitle Tool Team  
**最后更新**: 2024-11  
**版本**: v1.1.0
