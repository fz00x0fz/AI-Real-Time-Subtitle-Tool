@echo off
chcp 65001 >nul
echo ========================================
echo    AI实时字幕工具 - Windows打包脚本
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/5] 检查打包依赖...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装打包依赖...
    pip install -r build_requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [2/5] 检查运行时依赖...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装运行时依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [3/5] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "AI实时字幕.spec" del "AI实时字幕.spec"

echo [4/5] 开始打包应用...
echo [提示] 这可能需要几分钟时间，请耐心等待...
echo.
pyinstaller ai_subtitle.spec --clean

if errorlevel 1 (
    echo.
    echo [错误] 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo [5/5] 复制配置文件到发布目录...
copy .env.example "dist\AI实时字幕\" >nul
copy .env.aliyun.example "dist\AI实时字幕\" >nul
copy README.md "dist\AI实时字幕\" >nul
copy README_EN.md "dist\AI实时字幕\" >nul
copy LICENSE "dist\AI实时字幕\" >nul
if exist "docs" (
    xcopy /y /e /i "docs" "dist\AI实时字幕\docs" >nul
    echo [完成] 已复制 docs 目录
)

REM 创建启动说明
echo 创建使用说明...
(
echo ========================================
echo    AI实时字幕工具 - 使用说明
echo ========================================
echo.
echo 1. 首次使用前，请配置.env文件：
echo    - 复制 .env.example 为 .env
echo    - 编辑 .env 文件，填入你的API密钥
echo.
echo 2. 启动应用：
echo    - 双击 "AI实时字幕.exe" 运行
echo.
echo 3. 阿里云快速配置：
echo    - 复制 .env.aliyun.example 为 .env
echo    - 填入阿里云API密钥
echo    - 查看 docs\QUICKSTART_ALIYUN.md 获取详细步骤
echo.
echo 4. 启用音频捕获：
echo    - 在Windows声音设置中启用"立体声混音"
echo    - 详见 README.md 文档
echo.
echo 5. 技术支持：
echo    - 查看 README.md 获取完整文档
echo    - 遇到问题请查看故障排除部分
echo.
echo ========================================
) > "dist\AI实时字幕\使用说明.txt"

echo.
echo ========================================
echo ✅ 打包完成！
echo ========================================
echo.
echo 输出目录: dist\AI实时字幕\
echo 主程序: AI实时字幕.exe
echo.
echo 下一步：
echo 1. 进入 dist\AI实时字幕\ 目录
echo 2. 配置 .env 文件
echo 3. 运行 AI实时字幕.exe
echo.
echo 分发说明：
echo - 可以将整个 "AI实时字幕" 文件夹打包分发
echo - 用户无需安装Python环境
echo - 所有依赖已打包在内
echo ========================================
echo.

REM 询问是否打开输出目录
set /p open="是否打开输出目录？(Y/N): "
if /i "%open%"=="Y" (
    explorer "dist\AI实时字幕"
)

pause
