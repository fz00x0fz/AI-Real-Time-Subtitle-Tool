# 打包快速指南

> 3步完成Windows应用打包

## 🚀 快速打包

### 第一步：安装打包工具

```bash
pip install -r build_requirements.txt
```

### 第二步：运行打包脚本

```bash
build.bat
```

### 第三步：测试和分发

```bash
# 测试
cd dist\AI实时字幕
AI实时字幕.exe

# 分发（可选）
build_portable.bat
```

## 📦 输出说明

### 标准版

**位置**: `dist\AI实时字幕\`

**内容**:
- `AI实时字幕.exe` - 主程序
- `_internal\` - 依赖库
- 配置文件和文档

**大小**: ~300-400 MB

### 便携版

**位置**: `AI实时字幕_便携版\`

**额外包含**:
- `配置向导.bat` - 快速配置工具
- `README_便携版.txt` - 使用说明

**可选**: ZIP压缩包

## 🎯 使用场景

### 场景1: 个人使用

```bash
# 直接打包
build.bat

# 运行
dist\AI实时字幕\AI实时字幕.exe
```

### 场景2: 分发给他人

```bash
# 创建便携版
build.bat
build_portable.bat

# 分发ZIP文件
AI实时字幕_便携版.zip
```

### 场景3: 企业部署

```bash
# 打包
build.bat

# 使用Inno Setup创建安装程序
# 或部署到网络共享目录
```

## ⚙️ 自定义配置

### 修改应用图标

```bash
# 方法1: 自动生成
python create_icon.py

# 方法2: 使用自定义图标
# 将icon.ico放在项目根目录
```

### 修改打包配置

编辑 `ai_subtitle.spec`:

```python
# 添加更多数据文件
datas=[
    ('my_file.txt', '.'),
]

# 排除不需要的模块
excludes=[
    'module_name',
]
```

### 优化文件大小

```python
# 在ai_subtitle.spec中
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
    'openai',  # 如果不用OpenAI
]
```

## 🔍 常见问题

### Q: 打包失败怎么办？

**A**: 
```bash
# 1. 检查依赖
pip list

# 2. 重新安装
pip install -r requirements.txt
pip install -r build_requirements.txt

# 3. 清理后重试
rmdir /s /q build dist
build.bat
```

### Q: 程序无法启动？

**A**:
- 检查是否缺少 Visual C++ Redistributable
- 查看控制台错误信息（console=True）
- 在干净的Windows系统上测试

### Q: 文件太大？

**A**:
```bash
# 使用虚拟环境
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
build.bat
```

### Q: 杀毒软件报毒？

**A**:
- 添加到白名单
- 使用代码签名（需要证书）
- 向杀毒厂商报告误报

## 📤 分发方式

### ZIP压缩包

```bash
# 自动创建
build_portable.bat
# 选择 Y 创建ZIP

# 手动创建
powershell -command "Compress-Archive -Path 'dist\AI实时字幕' -DestinationPath 'AI实时字幕.zip'"
```

### 网盘分发

1. 上传ZIP到网盘
2. 分享下载链接
3. 提供使用说明

### GitHub Release

1. 创建Release
2. 上传ZIP文件
3. 编写Release Notes

## 🧪 测试清单

打包后必须测试：

- [ ] 程序启动正常
- [ ] UI显示正常
- [ ] 音频捕获工作
- [ ] AI转录功能正常
- [ ] 配置文件读取正常
- [ ] 在其他电脑上测试

## 💡 最佳实践

1. **使用虚拟环境打包** - 避免不必要的依赖
2. **测试打包结果** - 在干净系统上测试
3. **提供完整文档** - 包含配置和使用说明
4. **版本管理** - 记录每个版本的变更
5. **定期更新** - 保持依赖库最新

## 📚 详细文档

- **完整打包指南**: [BUILD_GUIDE.md](BUILD_GUIDE.md)
- **项目文档**: [README.md](README.md)
- **配置指南**: [setup_guide.md](setup_guide.md)

## 🆘 获取帮助

- **PyInstaller文档**: https://pyinstaller.org/
- **项目Issues**: 提交问题和建议

---

**快速开始**: 运行 `build.bat` 即可！
