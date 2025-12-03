@echo off
chcp 65001 >nul
echo ========================================
echo    创建便携版安装包
echo ========================================
echo.

REM 检查dist目录是否存在
if not exist "dist\AI实时字幕" (
    echo [错误] 未找到打包文件
    echo [提示] 请先运行 build.bat 进行打包
    pause
    exit /b 1
)

echo [1/3] 创建便携版目录结构...
set PORTABLE_DIR=AI实时字幕_便携版
if exist %PORTABLE_DIR% rmdir /s /q %PORTABLE_DIR%
mkdir %PORTABLE_DIR%

echo [2/3] 复制程序文件...
xcopy "dist\AI实时字幕\*" "%PORTABLE_DIR%\" /E /I /Y >nul

echo [3/3] 创建快速配置向导...
(
echo @echo off
echo chcp 65001 ^>nul
echo cls
echo ========================================
echo    AI实时字幕 - 快速配置向导
echo ========================================
echo.
echo 请选择AI服务：
echo.
echo 1. 阿里云百炼 ^(推荐，国内访问快^)
echo 2. OpenAI Whisper
echo 3. Azure Speech
echo 4. 本地Whisper ^(需要GPU^)
echo.
set /p choice="请输入选项 (1-4): "
echo.

if "%%choice%%"=="1" (
    echo 正在配置阿里云百炼...
    copy .env.aliyun.example .env ^>nul
    echo.
    echo ✓ 已创建配置文件
    echo.
    echo 下一步：
    echo 1. 访问 https://dashscope.aliyun.com/
    echo 2. 获取API密钥
    echo 3. 编辑 .env 文件，填入：
    echo    ALIYUN_API_KEY=你的密钥
    echo.
    notepad .env
) else if "%%choice%%"=="2" (
    echo 正在配置OpenAI...
    copy .env.example .env ^>nul
    echo AI_SERVICE=openai ^> .env
    echo OPENAI_API_KEY=your_key_here ^>^> .env
    echo.
    echo ✓ 已创建配置文件
    echo.
    echo 下一步：
    echo 1. 访问 https://platform.openai.com/
    echo 2. 获取API密钥
    echo 3. 编辑 .env 文件，填入密钥
    echo.
    notepad .env
) else if "%%choice%%"=="3" (
    echo 正在配置Azure...
    copy .env.example .env ^>nul
    echo AI_SERVICE=azure ^> .env
    echo AZURE_SPEECH_KEY=your_key_here ^>^> .env
    echo AZURE_SPEECH_REGION=eastus ^>^> .env
    echo.
    echo ✓ 已创建配置文件
    echo.
    notepad .env
) else if "%%choice%%"=="4" (
    echo 正在配置本地Whisper...
    copy .env.example .env ^>nul
    echo AI_SERVICE=local_whisper ^> .env
    echo.
    echo ✓ 已创建配置文件
    echo.
    echo 注意：本地Whisper需要：
    echo - 较好的CPU/GPU性能
    echo - 至少8GB内存
    echo - 首次运行会下载模型
) else (
    echo 无效选项
    pause
    exit /b 1
)

echo.
echo ========================================
echo 配置完成！
echo ========================================
echo.
set /p run="是否立即启动应用？(Y/N): "
if /i "%%run%%"=="Y" (
    start "" "AI实时字幕.exe"
)
) > "%PORTABLE_DIR%\配置向导.bat"

REM 创建README
(
echo # AI实时字幕 - 便携版
echo.
echo ## 快速开始
echo.
echo 1. **首次使用**：双击运行 `配置向导.bat`
echo 2. **日常使用**：双击运行 `AI实时字幕.exe`
echo.
echo ## 配置说明
echo.
echo ### 阿里云百炼（推荐）
echo - 访问：https://dashscope.aliyun.com/
echo - 获取API密钥
echo - 编辑 .env 文件配置
echo.
echo ### 启用音频捕获
echo 1. 右键任务栏音量图标
echo 2. 声音设置 → 声音控制面板
echo 3. 录制选项卡
echo 4. 启用"立体声混音"
echo.
echo ## 使用方法
echo 1. 启动应用
echo 2. 点击"开始"按钮
echo 3. 播放音频/视频
echo 4. 实时字幕显示
echo.
echo ## 技术支持
echo - 查看 README.md 获取详细文档
echo - 查看 docs\QUICKSTART_ALIYUN.md 快速配置
echo - 查看 docs 目录获取更多文档
echo.
echo ## 系统要求
echo - Windows 10/11
echo - 音频输出设备
echo.
) > "%PORTABLE_DIR%\README_便携版.txt"

echo.
echo ========================================
echo ✅ 便携版创建完成！
echo ========================================
echo.
echo 输出目录: %PORTABLE_DIR%\
echo.
echo 文件说明：
echo - AI实时字幕.exe      主程序
echo - 配置向导.bat         快速配置工具
echo - README_便携版.txt    使用说明
echo - .env.example         配置模板
echo.
echo 分发方式：
echo 1. 压缩整个文件夹为ZIP
echo 2. 发送给用户
echo 3. 用户解压后运行"配置向导.bat"
echo.

REM 询问是否创建ZIP
set /p zip="是否创建ZIP压缩包？(Y/N): "
if /i "%zip%"=="Y" (
    echo.
    echo 正在创建ZIP压缩包...
    powershell -command "Compress-Archive -Path '%PORTABLE_DIR%' -DestinationPath 'AI实时字幕_便携版.zip' -Force"
    if exist "AI实时字幕_便携版.zip" (
        echo ✓ ZIP创建成功: AI实时字幕_便携版.zip
    ) else (
        echo ✗ ZIP创建失败
    )
)

echo.
set /p open="是否打开输出目录？(Y/N): "
if /i "%open%"=="Y" (
    explorer "%PORTABLE_DIR%"
)

pause
