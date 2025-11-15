@echo off
chcp 65001 >nul
echo ========================================
echo AI实时字幕工具 - 依赖安装脚本
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [信息] 检测到Python版本:
python --version
echo.

REM 升级pip
echo [步骤 1/3] 升级pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [警告] pip升级失败，继续安装...
)
echo.

REM 询问安装方式
echo 请选择安装方式:
echo 1. 完整安装 (推荐，包含所有AI服务)
echo 2. 最小安装 (仅核心功能)
echo 3. 自定义安装
echo.
set /p choice="请输入选项 (1/2/3): "

if "%choice%"=="1" goto full_install
if "%choice%"=="2" goto minimal_install
if "%choice%"=="3" goto custom_install
goto full_install

:full_install
echo.
echo [步骤 2/3] 安装所有依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 安装失败！
    echo.
    echo 建议:
    echo 1. 检查网络连接
    echo 2. 尝试使用国内镜像: pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo 3. 查看 INSTALL.md 获取详细帮助
    pause
    exit /b 1
)
goto verify

:minimal_install
echo.
echo [步骤 2/3] 安装核心依赖...
pip install -r requirements-minimal.txt
if errorlevel 1 (
    echo [错误] 安装失败！
    pause
    exit /b 1
)
echo.
echo [提示] 已安装核心依赖，如需使用AI服务，请手动安装:
echo   - OpenAI: pip install openai
echo   - Azure: pip install azure-cognitiveservices-speech
goto verify

:custom_install
echo.
echo [步骤 2/3] 自定义安装...
echo.
echo 正在安装核心依赖...
pip install PyQt5 sounddevice numpy python-dotenv requests
if errorlevel 1 (
    echo [错误] 核心依赖安装失败！
    pause
    exit /b 1
)
echo.
echo 是否安装OpenAI支持? (Y/N)
set /p install_openai=
if /i "%install_openai%"=="Y" (
    pip install openai
)
echo.
echo 是否安装Azure支持? (Y/N)
set /p install_azure=
if /i "%install_azure%"=="Y" (
    pip install azure-cognitiveservices-speech
)
goto verify

:verify
echo.
echo [步骤 3/3] 验证安装...
python -c "import PyQt5; import sounddevice; import numpy; import dotenv; import requests; print('✅ 核心依赖验证成功！')"
if errorlevel 1 (
    echo [错误] 依赖验证失败！
    echo 请查看 INSTALL.md 获取帮助
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ 安装完成！
echo ========================================
echo.
echo 下一步:
echo 1. 配置.env文件 (或使用图形化配置界面)
echo 2. 运行: python main.py
echo 3. 点击⚙按钮进行配置
echo.
echo 详细文档:
echo - 安装问题: INSTALL.md
echo - 配置指南: SETTINGS_GUIDE.md
echo - 快速开始: QUICKSTART_ALIYUN.md
echo.
pause
