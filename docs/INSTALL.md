# 安装指南

## 快速安装

### 方法1: 安装所有依赖（推荐）

```bash
pip install -r requirements.txt
```

### 方法2: 仅安装核心依赖

如果完整安装遇到问题，可以先安装核心依赖：

```bash
pip install -r requirements-minimal.txt
```

然后根据需要安装AI服务依赖：

```bash
# OpenAI Whisper
pip install openai

# Azure Speech
pip install azure-cognitiveservices-speech
```

## 分步安装

### 1. 核心依赖（必需）

```bash
# UI框架
pip install PyQt5

# 音频捕获
pip install sounddevice

# 数值计算
pip install numpy

# 配置管理
pip install python-dotenv

# HTTP请求
pip install requests
```

### 2. AI服务依赖（按需）

#### 使用OpenAI Whisper
```bash
pip install openai
```

#### 使用Azure Speech
```bash
pip install azure-cognitiveservices-speech
```

#### 使用阿里云百炼
无需额外依赖，使用requests即可

#### 使用本地Whisper
```bash
pip install openai-whisper
```

## 常见问题

### Q1: PyQt5安装失败

**错误信息**:
```
ERROR: Could not find a version that satisfies the requirement PyQt5
```

**解决方法**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 重试安装
pip install PyQt5
```

### Q2: PyAudio安装失败（可忽略）

**说明**: 项目使用sounddevice，不需要PyAudio

如果确实需要PyAudio：

**方法1: 使用pipwin**
```bash
pip install pipwin
pipwin install pyaudio
```

**方法2: 下载预编译wheel**
1. 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. 下载对应Python版本的wheel文件
3. 安装: `pip install PyAudio-0.2.14-cpXX-cpXX-win_amd64.whl`

### Q3: numpy安装失败

**解决方法**:
```bash
# 安装特定版本
pip install numpy==1.24.3

# 或使用conda
conda install numpy
```

### Q4: sounddevice安装失败

**解决方法**:
```bash
# 确保已安装PortAudio
# Windows通常会自动处理

# 重试安装
pip install sounddevice --upgrade
```

### Q5: 网络问题导致安装慢

**使用国内镜像**:
```bash
# 清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 阿里镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 中科大镜像
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
```

## 验证安装

### 检查已安装的包

```bash
pip list | findstr "PyQt5 sounddevice numpy dotenv requests"
```

### 测试导入

```python
# 创建test_imports.py
import PyQt5
import sounddevice
import numpy
import dotenv
import requests

print("✅ 所有核心依赖已正确安装！")
```

运行测试：
```bash
python test_imports.py
```

## 推荐的安装顺序

1. **升级pip**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **安装核心依赖**
   ```bash
   pip install -r requirements-minimal.txt
   ```

3. **测试运行**
   ```bash
   python main.py
   ```

4. **安装AI服务依赖**
   ```bash
   pip install openai azure-cognitiveservices-speech
   ```

## 虚拟环境（推荐）

### 创建虚拟环境

```bash
# 创建
python -m venv venv

# 激活 (Windows)
venv\Scripts\activate

# 激活 (Linux/Mac)
source venv/bin/activate
```

### 在虚拟环境中安装

```bash
pip install -r requirements.txt
```

### 退出虚拟环境

```bash
deactivate
```

## 依赖说明

### 必需依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| PyQt5 | >=5.15.0 | UI框架 |
| sounddevice | >=0.4.6 | 音频捕获 |
| numpy | >=1.24.0 | 音频处理 |
| python-dotenv | >=1.0.0 | 配置管理 |
| requests | >=2.31.0 | HTTP请求 |

### 可选依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| openai | >=1.0.0 | OpenAI API |
| azure-cognitiveservices-speech | >=1.34.0 | Azure Speech |
| pydub | >=0.25.1 | 音频处理辅助 |
| openai-whisper | latest | 本地Whisper |

## 系统要求

- **操作系统**: Windows 10/11
- **Python**: 3.8 - 3.11
- **内存**: 至少2GB
- **磁盘**: 至少500MB

## 获取帮助

如果安装遇到问题：

1. 查看本文档的常见问题部分
2. 查看 [README.md](README.md)
3. 提交Issue到GitHub

---

**提示**: 建议使用虚拟环境来避免依赖冲突！
