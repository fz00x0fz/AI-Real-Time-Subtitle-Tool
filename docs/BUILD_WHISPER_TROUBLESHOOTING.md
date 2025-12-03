# Whisper本地模型版打包故障排除

## 🐛 常见错误：打包失败

### 错误信息
```
[错误] 打包失败！

常见问题:
1. 内存不足 - 关闭其他程序
2. 磁盘空间不足 - 至少需要5GB空闲空间
3. 依赖缺失 - 运行: pip install openai-whisper torch
```

---

## 🔍 问题诊断

### 1. 检查依赖是否安装

运行以下命令检查：

```bash
# 检查whisper
python -c "import whisper; print('Whisper已安装')"

# 检查torch
python -c "import torch; print('PyTorch已安装')"

# 检查PyInstaller
python -c "import PyInstaller; print('PyInstaller已安装')"
```

### 2. 查看详细错误

如果上述命令报错，说明依赖未安装。

---

## ✅ 解决方案

### 方案1: 使用修复脚本（推荐）

我们提供了一键修复脚本：

```bash
# 运行修复脚本
fix_whisper_build.bat
```

脚本会自动：
1. ✅ 检查Python环境
2. ✅ 安装PyTorch (CPU版本)
3. ✅ 安装openai-whisper
4. ✅ 验证安装

### 方案2: 手动安装依赖

#### 步骤1: 安装PyTorch

```bash
# CPU版本（推荐，体积小）
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 或GPU版本（如果有NVIDIA显卡）
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**注意**：
- CPU版本约200MB
- GPU版本约2GB
- 打包时推荐使用CPU版本

#### 步骤2: 安装openai-whisper

```bash
pip install openai-whisper
```

#### 步骤3: 安装打包工具

```bash
pip install -r build_requirements.txt
```

#### 步骤4: 验证安装

```bash
python -c "import whisper; print('Whisper:', whisper.__version__)"
python -c "import torch; print('PyTorch:', torch.__version__)"
```

### 方案3: 使用requirements文件

创建 `requirements-whisper.txt`:

```txt
openai-whisper
torch
torchaudio
tiktoken
numba
```

然后安装：

```bash
pip install -r requirements-whisper.txt
```

---

## 🔧 其他常见问题

### 问题1: 内存不足

**症状**: 打包过程中卡住或崩溃

**解决方案**:
1. 关闭其他程序
2. 增加虚拟内存
3. 使用64位Python
4. 至少需要8GB RAM

### 问题2: 磁盘空间不足

**症状**: 打包失败，提示磁盘空间不足

**解决方案**:
1. 清理磁盘空间
2. 至少需要5GB可用空间
3. 检查临时文件夹

### 问题3: PyTorch安装失败

**症状**: `pip install torch` 失败

**解决方案**:

```bash
# 方法1: 使用清华镜像
pip install torch torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方法2: 使用阿里云镜像
pip install torch torchaudio -i https://mirrors.aliyun.com/pypi/simple/

# 方法3: 从官网下载whl文件手动安装
# 访问: https://download.pytorch.org/whl/torch_stable.html
```

### 问题4: openai-whisper安装失败

**症状**: `pip install openai-whisper` 失败

**解决方案**:

```bash
# 方法1: 升级pip
python -m pip install --upgrade pip

# 方法2: 使用国内镜像
pip install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方法3: 分步安装依赖
pip install numpy
pip install torch
pip install tiktoken
pip install openai-whisper
```

### 问题5: 打包时间过长

**症状**: 打包超过30分钟

**原因**: 
- PyTorch体积大（约2GB）
- 需要分析大量依赖

**解决方案**:
- 正常现象，耐心等待
- 可以使用 `--log-level DEBUG` 查看进度

### 问题6: 打包后体积过大

**症状**: 打包后超过3GB

**解决方案**:

1. **使用CPU版PyTorch**:
```bash
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

2. **排除不需要的库**:
编辑 `ai_subtitle_with_whisper.spec`，在 `excludes` 中添加：
```python
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
    'PIL',
    'tkinter',
    'tensorboard',
    'tensorflow',
    'IPython',
    'jupyter',
]
```

3. **使用UPX压缩**:
```bash
# 安装UPX
# 下载: https://github.com/upx/upx/releases

# 在spec文件中启用
upx=True
```

---

## 📋 完整安装清单

### 必需依赖

```bash
# 核心依赖
pip install PyQt5
pip install sounddevice
pip install numpy
pip install requests
pip install python-dotenv

# Whisper依赖
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper

# 打包工具
pip install pyinstaller
```

### 可选依赖

```bash
# Azure支持
pip install azure-cognitiveservices-speech

# OpenAI支持
pip install openai
```

---

## 🚀 推荐打包流程

### 1. 准备环境

```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 升级pip
python -m pip install --upgrade pip
```

### 2. 安装依赖

```bash
# 运行修复脚本
fix_whisper_build.bat

# 或手动安装
pip install -r requirements.txt
pip install -r build_requirements.txt
pip install openai-whisper
```

### 3. 验证环境

```bash
# 测试应用
python main.py

# 测试Whisper
python -c "import whisper; model = whisper.load_model('base'); print('OK')"
```

### 4. 执行打包

```bash
# 清理旧文件
rmdir /s /q build dist

# 开始打包
build_with_whisper.bat
```

### 5. 测试打包结果

```bash
cd dist\AI实时字幕_本地模型版
AI实时字幕_本地模型版.exe
```

---

## 💡 优化建议

### 1. 减小打包体积

**使用标准版 + 运行时安装**（推荐）:
- 标准版: 50-200MB
- 用户按需安装本地模型
- 参考: [运行时安装指南](RUNTIME_INSTALL_GUIDE.md)

### 2. 提高打包速度

- 使用SSD硬盘
- 关闭杀毒软件
- 使用虚拟环境

### 3. 提高打包成功率

- 使用Python 3.8-3.10（推荐3.9）
- 使用64位Python
- 确保至少8GB RAM
- 确保至少5GB磁盘空间

---

## 📊 系统要求对比

### 开发环境

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| Python | 3.8+ | 3.9 |
| RAM | 4GB | 8GB+ |
| 磁盘 | 3GB | 10GB+ |
| CPU | 双核 | 四核+ |

### 打包环境

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| RAM | 8GB | 16GB+ |
| 磁盘 | 5GB | 20GB+ |
| 时间 | 10分钟 | 30分钟 |

---

## 🔗 相关资源

### 官方文档
- [PyTorch安装指南](https://pytorch.org/get-started/locally/)
- [OpenAI Whisper GitHub](https://github.com/openai/whisper)
- [PyInstaller文档](https://pyinstaller.org/)

### 项目文档
- [打包指南](BUILD_GUIDE.md)
- [打包选项](BUILD_OPTIONS.md)
- [运行时安装](RUNTIME_INSTALL_GUIDE.md)

---

## 📞 获取帮助

如果以上方案都无法解决问题：

1. **查看详细日志**:
   - 运行 `build_with_whisper.bat`
   - 保存完整输出
   - 查找具体错误信息

2. **提交Issue**:
   - 访问: https://github.com/fz00x0fz/AI-Real-Time-Subtitle-Tool/issues
   - 提供系统信息、Python版本、完整错误日志

3. **使用标准版**:
   - 如果本地模型版打包困难
   - 推荐使用标准版 + 运行时安装
   - 参考: [运行时安装指南](RUNTIME_INSTALL_GUIDE.md)

---

**最后更新**: 2024-11-15  
**适用版本**: v1.0.0+
