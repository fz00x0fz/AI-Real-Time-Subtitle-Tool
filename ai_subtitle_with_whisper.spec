# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller配置文件 - 包含本地Whisper模型
用于将AI实时字幕工具打包为Windows可执行文件（包含本地Whisper支持）
"""

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
            # 添加所有DLL文件
            for dll in lib_dir.glob('*.dll'):
                binaries.append((str(dll), 'torch/lib'))
            print(f"找到 {len(binaries)} 个PyTorch DLL文件")
    except Exception as e:
        print(f"警告: 无法获取PyTorch DLL文件: {e}")
    
    return binaries

# 分析依赖
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=get_torch_binaries(),
    datas=[
        ('.env.example', '.'),
        ('.env.aliyun.example', '.'),
        ('README.md', '.'),
        ('README_EN.md', '.'),
        ('LICENSE', '.'),
        ('docs', 'docs'),
    ],
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
        
        # Whisper本地模型相关
        'whisper',
        'torch',
        'torchaudio',
        'ffmpeg',
        'tiktoken',
        'numba',
        'librosa',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 数据科学库（不需要）
        'matplotlib',
        'scipy',
        'pandas',
        'PIL',
        'tkinter',
        
        # TensorFlow相关（不需要）
        'tensorboard',
        'tensorflow',
        
        # Jupyter相关（不需要）
        'IPython',
        'jupyter',
        'notebook',
        
        # 测试框架（不需要）
        'pytest',
        'unittest',
        'nose',
        
        # 其他不需要的库
        'setuptools',
        'pip',
        'wheel',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 打包资源
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AI实时字幕_本地模型版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX，避免DLL损坏
    console=True,  # 显示控制台窗口，方便查看日志
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

# 收集所有文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # 禁用UPX，避免DLL损坏
    upx_exclude=[],
    name='AI实时字幕_本地模型版',
)
