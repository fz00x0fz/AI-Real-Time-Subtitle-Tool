@echo off
chcp 65001 >nul
echo ========================================
echo AI实时字幕工具 - 调试运行
echo ========================================
echo.

REM 设置Python环境
set PYTHONIOENCODING=utf-8

REM 运行程序
python main.py

REM 程序退出后的清理
echo.
echo ========================================
echo 程序已退出，正在清理...
echo ========================================

REM 强制结束可能残留的Python进程
taskkill /F /IM python.exe /FI "WINDOWTITLE eq AI*" 2>nul

echo 清理完成
echo.
pause
