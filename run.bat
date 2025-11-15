@echo off
chcp 65001 >nul
echo ========================================
echo    AI实时字幕工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查.env文件是否存在
if not exist .env (
    echo [警告] 未找到.env配置文件
    echo [提示] 正在从.env.example创建.env文件...
    copy .env.example .env >nul
    echo [完成] 请编辑.env文件配置API密钥后重新运行
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [提示] 检测到缺少依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [启动] 正在启动AI实时字幕工具...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出
    pause
)
