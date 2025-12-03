@echo off
chcp 65001 >nul
echo ========================================
echo 修复Whisper打包依赖问题
echo ========================================
echo.

echo [步骤 1/4] 检查Python环境
python --version
if errorlevel 1 (
    echo [错误] Python未安装
    pause
    exit /b 1
)
echo.

echo [步骤 2/4] 安装PyTorch
echo 这可能需要5-10分钟，请耐心等待...
echo.
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo [错误] PyTorch安装失败
    echo.
    echo 请尝试手动安装:
    echo pip install torch torchaudio
    pause
    exit /b 1
)
echo [完成] PyTorch安装成功
echo.

echo [步骤 3/4] 安装openai-whisper
echo 这可能需要3-5分钟...
echo.
pip install openai-whisper
if errorlevel 1 (
    echo [错误] openai-whisper安装失败
    pause
    exit /b 1
)
echo [完成] openai-whisper安装成功
echo.

echo [步骤 4/4] 验证安装
echo.
python -c "import whisper; print('✅ Whisper:', whisper.__version__)"
python -c "import torch; print('✅ PyTorch:', torch.__version__)"
echo.

echo ========================================
echo ✅ 依赖安装完成！
echo ========================================
echo.
echo 现在可以运行: build_with_whisper.bat
echo.
pause
