# Windows应用打包指南

## 📦 打包说明

本项目支持将Python应用打包为独立的Windows可执行文件，用户无需安装Python环境即可使用。

**遇到打包问题？** 查看 **[打包故障排除指南](BUILD_TROUBLESHOOTING.md)**

## 🎯 打包方式

### 方式一：标准打包（推荐）

使用 `build.bat` 创建标准发布版本。

```bash
# 运行打包脚本
build.bat
```

**输出**:
- 目录: `dist\AI实时字幕\`
- 主程序: `AI实时字幕.exe`
- 包含所有依赖和配置文件

### 方式二：便携版打包

使用 `build_portable.bat` 创建便携版安装包。

```bash
# 先运行标准打包
build.bat

# 再创建便携版
build_portable.bat
```

**输出**:
- 目录: `AI实时字幕_便携版\`
- 包含配置向导
- 可选ZIP压缩包

## 📋 打包前准备

### 1. 安装打包依赖

```bash
pip install -r build_requirements.txt
```

包含：
- `pyinstaller` - 打包工具
- `pillow` - 图标生成（可选）

### 2. 创建应用图标（可选）

```bash
# 自动生成图标
python create_icon.py

# 或使用自定义图标
# 将icon.ico放在项目根目录
```

### 3. 检查依赖

```bash
pip install -r requirements.txt
```

## 🔧 打包配置

### PyInstaller配置文件

`ai_subtitle.spec` - 主配置文件

**关键配置**:

```python
# 包含的数据文件
datas=[
    ('.env.example', '.'),
    ('.env.aliyun.example', '.'),
    ('README.md', '.'),
    ('docs', 'docs'),
]

# 隐藏导入
hiddenimports=[
    'PyQt5.QtCore',
    'sounddevice',
    'numpy',
    'requests',
    'openai',
    'azure.cognitiveservices.speech',
]

# 排除不需要的模块
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
]
```

## 🚀 打包流程

### 自动打包流程

运行 `build.bat` 会自动执行：

1. ✅ 检查Python环境
2. ✅ 安装打包依赖
3. ✅ 清理旧构建文件
4. ✅ 运行PyInstaller打包
5. ✅ 复制配置文件
6. ✅ 创建使用说明

### 手动打包流程

```bash
# 1. 清理旧文件
rmdir /s /q build dist

# 2. 运行PyInstaller
pyinstaller ai_subtitle.spec --clean

# 3. 复制配置文件
copy .env.example dist\AI实时字幕\
copy README.md dist\AI实时字幕\
```

## 📁 打包输出结构

```
dist\AI实时字幕\
├── AI实时字幕.exe          # 主程序
├── _internal\              # 依赖库和资源
│   ├── PyQt5\
│   ├── numpy\
│   ├── sounddevice\
│   └── ... (其他依赖)
├── .env.example            # 配置模板
├── .env.aliyun.example     # 阿里云配置模板
├── README.md               # 使用文档
├── QUICKSTART_ALIYUN.md    # 快速指南
├── docs\                   # 文档目录
└── 使用说明.txt            # 快速说明
```

## 💾 文件大小

**预期大小**:
- 压缩前: ~300-400 MB
- ZIP压缩后: ~150-200 MB

**大小优化**:
- 已排除不必要的库（matplotlib, scipy等）
- 使用UPX压缩
- 可进一步排除未使用的AI服务依赖

## 🎨 自定义图标

### 使用自动生成的图标

```bash
python create_icon.py
```

### 使用自定义图标

1. 准备256x256的PNG图像
2. 转换为ICO格式（可使用在线工具）
3. 命名为 `icon.ico`
4. 放在项目根目录

### 推荐工具

- [ConvertICO](https://convertico.com/)
- [ICO Convert](https://icoconvert.com/)
- Photoshop / GIMP

## 🔍 故障排除

### 问题1: 打包失败

**错误**: `ModuleNotFoundError`

**解决**:
```bash
# 检查依赖
pip list

# 重新安装
pip install -r requirements.txt
pip install -r build_requirements.txt
```

### 问题2: 运行时缺少DLL

**错误**: `DLL load failed`

**解决**:
- 安装 [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- 在spec文件中添加binaries

### 问题3: 程序启动慢

**原因**: PyInstaller首次解压需要时间

**优化**:
- 使用 `--onefile` 选项（但会更慢）
- 或保持当前目录模式（推荐）

### 问题4: 打包文件太大

**解决方案**:

1. **排除未使用的服务**:

编辑 `ai_subtitle.spec`:
```python
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
    'openai',  # 如果不用OpenAI
    'azure.cognitiveservices.speech',  # 如果不用Azure
]
```

2. **使用虚拟环境**:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
build.bat
```

### 问题5: 杀毒软件误报

**原因**: PyInstaller打包的程序可能被误报

**解决**:
- 添加到杀毒软件白名单
- 使用代码签名证书
- 向杀毒厂商报告误报

## 📤 分发方式

### 方式1: ZIP压缩包

```bash
# 手动压缩
# 压缩 dist\AI实时字幕\ 文件夹

# 或使用PowerShell
powershell -command "Compress-Archive -Path 'dist\AI实时字幕' -DestinationPath 'AI实时字幕.zip'"
```

### 方式2: 安装程序

使用 Inno Setup 或 NSIS 创建安装程序：

**Inno Setup示例**:
```iss
[Setup]
AppName=AI实时字幕
AppVersion=1.1.0
DefaultDirName={pf}\AI实时字幕
OutputBaseFilename=AI实时字幕_Setup

[Files]
Source: "dist\AI实时字幕\*"; DestDir: "{app}"; Flags: recursesubdirs
```

### 方式3: 便携版

```bash
build_portable.bat
```

自动创建包含配置向导的便携版。

## 🔐 代码签名（可选）

### 为什么需要签名

- 避免Windows SmartScreen警告
- 提升用户信任度
- 防止杀毒软件误报

### 签名步骤

1. **获取代码签名证书**
   - 从CA机构购买（如DigiCert, Sectigo）
   - 价格: $100-$500/年

2. **签名工具**
   ```bash
   # 使用signtool.exe（Windows SDK）
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com "AI实时字幕.exe"
   ```

3. **在spec中配置**
   ```python
   exe = EXE(
       ...,
       codesign_identity="Your Certificate Name",
   )
   ```

## 📊 性能优化

### 启动速度优化

1. **减少导入**:
   - 延迟导入不常用的模块
   - 使用条件导入

2. **使用单文件模式**:
   ```bash
   pyinstaller --onefile main.py
   ```
   注意: 启动会更慢，但分发更方便

### 文件大小优化

1. **使用虚拟环境打包**
2. **排除不需要的依赖**
3. **启用UPX压缩**
4. **移除调试信息**

## 🧪 测试清单

打包后测试：

- [ ] 程序能正常启动
- [ ] UI界面显示正常
- [ ] 音频捕获功能正常
- [ ] AI转录功能正常
- [ ] 配置文件读取正常
- [ ] 在干净的Windows系统上测试
- [ ] 测试不同Windows版本（Win10/11）
- [ ] 检查文件权限
- [ ] 测试网络连接功能

## 📝 发布清单

准备发布时：

- [ ] 更新版本号
- [ ] 更新README文档
- [ ] 测试所有功能
- [ ] 创建发布说明
- [ ] 准备用户文档
- [ ] 创建安装指南
- [ ] 准备示例配置
- [ ] 测试安装流程

## 🆘 获取帮助

**PyInstaller文档**:
- https://pyinstaller.org/

**常见问题**:
- https://github.com/pyinstaller/pyinstaller/wiki

**社区支持**:
- Stack Overflow
- PyInstaller GitHub Issues

## 📌 最佳实践

1. **使用虚拟环境**: 避免打包不必要的依赖
2. **测试打包结果**: 在干净系统上测试
3. **保持依赖最新**: 定期更新依赖库
4. **文档完善**: 提供详细的使用说明
5. **版本管理**: 记录每个版本的变更

---

**打包工具版本**: PyInstaller 6.3.0  
**Python版本**: 3.8+  
**目标平台**: Windows 10/11 (64-bit)
