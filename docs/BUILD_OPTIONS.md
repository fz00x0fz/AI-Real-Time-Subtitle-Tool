# 打包选项说明

## 📦 两种打包方式

本项目提供两种打包方式，适用于不同的使用场景。

---

## 🌐 标准版（在线API版）

### 特点

✅ **体积小** - 约50-200MB  
✅ **打包快** - 5-10分钟  
✅ **依赖少** - 无需大型模型库  
✅ **推荐使用** - 适合大多数用户  

### 支持的AI服务

- ✅ 阿里云百炼 (推荐)
- ✅ OpenAI Whisper API
- ✅ Azure Speech Service
- ❌ 本地Whisper模型 (不支持)

### 打包命令

```bash
build.bat
```

### 使用场景

- 有稳定网络连接
- 使用云端AI服务
- 对体积有要求
- 快速部署

### 配置文件

使用 `ai_subtitle.spec`

---

## 💻 本地模型版（离线版）

### 特点

✅ **离线使用** - 无需联网  
✅ **隐私保护** - 数据不上传  
✅ **完整功能** - 支持所有AI服务  
⚠️ **体积大** - 约1-2GB  
⚠️ **打包慢** - 10-30分钟  

### 支持的AI服务

- ✅ 阿里云百炼
- ✅ OpenAI Whisper API
- ✅ Azure Speech Service
- ✅ 本地Whisper模型 (支持)

### 打包命令

```bash
build_with_whisper.bat
```

### 使用场景

- 需要离线使用
- 对隐私有要求
- 网络不稳定
- 需要本地模型

### 配置文件

使用 `ai_subtitle_with_whisper.spec`

---

## 📊 对比表格

| 特性 | 标准版 | 本地模型版 |
|------|--------|-----------|
| **打包体积** | 50-200MB | 1-2GB |
| **打包时间** | 5-10分钟 | 10-30分钟 |
| **运行内存** | 200-500MB | 500MB-2GB |
| **网络要求** | 需要联网 | 首次需要下载模型 |
| **阿里云百炼** | ✅ | ✅ |
| **OpenAI API** | ✅ | ✅ |
| **Azure Speech** | ✅ | ✅ |
| **本地Whisper** | ❌ | ✅ |
| **离线使用** | ❌ | ✅ |
| **推荐用户** | 大多数用户 | 高级用户/离线场景 |

---

## 🎯 选择建议

### 选择标准版，如果你：

- ✅ 有稳定的网络连接
- ✅ 使用阿里云/OpenAI/Azure服务
- ✅ 对安装包体积有要求
- ✅ 想要快速部署

### 选择本地模型版，如果你：

- ✅ 需要离线使用
- ✅ 对数据隐私有要求
- ✅ 网络环境不稳定
- ✅ 想要使用本地Whisper模型
- ✅ 不在意安装包体积

---

## 🚀 快速开始

### 打包标准版

```bash
# 1. 运行打包脚本
build.bat

# 2. 等待5-10分钟

# 3. 输出目录
dist\AI实时字幕\
```

### 打包本地模型版

```bash
# 1. 安装额外依赖
pip install openai-whisper

# 2. 运行打包脚本
build_with_whisper.bat

# 3. 等待10-30分钟

# 4. 输出目录
dist\AI实时字幕_本地模型版\
```

---

## 📝 详细说明

### 标准版打包流程

1. **检查环境**
   - Python 3.8-3.11
   - pip 最新版本

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install -r build_requirements.txt
   ```

3. **运行打包**
   ```bash
   build.bat
   ```

4. **输出文件**
   ```
   dist/AI实时字幕/
   ├── AI实时字幕.exe
   ├── .env.example
   ├── README.md
   └── ...
   ```

### 本地模型版打包流程

1. **检查环境**
   - Python 3.8-3.11
   - pip 最新版本
   - 至少5GB磁盘空间

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   pip install openai-whisper
   pip install -r build_requirements.txt
   ```

3. **运行打包**
   ```bash
   build_with_whisper.bat
   ```

4. **输出文件**
   ```
   dist/AI实时字幕_本地模型版/
   ├── AI实时字幕_本地模型版.exe
   ├── .env.example
   ├── README.md
   ├── 使用说明_本地模型版.txt
   └── ...
   ```

---

## 🔧 本地模型版特别说明

### 首次运行

本地模型版首次运行时会自动下载Whisper模型：

```
首次启动 → 下载模型 (约140MB) → 开始使用
```

### 模型存储位置

```
Windows: %USERPROFILE%\.cache\whisper
```

### 支持的模型

| 模型 | 大小 | 速度 | 准确度 | 推荐 |
|------|------|------|--------|------|
| tiny | 39MB | 最快 | 低 | 测试 |
| base | 74MB | 快 | 中 | ⭐推荐 |
| small | 244MB | 中 | 高 | 平衡 |
| medium | 769MB | 慢 | 很高 | 高质量 |
| large | 1550MB | 最慢 | 最高 | 专业 |

### 切换模型

编辑 `transcription_service.py`:
```python
self.model = whisper.load_model("base")  # 改为其他模型
```

---

## ⚠️ 注意事项

### 标准版

1. **需要API Key**
   - 阿里云/OpenAI/Azure的API密钥
   - 在.env文件中配置

2. **网络连接**
   - 需要稳定的网络
   - API调用需要联网

3. **使用成本**
   - 云端API可能产生费用
   - 查看各服务商定价

### 本地模型版

1. **首次下载**
   - 首次运行需要联网
   - 下载Whisper模型（约140MB）
   - 下载完成后可离线使用

2. **系统要求**
   - 至少4GB内存
   - 推荐8GB内存
   - 至少2GB磁盘空间

3. **性能要求**
   - CPU: 推荐i5或以上
   - GPU: 可选，支持CUDA加速
   - 识别速度取决于CPU性能

---

## 🛠️ 故障排除

### 标准版打包失败

**问题**: 找不到tensorboard模块

**解决**: 
```bash
# 已在 ai_subtitle.spec 中排除
# 重新运行即可
build.bat
```

详见: [BUILD_TROUBLESHOOTING.md](BUILD_TROUBLESHOOTING.md)

### 本地模型版打包失败

**问题1**: 内存不足

**解决**:
- 关闭其他程序
- 增加虚拟内存
- 使用更大内存的机器

**问题2**: openai-whisper安装失败

**解决**:
```bash
# 手动安装
pip install openai-whisper

# 或使用conda
conda install -c conda-forge openai-whisper
```

**问题3**: torch安装失败

**解决**:
```bash
# 安装CPU版本的torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## 📚 相关文档

- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - 完整打包指南
- **[BUILD_TROUBLESHOOTING.md](BUILD_TROUBLESHOOTING.md)** - 故障排除
- **[HOW_TO_BUILD.md](HOW_TO_BUILD.md)** - 快速打包教程
- **[README.md](README.md)** - 项目说明

---

## ✅ 推荐流程

### 对于普通用户

```bash
# 1. 先尝试标准版
build.bat

# 2. 测试是否满足需求

# 3. 如需本地模型，再打包本地模型版
build_with_whisper.bat
```

### 对于开发者

```bash
# 1. 开发时使用标准版（快速迭代）
build.bat

# 2. 发布时提供两个版本
build.bat                    # 标准版
build_with_whisper.bat       # 本地模型版
```

---

## 🎉 总结

- **大多数用户**: 使用标准版 (`build.bat`)
- **离线场景**: 使用本地模型版 (`build_with_whisper.bat`)
- **不确定**: 先试标准版，不满足再用本地模型版

**开始打包**: 运行对应的 `.bat` 文件即可！ 🚀
