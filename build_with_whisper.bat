@echo off
chcp 65001 >nul
echo ========================================
echo AI实时字幕工具 - 本地模型版打包脚本
echo ========================================
echo.
echo 注意: 此版本包含本地Whisper模型支持
echo 打包体积较大 (约1-2GB)
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [信息] Python版本:
python --version
echo.

REM 询问是否继续
echo 本地模型版本特点:
echo ✅ 包含完整的Whisper模型支持
echo ✅ 无需联网即可使用语音识别
echo ✅ 支持离线场景
echo.
echo ⚠️  注意事项:
echo • 打包时间较长 (10-30分钟)
echo • 打包体积较大 (1-2GB)
echo • 需要安装额外依赖
echo.
set /p continue="是否继续打包本地模型版本? (Y/N): "
if /i not "%continue%"=="Y" (
    echo 已取消打包
    pause
    exit /b 0
)

echo.
echo ========================================
echo 步骤 1/5: 检查并安装依赖
echo ========================================
echo.

REM 检查是否已安装openai-whisper
python -c "import whisper" >nul 2>&1
if errorlevel 1 (
    echo [信息] 未检测到openai-whisper，正在安装...
    echo.
    echo 这可能需要几分钟时间...
    pip install openai-whisper
    if errorlevel 1 (
        echo [错误] openai-whisper安装失败
        echo.
        echo 请手动安装:
        echo pip install openai-whisper
        pause
        exit /b 1
    )
    echo [成功] openai-whisper安装完成
) else (
    echo [信息] openai-whisper已安装
)
echo.

REM 检查PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [信息] 安装打包工具...
    pip install -r build_requirements.txt
    if errorlevel 1 (
        echo [错误] 打包工具安装失败
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo 步骤 2/5: 清理旧构建文件
echo ========================================
echo.

if exist "build" (
    echo [信息] 清理build目录...
    rmdir /s /q build
)

if exist "dist\AI实时字幕_本地模型版" (
    echo [信息] 清理旧的dist目录...
    rmdir /s /q "dist\AI实时字幕_本地模型版"
)

echo [完成] 清理完成
echo.

echo.
echo ========================================
echo 步骤 3/5: 创建图标文件
echo ========================================
echo.

if not exist "icon.ico" (
    echo [信息] 创建应用图标...
    python create_icon.py
    if errorlevel 1 (
        echo [警告] 图标创建失败，将使用默认图标
    ) else (
        echo [完成] 图标创建成功
    )
) else (
    echo [信息] 图标文件已存在
)
echo.

echo.
echo ========================================
echo 步骤 4/5: 运行PyInstaller打包
echo ========================================
echo.
echo 这可能需要10-30分钟，请耐心等待...
echo.

pyinstaller ai_subtitle_with_whisper.spec --clean

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    echo.
    echo 常见问题:
    echo 1. 内存不足 - 关闭其他程序
    echo 2. 磁盘空间不足 - 至少需要5GB空闲空间
    echo 3. 依赖缺失 - 运行: pip install openai-whisper torch
    echo.
    echo 详细帮助: BUILD_TROUBLESHOOTING.md
    pause
    exit /b 1
)

echo.
echo [完成] 打包完成
echo.

echo.
echo ========================================
echo 步骤 5/5: 复制配置文件和文档
echo ========================================
echo.

set DIST_DIR=dist\AI实时字幕_本地模型版

REM 复制配置文件
if exist ".env.example" (
    copy /y ".env.example" "%DIST_DIR%\" >nul
    echo [完成] 已复制 .env.example
)

if exist ".env.aliyun.example" (
    copy /y ".env.aliyun.example" "%DIST_DIR%\" >nul
    echo [完成] 已复制 .env.aliyun.example
)

REM 复制文档
if exist "README.md" (
    copy /y "README.md" "%DIST_DIR%\" >nul
    echo [完成] 已复制 README.md
)

if exist "README_EN.md" (
    copy /y "README_EN.md" "%DIST_DIR%\" >nul
    echo [完成] 已复制 README_EN.md
)

if exist "LICENSE" (
    copy /y "LICENSE" "%DIST_DIR%\" >nul
    echo [完成] 已复制 LICENSE
)

REM 复制docs目录（包含所有文档）
if exist "docs" (
    if not exist "%DIST_DIR%\docs" mkdir "%DIST_DIR%\docs"
    xcopy /y /e /i "docs" "%DIST_DIR%\docs" >nul
    echo [完成] 已复制 docs 目录
)

REM 创建使用说明
echo 创建使用说明...
(
echo ========================================
echo AI实时字幕工具 - 本地模型版
echo ========================================
echo.
echo 版本特点:
echo ✅ 包含完整的Whisper本地模型支持
echo ✅ 支持离线语音识别
echo ✅ 无需联网即可使用
echo.
echo 快速开始:
echo 1. 双击运行 "AI实时字幕_本地模型版.exe"
echo 2. 首次运行会自动下载Whisper模型 (约140MB)
echo 3. 点击⚙按钮进行配置
echo 4. 在AI服务中选择"本地Whisper模型"
echo 5. 点击▶开始按钮开始捕获音频
echo.
echo 配置说明:
echo • 复制 .env.example 为 .env
echo • 编辑 .env 文件设置 AI_SERVICE=local_whisper
echo • 或使用图形化配置界面 (点击⚙按钮^)
echo.
echo 音频设置:
echo • 如使用外接音箱/耳机，请查看 EXTERNAL_AUDIO_SETUP.md
echo • 如使用内置音箱，请查看 AUDIO_SETUP.md
echo.
echo 模型说明:
echo • 首次运行会下载base模型 (约140MB^)
echo • 模型保存在: %%USERPROFILE%%\.cache\whisper
echo • 支持的模型: tiny, base, small, medium, large
echo • 模型越大，识别越准确，但速度越慢
echo.
echo 系统要求:
echo • Windows 10/11
echo • 至少4GB内存
echo • 至少2GB磁盘空间
echo.
echo 详细文档:
echo • README.md - 完整使用指南
echo • SETTINGS_GUIDE.md - 配置指南
echo • AUDIO_SETUP.md - 音频设置
echo.
echo 技术支持:
echo • 查看文档目录获取更多帮助
echo • 遇到问题请查看 README.md 中的故障排除部分
echo.
echo ========================================
) > "%DIST_DIR%\使用说明_本地模型版.txt"

echo [完成] 已创建使用说明
echo.

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 输出目录: %DIST_DIR%
echo 主程序: AI实时字幕_本地模型版.exe
echo 打包大小: 约1-2GB
echo.
echo 重要提示:
echo 1. 首次运行会下载Whisper模型 (约140MB)
echo 2. 需要联网下载模型 (仅首次)
echo 3. 下载完成后可离线使用
echo.
echo 下一步:
echo 1. 进入 %DIST_DIR%
echo 2. 双击运行 AI实时字幕_本地模型版.exe
echo 3. 等待模型下载完成
echo 4. 开始使用
echo.
echo 如需创建便携版安装包:
echo 运行: build_portable.bat
echo.

pause
