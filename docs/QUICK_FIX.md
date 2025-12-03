# 快速修复：Whisper打包失败

## ❌ 错误

```
[错误] 打包失败！
常见问题:
1. 内存不足 - 关闭其他程序
2. 磁盘空间不足 - 至少需要5GB空闲空间
3. 依赖缺失 - 运行: pip install openai-whisper torch
```

---

## ✅ 一键修复（推荐）

### 运行修复脚本

```bash
fix_whisper_build.bat
```

脚本会自动安装所有必需依赖。

---

## 🔧 手动修复

### 步骤1: 安装PyTorch

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 步骤2: 安装Whisper

```bash
pip install openai-whisper
```

### 步骤3: 验证安装

```bash
python -c "import whisper; print('OK')"
python -c "import torch; print('OK')"
```

### 步骤4: 重新打包

```bash
build_with_whisper.bat
```

---

## 💡 推荐方案

如果打包本地模型版遇到困难，推荐使用：

### **标准版 + 运行时安装**

**优势**:
- ✅ 打包体积小（50-200MB）
- ✅ 打包速度快（3-5分钟）
- ✅ 用户按需安装本地模型
- ✅ 不需要安装PyTorch

**使用方法**:
1. 运行 `build.bat` 打包标准版
2. 用户在应用中点击"安装本地模型"
3. 自动下载安装

详见: [运行时安装指南](docs/RUNTIME_INSTALL_GUIDE.md)

---

## 📋 系统要求

### 打包本地模型版

- **RAM**: 至少8GB
- **磁盘**: 至少5GB可用空间
- **时间**: 10-30分钟

### 打包标准版

- **RAM**: 至少4GB
- **磁盘**: 至少2GB可用空间
- **时间**: 3-5分钟

---

## 🔗 详细文档

- [完整故障排除](BUILD_WHISPER_TROUBLESHOOTING.md)
- [打包选项对比](docs/BUILD_OPTIONS.md)
- [运行时安装](docs/RUNTIME_INSTALL_GUIDE.md)

---

**需要帮助？** 查看 [BUILD_WHISPER_TROUBLESHOOTING.md](BUILD_WHISPER_TROUBLESHOOTING.md)
