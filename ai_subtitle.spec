# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller配置文件
用于将AI实时字幕工具打包为Windows可执行文件
"""

block_cipher = None

# 分析依赖
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
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
        
        # TensorFlow/PyTorch相关（不需要）
        'tensorboard',
        'tensorflow',
        'torch',
        'torchvision',
        
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
    name='AI实时字幕',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    upx=True,
    upx_exclude=[],
    name='AI实时字幕',
)
