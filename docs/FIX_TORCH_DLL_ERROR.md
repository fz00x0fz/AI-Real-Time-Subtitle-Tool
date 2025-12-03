# 修复PyTorch DLL错误

## 🐛 错误信息

```
[WinError 1114] 动态链接库(DLL)初始化程序失败。Error loading "E:\project\LiteTool\ai_subtitle_tool\dist\AI实时字幕_本地模型版\_internal\torch\lib\c10.dll" or one of its dependencies.
```

## 🔍 问题原因

PyInstaller打包PyTorch应用时，常见的DLL依赖问题：

1. **c10.dll 缺失或损坏**
2. **依赖的其他DLL未正确打包**
3. **DLL加载顺序问题**

---

## ✅ 解决方案

### 方案1: 修复spec文件（已应用）

我已经修改了 `ai_subtitle_with_whisper.spec`，添加了自动收集PyTorch DLL的功能。

**修改内容**:
```python
# 获取torch库路径
def get_torch_binaries():
    """获取PyTorch的DLL文件"""
    binaries = []
    try:
        import torch
        torch_dir = Path(torch.__file__).parent
        lib_dir = torch_dir / 'lib'
        
        if lib_dir.exists():
            # 添加所有DLL文件
            for dll in lib_dir.glob('*.dll'):
                binaries.append((str(dll), 'torch/lib'))
            print(f"找到 {len(binaries)} 个PyTorch DLL文件")
    except Exception as e:
        print(f"警告: 无法获取PyTorch DLL文件: {e}")
    
    return binaries

# 在Analysis中使用
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=get_torch_binaries(),  # 添加PyTorch DLL
    ...
)
```

### 方案2: 手动添加DLL路径

如果方案1不work，可以手动指定：

```python
import torch
torch_path = os.path.dirname(torch.__file__)

binaries=[
    (os.path.join(torch_path, 'lib', '*.dll'), 'torch/lib'),
]
```

### 方案3: 使用PyInstaller hooks

创建 `hook-torch.py`:

```python
from PyInstaller.utils.hooks import collect_dynamic_libs

binaries = collect_dynamic_libs('torch')
```

---

## 🚀 重新打包

### 步骤1: 清理旧文件

```bash
rmdir /s /q build dist
```

### 步骤2: 重新打包

```bash
build_with_whisper.bat
```

### 步骤3: 验证

打包完成后，检查：

```bash
# 检查DLL是否存在
dir "dist\AI实时字幕_本地模型版\_internal\torch\lib\*.dll"
```

应该看到类似：
```
c10.dll
torch_cpu.dll
torch_python.dll
fbgemm.dll
asmjit.dll
...
```

---

## 🔧 其他可能的解决方案

### 1. 安装Visual C++ Redistributable

某些DLL依赖Visual C++运行库：

**下载安装**:
- [Microsoft Visual C++ 2015-2022 Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### 2. 使用CPU版本的PyTorch

如果使用GPU版本，尝试切换到CPU版本：

```bash
# 卸载当前版本
pip uninstall torch torchaudio

# 安装CPU版本
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

CPU版本体积更小，依赖更少。

### 3. 添加更多hiddenimports

在spec文件中添加：

```python
hiddenimports=[
    'torch',
    'torch.nn',
    'torch.nn.functional',
    'torch._C',
    'torch._six',
    ...
]
```

### 4. 禁用UPX压缩

UPX压缩可能导致DLL损坏：

```python
exe = EXE(
    ...
    upx=False,  # 禁用UPX
    ...
)

coll = COLLECT(
    ...
    upx=False,  # 禁用UPX
    ...
)
```

---

## 📋 完整的spec文件示例

```python
# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None

# 获取torch库路径
def get_torch_binaries():
    """获取PyTorch的DLL文件"""
    binaries = []
    try:
        import torch
        torch_dir = Path(torch.__file__).parent
        lib_dir = torch_dir / 'lib'
        
        if lib_dir.exists():
            for dll in lib_dir.glob('*.dll'):
                binaries.append((str(dll), 'torch/lib'))
            print(f"找到 {len(binaries)} 个PyTorch DLL文件")
    except Exception as e:
        print(f"警告: 无法获取PyTorch DLL文件: {e}")
    
    return binaries

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=get_torch_binaries(),
    datas=[
        ('.env.example', '.'),
        ('README.md', '.'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        'torch',
        'torch.nn',
        'torch._C',
        'whisper',
        ...
    ],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI实时字幕_本地模型版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # 禁用UPX
    upx_exclude=[],
    name='AI实时字幕_本地模型版',
)
```

---

## 🧪 测试步骤

### 1. 验证打包环境

```bash
# 检查torch是否正常
python -c "import torch; print(torch.__version__)"

# 检查DLL位置
python -c "import torch; import os; print(os.path.join(os.path.dirname(torch.__file__), 'lib'))"
```

### 2. 清理并重新打包

```bash
# 清理
rmdir /s /q build dist

# 打包
build_with_whisper.bat
```

### 3. 检查打包结果

```bash
# 进入dist目录
cd "dist\AI实时字幕_本地模型版"

# 检查torch/lib目录
dir _internal\torch\lib

# 运行测试
AI实时字幕_本地模型版.exe
```

---

## 💡 推荐方案

如果本地模型版打包仍然困难，强烈推荐：

### **使用标准版 + 运行时安装**

**优势**:
- ✅ 不需要打包PyTorch
- ✅ 避免DLL依赖问题
- ✅ 打包体积小（50-200MB）
- ✅ 打包速度快
- ✅ 用户按需安装

**使用方法**:
```bash
# 打包标准版
build.bat

# 用户在应用中点击"安装本地模型"即可
```

详见: [运行时安装指南](docs/RUNTIME_INSTALL_GUIDE.md)

---

## 📊 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| 修复spec文件 | 一次打包完成 | 可能遇到DLL问题 | ⭐⭐⭐ |
| 标准版+运行时安装 | 简单可靠 | 需要网络下载 | ⭐⭐⭐⭐⭐ |
| 手动复制DLL | 灵活 | 繁琐 | ⭐⭐ |

---

## 🔗 相关资源

- [PyInstaller文档](https://pyinstaller.org/)
- [PyTorch打包指南](https://pytorch.org/docs/stable/notes/windows.html)
- [运行时安装指南](docs/RUNTIME_INSTALL_GUIDE.md)
- [打包故障排除](BUILD_WHISPER_TROUBLESHOOTING.md)

---

## 📞 需要帮助？

如果问题仍未解决：

1. 查看完整的打包日志
2. 检查 `_internal\torch\lib` 目录是否有DLL文件
3. 尝试使用标准版 + 运行时安装
4. 提交Issue并附上详细错误信息

---

**最后更新**: 2024-11-15  
**适用版本**: v1.0.0+
