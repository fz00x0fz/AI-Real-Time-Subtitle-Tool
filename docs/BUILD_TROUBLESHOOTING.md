# 打包故障排除指南

## 🔧 常见打包问题

### 问题1: 找不到 tensorboard 模块

**错误信息**:
```
ModuleNotFoundError: No module named 'tensorboard'
或
ImportError: cannot import name 'tensorboard'
```

**原因**: 
PyInstaller尝试包含不需要的tensorboard模块（通常是某些依赖库间接引用）

**解决方案**: ✅ 已修复

在 `ai_subtitle.spec` 的 `excludes` 列表中添加了 `tensorboard`：

```python
excludes=[
    'tensorboard',
    'tensorflow',
    'torch',
    ...
]
```

**操作步骤**:
1. 确保使用最新的 `ai_subtitle.spec` 文件
2. 重新运行打包: `build.bat`

---

### 问题2: 打包体积过大

**现象**: 
生成的exe文件超过500MB

**原因**: 
包含了不必要的大型库（如TensorFlow、PyTorch等）

**解决方案**:

已在 `ai_subtitle.spec` 中排除大型库：
```python
excludes=[
    'tensorflow',
    'torch',
    'torchvision',
    'matplotlib',
    'scipy',
    'pandas',
]
```

**预期大小**:
- 基础版本: ~50-100MB
- 包含OpenAI: ~100-150MB
- 包含Azure: ~150-200MB

---

### 问题3: PyInstaller 未安装

**错误信息**:
```
'pyinstaller' 不是内部或外部命令
```

**解决方案**:
```bash
# 安装PyInstaller
pip install pyinstaller

# 或使用build_requirements.txt
pip install -r build_requirements.txt
```

---

### 问题4: 缺少隐藏导入

**错误信息**:
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**:

在 `ai_subtitle.spec` 的 `hiddenimports` 中添加缺失的模块：

```python
hiddenimports=[
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'sounddevice',
    'numpy',
    'requests',
    'dotenv',
    'openai',
    'azure.cognitiveservices.speech',
    # 添加缺失的模块
    'your_missing_module',
],
```

---

### 问题5: UPX 压缩失败

**错误信息**:
```
UPX is not available
```

**解决方案**:

**方法1**: 禁用UPX压缩

编辑 `ai_subtitle.spec`:
```python
exe = EXE(
    ...
    upx=False,  # 改为False
    ...
)

coll = COLLECT(
    ...
    upx=False,  # 改为False
    ...
)
```

**方法2**: 安装UPX
1. 下载: https://github.com/upx/upx/releases
2. 解压到系统PATH路径
3. 重新打包

---

### 问题6: 图标文件缺失

**警告信息**:
```
WARNING: icon.ico not found
```

**解决方案**:

**方法1**: 创建图标
```bash
python create_icon.py
```

**方法2**: 使用默认图标
编辑 `ai_subtitle.spec`:
```python
icon=None,  # 不使用自定义图标
```

---

### 问题7: 打包后运行报错

**错误信息**:
```
Failed to execute script main
```

**排查步骤**:

1. **使用控制台模式查看详细错误**
   
   编辑 `ai_subtitle.spec`:
   ```python
   console=True,  # 确保为True
   ```

2. **检查依赖文件**
   
   确保 `.env.example` 等文件已复制：
   ```python
   datas=[
       ('.env.example', '.'),
       ('.env.aliyun.example', '.'),
       ...
   ],
   ```

3. **测试单独运行**
   ```bash
   cd dist\AI实时字幕
   AI实时字幕.exe
   ```
   查看控制台输出的错误信息

---

### 问题8: 内存不足

**错误信息**:
```
MemoryError
或
Out of memory
```

**解决方案**:

1. **关闭其他程序**
2. **增加虚拟内存**
3. **分步打包**

   ```bash
   # 先清理
   rmdir /s /q build dist
   
   # 再打包
   pyinstaller ai_subtitle.spec
   ```

---

### 问题9: 权限问题

**错误信息**:
```
Permission denied
或
Access is denied
```

**解决方案**:

1. **以管理员身份运行**
   - 右键 `build.bat`
   - 选择"以管理员身份运行"

2. **关闭杀毒软件**
   - 临时禁用实时保护
   - 将项目文件夹添加到白名单

3. **清理锁定文件**
   ```bash
   # 关闭所有相关程序
   taskkill /f /im AI实时字幕.exe
   
   # 清理文件
   rmdir /s /q build dist
   ```

---

### 问题10: 路径包含中文或空格

**错误信息**:
```
UnicodeDecodeError
或
Path not found
```

**解决方案**:

1. **移动项目到纯英文路径**
   ```
   ❌ C:\用户\项目\ai_subtitle_tool
   ✅ C:\projects\ai_subtitle_tool
   ```

2. **避免路径中的空格**
   ```
   ❌ C:\My Projects\ai_subtitle_tool
   ✅ C:\projects\ai_subtitle_tool
   ```

---

## 🛠️ 高级故障排除

### 完全清理重新打包

```bash
# 1. 清理所有构建文件
rmdir /s /q build
rmdir /s /q dist
del /f /q *.spec.bak

# 2. 清理Python缓存
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc

# 3. 重新安装打包依赖
pip install -r build_requirements.txt --upgrade

# 4. 重新打包
build.bat
```

### 调试模式打包

编辑 `ai_subtitle.spec`:
```python
exe = EXE(
    ...
    debug=True,  # 启用调试
    console=True,  # 显示控制台
    ...
)
```

### 生成详细日志

```bash
pyinstaller --log-level=DEBUG ai_subtitle.spec > build_log.txt 2>&1
```

查看 `build_log.txt` 了解详细信息

---

## 📋 打包前检查清单

### 环境检查
- [ ] Python 3.8-3.11 已安装
- [ ] pip 已更新到最新版本
- [ ] 所有依赖已安装: `pip install -r requirements.txt`
- [ ] 打包工具已安装: `pip install -r build_requirements.txt`

### 文件检查
- [ ] `main.py` 存在
- [ ] `ai_subtitle.spec` 存在
- [ ] `.env.example` 存在
- [ ] `README.md` 存在

### 配置检查
- [ ] `ai_subtitle.spec` 中的 `excludes` 包含 `tensorboard`
- [ ] `hiddenimports` 包含所有必需模块
- [ ] `datas` 包含所有配置文件

### 系统检查
- [ ] 磁盘空间充足（至少2GB）
- [ ] 内存充足（至少4GB可用）
- [ ] 杀毒软件已添加白名单
- [ ] 项目路径为纯英文

---

## 🔍 验证打包结果

### 检查文件结构

```
dist/
└── AI实时字幕/
    ├── AI实时字幕.exe          ✅ 主程序
    ├── .env.example            ✅ 配置示例
    ├── .env.aliyun.example     ✅ 阿里云配置
    ├── README.md               ✅ 说明文档
    ├── QUICKSTART_ALIYUN.md    ✅ 快速开始
    ├── docs/                   ✅ 文档目录
    └── _internal/              ✅ 依赖文件
```

### 测试运行

```bash
cd dist\AI实时字幕
AI实时字幕.exe
```

**预期结果**:
- ✅ 程序正常启动
- ✅ 显示字幕窗口
- ✅ 配置按钮可用
- ✅ 无错误提示

---

## 📞 获取帮助

### 查看文档
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - 完整打包指南
- **[HOW_TO_BUILD.md](HOW_TO_BUILD.md)** - 快速打包教程
- **[PACKAGE_QUICKSTART.md](PACKAGE_QUICKSTART.md)** - 打包快速开始

### 常用命令

```bash
# 查看PyInstaller版本
pyinstaller --version

# 查看Python版本
python --version

# 查看已安装包
pip list

# 测试导入
python -c "import PyQt5; import sounddevice; print('OK')"
```

### 收集诊断信息

如果问题仍未解决，收集以下信息：

```bash
# 1. 系统信息
systeminfo > system_info.txt

# 2. Python环境
python --version > python_info.txt
pip list >> python_info.txt

# 3. 打包日志
pyinstaller --log-level=DEBUG ai_subtitle.spec > build_log.txt 2>&1

# 4. 错误截图
# 截取错误信息的屏幕截图
```

---

## ✅ 成功标志

打包成功的标志：

1. **构建完成**
   ```
   Building EXE from EXE-00.toc completed successfully.
   ```

2. **文件生成**
   - `dist\AI实时字幕\AI实时字幕.exe` 存在
   - 文件大小合理（50-200MB）

3. **运行正常**
   - 双击exe可以启动
   - 界面正常显示
   - 功能可以使用

4. **无错误提示**
   - 无DLL缺失
   - 无模块缺失
   - 无权限错误

---

**打包问题已解决！** 🎉

如果仍有问题，请运行 `build.bat` 并查看详细输出。
